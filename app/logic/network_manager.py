import asyncio
import threading
from typing import List, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal
from dbus_fast.aio import MessageBus
from dbus_fast import BusType, Variant

_SAMPLE_NETWORKS = [
    {"ssid": "Home_WiFi_5G", "strength": 92, "secured": True, "connected": False, "band": "5GHz", "frequency": 5180},
    {"ssid": "Home_WiFi_2.4G", "strength": 85, "secured": True, "connected": False, "band": "2.4GHz", "frequency": 2412},
    {"ssid": "CoffeeShop_Guest", "strength": 67, "secured": False, "connected": False, "band": "2.4GHz", "frequency": 2437},
    {"ssid": "Office_Network", "strength": 58, "secured": True, "connected": False, "band": "5GHz", "frequency": 5180},
]

class NetworkManager(QObject):
    network_changed = pyqtSignal(list)
    connection_changed = pyqtSignal(str)

    NM_BUS_NAME = "org.freedesktop.NetworkManager"
    NM_PATH = "/org/freedesktop/NetworkManager"
    NM_DEVICE_IFACE = "org.freedesktop.NetworkManager.Device"
    NM_WIFI_IFACE = "org.freedesktop.NetworkManager.Device.Wireless"
    NM_AP_IFACE = "org.freedesktop.NetworkManager.AccessPoint"
    NM_ACTIVE_IFACE = "org.freedesktop.NetworkManager.Connection.Active"
    DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"

    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.current_network: str | None = None
        self.networks: List[Dict[str, Any]] = []
        self._loop = asyncio.new_event_loop()
        self._bus = None
        self._running = True
        self.monitor = self

        print("[NM LOG] Starting NetworkManager thread")
        self._thread = threading.Thread(target=self._thread_main, daemon=True)
        self._thread.start()
        threading.Timer(0.8, lambda: print("[NM LOG] Watchdog timer triggered")).start()

    def _thread_main(self):
        asyncio.set_event_loop(self._loop)
        print("[NM LOG] Asyncio loop set in thread")
        try:
            self._loop.run_until_complete(self._async_init())
            print("[NM LOG] Async init finished, entering loop")
            self._loop.run_forever()
        except Exception as e:
            print("[NM LOG] NetworkManager thread error:", e)

    async def _async_init(self):
        try:
            print("[NM LOG] Connecting to system bus...")
            self._bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
            self._bus.add_message_handler(self._on_dbus_message)
            print("[NM LOG] Connected to DBus, doing initial scan...")
            await self._async_scan_networks()
            await self._async_update_current_connection()
            print("[NM LOG] Initial network scan and connection update done")
        except Exception as e:
            print("[NM LOG] NetworkManager async init failed:", e)

    def _on_dbus_message(self, msg):
        try:
            if not msg or msg.sender != self.NM_BUS_NAME:
                return
            member = getattr(msg, "member", "")
            print(f"[NM LOG] DBus message received: {member}")
            if member in ("AccessPointAdded", "AccessPointRemoved", "PropertiesChanged", "StateChanged"):
                print("[NM LOG] Scheduling scan and update due to signal")
                asyncio.run_coroutine_threadsafe(self._async_scan_networks(), self._loop)
                asyncio.run_coroutine_threadsafe(self._async_update_current_connection(), self._loop)
        except Exception as e:
            print("[NM LOG] _on_dbus_message error:", e)

    def scan_networks(self, timeout: float = 5.0) -> List[Dict[str, Any]]:
        print("[NM LOG] scan_networks called")
        if not self._bus:
            print("[NM LOG] DBus not ready, returning sample networks")
            return list(_SAMPLE_NETWORKS)
        fut = asyncio.run_coroutine_threadsafe(self._async_scan_networks(), self._loop)
        try:
            fut.result(timeout=timeout)
        except Exception as e:
            print("[NM LOG] scan_networks: async scan failed or timed out:", e)
        return list(self.networks) if self.networks else list(_SAMPLE_NETWORKS)

    def connect_to_network(self, ssid: str, password: str | None = None, timeout: float = 30.0) -> bool:
        print(f"[NM LOG] connect_to_network called for SSID: {ssid}")
        if not self._bus:
            print("[NM LOG] DBus not available, simulating connection (mock)")
            self.current_network = ssid
            self.connection_changed.emit(ssid or "")
            return True
        fut = asyncio.run_coroutine_threadsafe(self._async_connect(ssid, password), self._loop)
        try:
            success = bool(fut.result(timeout=timeout))
            print(f"[NM LOG] connect_to_network result: {success}")
            return success
        except Exception as e:
            print("[NM LOG] connect_to_network error:", e)
            return False

    async def _async_scan_networks(self):
        print("[NM LOG] _async_scan_networks started")
        try:
            if not self._bus:
                raise RuntimeError("DBus MessageBus not available")

            nm_intro = await self._bus.introspect(self.NM_BUS_NAME, self.NM_PATH)
            nm_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, self.NM_PATH, nm_intro)
            nm_iface = nm_obj.get_interface(self.NM_BUS_NAME)
            nm_props = nm_obj.get_interface(self.DBUS_PROP_IFACE)

            try:
                devices = await nm_iface.call_get_devices()
            except Exception:
                try:
                    devices_variant = await nm_props.call_get(self.NM_BUS_NAME, "Devices")
                    devices = devices_variant.value if hasattr(devices_variant, "value") else devices_variant
                except Exception:
                    devices = []

            print(f"[NM LOG] Devices: {devices}")
            networks: List[Dict[str, Any]] = []

            for dev_path in devices:
                try:
                    dev_intro = await self._bus.introspect(self.NM_BUS_NAME, dev_path)
                    dev_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, dev_path, dev_intro)
                    dev_props = dev_obj.get_interface(self.DBUS_PROP_IFACE)
                except Exception as e:
                    print(f"[NM LOG] Cannot introspect device {dev_path}: {e}")
                    continue

                try:
                    dtype_variant = await dev_props.call_get(self.NM_DEVICE_IFACE, "DeviceType")
                    dtype = dtype_variant.value if hasattr(dtype_variant, "value") else dtype_variant
                except Exception as e:
                    print(f"[NM LOG] Cannot read DeviceType for {dev_path}: {e}")
                    dtype = None

                if dtype != 2:
                    print(f"[NM LOG] Device {dev_path} type is {dtype}, skipping (not WiFi)")
                    continue

                try:
                    wifi_iface = dev_obj.get_interface(self.NM_WIFI_IFACE)
                    aps = await wifi_iface.call_get_access_points()
                except Exception:
                    try:
                        aps_variant = await dev_props.call_get(self.NM_WIFI_IFACE, "AccessPoints")
                        aps = aps_variant.value if hasattr(aps_variant, "value") else aps_variant
                    except Exception:
                        aps = []

                print(f"[NM LOG] AccessPoints for {dev_path}: {aps}")

                for ap_path in aps:
                    try:
                        ap_intro = await self._bus.introspect(self.NM_BUS_NAME, ap_path)
                        ap_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, ap_path, ap_intro)
                        ap_props = ap_obj.get_interface(self.DBUS_PROP_IFACE)
                        ssid_variant = await ap_props.call_get(self.NM_AP_IFACE, "Ssid")
                        strength_variant = await ap_props.call_get(self.NM_AP_IFACE, "Strength")
                        freq_variant = await ap_props.call_get(self.NM_AP_IFACE, "Frequency")
                        ssid_raw = ssid_variant.value if hasattr(ssid_variant, "value") else ssid_variant
                        strength_raw = strength_variant.value if hasattr(strength_variant, "value") else strength_variant
                        freq_raw = freq_variant.value if hasattr(freq_variant, "value") else freq_variant

                        ssid = bytes(ssid_raw).decode("utf-8", errors="ignore") if isinstance(ssid_raw, (list, tuple, bytes, bytearray)) else str(ssid_raw)
                        strength = int(strength_raw)
                        freq = int(freq_raw)
                        connected = ssid == (self.current_network or "")
                        secured = True
                        try:
                            wpa_flags = (await ap_props.call_get(self.NM_AP_IFACE, "WpaFlags")).value
                            rsn_flags = (await ap_props.call_get(self.NM_AP_IFACE, "RsnFlags")).value
                            flags = (await ap_props.call_get(self.NM_AP_IFACE, "Flags")).value
                            if not wpa_flags and not rsn_flags and flags == 0:
                                secured = False
                        except Exception:
                            pass
                        networks.append({"ssid": ssid, "strength": strength, "frequency": freq, "secured": secured, "connected": connected})
                    except Exception as e:
                        print(f"[NM LOG] Cannot read AP {ap_path} props: {e}")
                        continue

            dedup = {}
            for n in sorted(networks, key=lambda x: x["strength"], reverse=True):
                if n["ssid"] not in dedup or n["strength"] > dedup[n["ssid"]]["strength"]:
                    dedup[n["ssid"]] = n
            self.networks = list(dedup.values())
            print(f"[NM LOG] Networks found: {[n['ssid'] for n in self.networks]}")
            self.network_changed.emit(self.networks)
            return self.networks
        except Exception as e:
            print("[NM LOG] async_scan_networks error:", e)
            if not self.networks:
                self.networks = list(_SAMPLE_NETWORKS)
                self.network_changed.emit(self.networks)
            return self.networks

    async def _async_update_current_connection(self):
        print("[NM LOG] _async_update_current_connection started")
        try:
            if not self._bus:
                raise RuntimeError("DBus MessageBus not available")

            nm_intro = await self._bus.introspect(self.NM_BUS_NAME, self.NM_PATH)
            nm_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, self.NM_PATH, nm_intro)
            nm_props = nm_obj.get_interface(self.DBUS_PROP_IFACE)

            # Pobierz listę aktywnych połączeń
            try:
                active_variant = await nm_props.call_get(self.NM_BUS_NAME, "ActiveConnections")
                active = active_variant.value if hasattr(active_variant, "value") else active_variant
            except Exception:
                active = []

            current_ssid = None
            
            # Przeszukaj aktywne połączenia
            for ac_path in active:
                try:
                    ac_intro = await self._bus.introspect(self.NM_BUS_NAME, ac_path)
                    ac_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, ac_path, ac_intro)
                    ac_props = ac_obj.get_interface(self.DBUS_PROP_IFACE)
                    
                    # 1. Sprawdź typ połączenia (chcemy Wireless - '802-11-wireless')
                    type_variant = await ac_props.call_get(self.NM_ACTIVE_IFACE, "Type")
                    con_type = type_variant.value if hasattr(type_variant, "value") else type_variant
                    
                    # 2. Spróbuj pobrać SSID z obiektu AccessPoint (SpecificObject)
                    # To jest kluczowe! SpecificObject wskazuje na konkretny AP (router)
                    spec_obj_variant = await ac_props.call_get(self.NM_ACTIVE_IFACE, "SpecificObject")
                    spec_obj_path = spec_obj_variant.value if hasattr(spec_obj_variant, "value") else spec_obj_variant
                    
                    found_real_ssid = False
                    
                    if spec_obj_path and spec_obj_path != "/":
                        try:
                            # Introspekcja AccessPointa
                            ap_intro = await self._bus.introspect(self.NM_BUS_NAME, spec_obj_path)
                            ap_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, spec_obj_path, ap_intro)
                            ap_props = ap_obj.get_interface(self.DBUS_PROP_IFACE)
                            
                            ssid_variant = await ap_props.call_get(self.NM_AP_IFACE, "Ssid")
                            ssid_raw = ssid_variant.value if hasattr(ssid_variant, "value") else ssid_variant
                            
                            # Dekodowanie SSID
                            if isinstance(ssid_raw, (list, tuple, bytes, bytearray)):
                                current_ssid = bytes(ssid_raw).decode("utf-8", errors="ignore")
                            else:
                                current_ssid = str(ssid_raw)
                                
                            found_real_ssid = True
                        except Exception as e:
                            print(f"[NM LOG] Failed to get SSID from AP: {e}")

                    # 3. Jeśli nie udało się pobrać SSID (lub to nie Wi-Fi), użyj nazwy profilu (Id) jako fallback
                    if not found_real_ssid:
                        cid_variant = await ac_props.call_get(self.NM_ACTIVE_IFACE, "Id")
                        cid = cid_variant.value if hasattr(cid_variant, "value") else cid_variant
                        # Jeśli to Wi-Fi, ale nie mamy SSID, to prawdopodobnie "Wi-Fi connection 1"
                        # Wtedy spróbujemy to nadpisać jeśli con_type == wireless w przyszłości
                        current_ssid = str(cid)

                    # Jeśli znaleźliśmy cokolwiek i to jest typ wireless, przerywamy szukanie
                    if con_type == "802-11-wireless" or found_real_ssid:
                        break

                except Exception as e:
                    print(f"[NM LOG] Error checking active connection {ac_path}: {e}")
                    continue

            previous = self.current_network
            self.current_network = current_ssid
            
            if previous != self.current_network:
                print(f"[NM LOG] Connection changed: {self.current_network}")
                self.connection_changed.emit(self.current_network or "")
            
            return self.current_network

        except Exception as e:
            print("[NM LOG] async_update_current_connection error:", e)
            return None

    async def _async_connect(self, ssid: str, password: str | None = None) -> bool:
        print(f"[NM LOG] _async_connect called for SSID: {ssid}")
        try:
            nm_intro = await self._bus.introspect(self.NM_BUS_NAME, self.NM_PATH)
            nm_obj = self._bus.get_proxy_object(self.NM_BUS_NAME, self.NM_PATH, nm_intro)
            nm_iface = nm_obj.get_interface(self.NM_BUS_NAME)
            settings = {
                "connection": {"id": ssid, "type": "802-11-wireless"},
                "802-11-wireless": {"ssid": Variant("ay", ssid.encode()), "mode": "infrastructure"},
                "ipv4": {"method": "auto"},
                "ipv6": {"method": "ignore"}
            }
            if password:
                settings["802-11-wireless-security"] = {"key-mgmt": "wpa-psk", "psk": password}
            try:
                await nm_iface.call_add_and_activate_connection(settings, "/", "/")
            except Exception:
                try:
                    await nm_iface.call_activate_connection(settings, "/", "/")
                except Exception:
                    pass
            await asyncio.sleep(1.0)
            await self._async_update_current_connection()
            return self.current_network == ssid
        except Exception as e:
            print("[NM LOG] async_connect error:", e)
            return False

    def stop(self):
        self._running = False
        try:
            if self._loop and self._loop.is_running():
                print("[NM LOG] Stopping asyncio loop")
                self._loop.call_soon_threadsafe(self._loop.stop)
        except Exception:
            pass
