import subprocess
import platform
import time
import re
from typing import List, Dict


class NetworkManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.current_network = None
        self.scanning = False
        self.connection_callbacks = []
        self.mock = self.config.get("use_mock_data", False)

        print(f"NetworkManager initialized (mock mode: {self.mock})")

    def scan_networks(self) -> List[Dict]:
        print(
            f"Scanning networks... (Platform: {platform.system()}, Mock: {self.mock})")
        self.scanning = True

        try:
            if self.mock:
                print("Using mock data")
                networks = self._get_sample_networks()
            elif platform.system() == "Windows":
                print("Scanning Windows networks...")
                networks = self._scan_windows()
            elif platform.system() == "Linux":
                print("Scanning Linux networks...")
                networks = self._scan_linux()
            elif platform.system() == "Darwin":
                print("Scanning macOS networks...")
                networks = self._scan_macos()
            else:
                print(f"Unsupported platform, using mock data")
                networks = self._get_sample_networks()

            self._update_current_connection()
            print(f"Scan complete: found {len(networks)} networks")

            for net in networks:
                print(
                    f"  - {net['ssid']}: {net['strength']}% {'(CONNECTED)' if net['connected'] else ''}")

            return networks

        except Exception as e:
            print(f"Error during scan: {e}")
            import traceback
            traceback.print_exc()
            return self._get_sample_networks()
        finally:
            self.scanning = False

    def _scan_linux(self) -> List[Dict]:
        """Scan networks on Linux using nmcli or iwlist"""
        try:
            print("Trying nmcli...")
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY,ACTIVE',
                    'dev', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                print(f"nmcli output: {result.stdout[:500]}")
                return self._parse_nmcli_output(result.stdout)

            # Try iwlist as fallback
            print("Trying iwlist...")
            result = subprocess.run(
                ['iwlist', 'scanning'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                print(f"iwlist output: {result.stdout[:500]}")
                return self._parse_iwlist_output(result.stdout)

            print("No Linux tools available, using mock data")
            return self._get_sample_networks()

        except FileNotFoundError as e:
            print(f"Command not found: {e}")
            return self._get_sample_networks()
        except Exception as e:
            print(f"Linux scan error: {type(e).__name__}: {e}")
            return self._get_sample_networks()

    def _parse_nmcli_output(self, output: str) -> List[Dict]:
        """Parse nmcli output"""
        networks = []
        lines = output.strip().split('\n')

        for line in lines:
            parts = line.split(':')
            if len(parts) >= 3:
                ssid = parts[0].strip()
                if not ssid or ssid == '--':
                    continue

                try:
                    signal = int(parts[1].strip())
                except ValueError:
                    signal = 50

                security = parts[2].strip()
                is_active = len(parts) > 3 and parts[3].strip() == 'yes'

                networks.append({
                    'ssid': ssid,
                    'strength': signal,
                    'secured': security != '' and security != '--',
                    'connected': is_active,
                    'band': '2.4GHz',
                    'frequency': 2412
                })

        return networks if networks else self._get_sample_networks()

    def _parse_iwlist_output(self, output: str) -> List[Dict]:
        """Parse iwlist output"""
        networks = []
        current_network = {}

        for line in output.split('\n'):
            line = line.strip()

            if 'ESSID:' in line:
                if current_network.get('ssid'):
                    networks.append(current_network.copy())

                ssid = line.split('ESSID:')[1].strip('"')
                if ssid:
                    current_network = {
                        'ssid': ssid,
                        'strength': 50,
                        'secured': False,
                        'connected': False,
                        'band': '2.4GHz',
                        'frequency': 2412
                    }

            elif 'Quality=' in line and current_network.get('ssid'):
                match = re.search(r'Quality=(\d+)/(\d+)', line)
                if match:
                    quality = int(match.group(1))
                    max_quality = int(match.group(2))
                    current_network['strength'] = int(
                        (quality / max_quality) * 100)

            elif 'Encryption key:' in line and current_network.get('ssid'):
                if 'on' in line.lower():
                    current_network['secured'] = True

        if current_network.get('ssid'):
            networks.append(current_network)

        return networks if networks else self._get_sample_networks()

    def _scan_macos(self) -> List[Dict]:
        """Scan networks on macOS"""
        try:
            result = subprocess.run(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return self._parse_macos_output(result.stdout)

            return self._get_sample_networks()
        except Exception as e:
            print(f"macOS scan error: {e}")
            return self._get_sample_networks()

    def _parse_macos_output(self, output: str) -> List[Dict]:
        """Parse macOS airport output"""
        networks = []
        lines = output.split('\n')[1:]  # Skip header

        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                ssid = parts[0]
                try:
                    signal = int(parts[2])
                    # Convert dBm to percentage
                    signal = min(100, max(0, signal + 100))
                except ValueError:
                    signal = 50

                networks.append({
                    'ssid': ssid,
                    'strength': signal,
                    'secured': 'WPA' in line or 'WEP' in line,
                    'connected': False,
                    'band': '2.4GHz',
                    'frequency': 2412
                })

        return networks if networks else self._get_sample_networks()

    def _scan_windows(self) -> List[Dict]:
        """Scan networks on Windows using netsh"""
        try:
            print("Running: netsh wlan show networks mode=bssid")

            # Use chcp to ensure proper encoding handling
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                capture_output=True,
                text=True,
                timeout=15,
                encoding='cp1252',  # Windows default code page
                errors='replace'
            )

            if result.returncode != 0:
                print(f"netsh command failed with code {result.returncode}")
                print(f"stderr: {result.stderr}")
                return self._get_sample_networks()

            print(f"Raw output length: {len(result.stdout)} chars")
            networks = self._parse_windows_output(result.stdout)
            return networks if networks else self._get_sample_networks()

        except subprocess.TimeoutExpired:
            print("Windows scan timed out")
            return self._get_sample_networks()
        except Exception as e:
            print(f"Windows scan error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return self._get_sample_networks()

    def _parse_windows_output(self, output: str) -> List[Dict]:
        """Parse Windows netsh output with improved robustness"""
        networks = []
        lines = output.split('\n')
        current_network = {}

        print(f"Parsing {len(lines)} lines of Windows output")

        for i, line in enumerate(lines):
            line = line.strip()

            # Detect SSID line (avoid BSSID)
            if line.startswith('SSID') and ':' in line and 'BSSID' not in line:
                # Save previous network if exists
                if current_network.get('ssid'):
                    if not any(n['ssid'] == current_network['ssid'] for n in networks):
                        networks.append(current_network.copy())
                        print(f"Added network: {current_network['ssid']}")

                # Extract SSID
                parts = line.split(':', 1)
                if len(parts) == 2:
                    ssid = parts[1].strip()

                    # Skip empty SSIDs
                    if ssid and ssid != '':
                        current_network = {
                            'ssid': ssid,
                            'strength': 50,  # Default value
                            'secured': True,  # Assume secured by default
                            'connected': False,
                            'band': '2.4GHz',
                            'frequency': 2412
                        }
                        print(f"Found SSID: {ssid}")

            # Check for authentication type
            elif 'Authentication' in line and current_network.get('ssid'):
                current_network['secured'] = 'Open' not in line
                print(
                    f"  Auth: {'Secured' if current_network['secured'] else 'Open'}")

            # Extract signal strength
            elif 'Signal' in line and ':' in line and current_network.get('ssid'):
                try:
                    signal_str = line.split(':', 1)[1].strip()
                    # Remove '%' and any extra whitespace
                    signal_str = signal_str.replace('%', '').strip()
                    signal = int(signal_str)
                    current_network['strength'] = signal
                    print(f"  Signal: {signal}%")
                except (ValueError, IndexError) as e:
                    print(f"  Could not parse signal from: '{line}' - {e}")

            # Detect band/frequency from radio type
            elif 'Radio type' in line and current_network.get('ssid'):
                line_lower = line.lower()
                if '802.11a' in line_lower or '802.11ac' in line_lower or '802.11ax' in line_lower or '5' in line_lower:
                    current_network['band'] = '5GHz'
                    current_network['frequency'] = 5180
                    print(f"  Band: 5GHz")
                else:
                    print(f"  Band: 2.4GHz")

        # Don't forget the last network
        if current_network.get('ssid'):
            if not any(n['ssid'] == current_network['ssid'] for n in networks):
                networks.append(current_network)
                print(f"Added final network: {current_network['ssid']}")

        # Check connection status for all networks
        print("Checking connection status...")
        for network in networks:
            network['connected'] = self._is_connected_windows(network['ssid'])

        # Sort by signal strength
        networks.sort(key=lambda x: x['strength'], reverse=True)

        print(f"Total networks found: {len(networks)}")
        return networks

    def _is_connected_windows(self, ssid: str) -> bool:
        """Check if currently connected to specific SSID on Windows"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='cp1252',
                errors='replace'
            )

            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line and ':' in line:
                        connected_ssid = line.split(':', 1)[1].strip()
                        if connected_ssid == ssid:
                            print(f"  Connected to: {ssid}")
                            return True
            return False
        except Exception as e:
            print(f"Error checking connection status: {e}")
            return False

    def connect_to_network(self, ssid: str, password: str = None) -> bool:
        """Connect to a Wi-Fi network"""
        print(f"Connecting to {ssid}...")
        try:
            if self.mock:
                time.sleep(1)
                self.current_network = ssid
                self._notify_callbacks(True, ssid)
                return True

            if platform.system() == "Windows":
                success = self._connect_windows(ssid, password)
                if success:
                    self._notify_callbacks(True, ssid)
                return success
            elif platform.system() == "Linux":
                success = self._connect_linux(ssid, password)
                if success:
                    self._notify_callbacks(True, ssid)
                return success
            else:
                time.sleep(2)
                self.current_network = ssid
                self._notify_callbacks(True, ssid)
                return True

        except Exception as e:
            print(f"Connection error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _connect_linux(self, ssid: str, password: str = None) -> bool:
        """Connect to network on Linux using nmcli"""
        try:
            if password:
                cmd = ['nmcli', 'dev', 'wifi', 'connect',
                       ssid, 'password', password]
            else:
                cmd = ['nmcli', 'dev', 'wifi', 'connect', ssid]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.current_network = ssid
                return True

            print(f"Connection failed: {result.stderr}")
            return False
        except Exception as e:
            print(f"Linux connection error: {e}")
            return False

    def _connect_windows(self, ssid: str, password: str = None) -> bool:
        """Connect to network on Windows with improved error handling"""
        try:
            # First, try to connect to existing profile
            print(f"Attempting to connect to existing profile: {ssid}")
            result = subprocess.run(
                ['netsh', 'wlan', 'connect', f'name={ssid}'],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='cp1252',
                errors='replace'
            )

            if result.returncode == 0 or "Connection request was completed successfully" in result.stdout:
                print("Connected successfully using existing profile")
                time.sleep(2)  # Wait for connection to establish
                self.current_network = ssid
                return True

            # If password provided and connection failed, try creating new profile
            if password:
                print(f"Creating new profile for: {ssid}")
                return self._create_windows_profile(ssid, password)

            print(f"Connection failed: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return False

        except subprocess.TimeoutExpired:
            print("Connection attempt timed out")
            return False
        except Exception as e:
            print(f"Windows connection error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _create_windows_profile(self, ssid: str, password: str) -> bool:
        """Create a new Windows Wi-Fi profile and connect"""
        try:
            # Create XML profile
            profile_xml = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''

            # Save profile to temp file
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8') as f:
                f.write(profile_xml)
                profile_path = f.name

            try:
                # Add profile
                print(f"Adding Wi-Fi profile from: {profile_path}")
                result = subprocess.run(
                    ['netsh', 'wlan', 'add', 'profile',
                        f'filename={profile_path}'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='cp1252',
                    errors='replace'
                )

                print(f"Add profile result: {result.stdout}")

                if result.returncode != 0:
                    print(f"Failed to add profile: {result.stderr}")
                    return False

                # Now connect
                time.sleep(1)
                result = subprocess.run(
                    ['netsh', 'wlan', 'connect', f'name={ssid}'],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='cp1252',
                    errors='replace'
                )

                if result.returncode == 0 or "Connection request was completed successfully" in result.stdout:
                    print("Connected successfully with new profile")
                    time.sleep(2)
                    self.current_network = ssid
                    return True

                print(f"Connect failed: {result.stdout}")
                return False

            finally:
                # Clean up temp file
                try:
                    os.unlink(profile_path)
                except:
                    pass

        except Exception as e:
            print(f"Error creating profile: {e}")
            import traceback
            traceback.print_exc()
            return False

    def disconnect(self) -> bool:
        """Disconnect from current network"""
        try:
            if self.mock:
                self.current_network = None
                return True

            if platform.system() == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'disconnect'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    self.current_network = None
                    print("Disconnected successfully")
                    return True
                else:
                    print(f"Disconnect failed: {result.stderr}")
                    return False
            elif platform.system() == "Linux":
                result = subprocess.run(
                    ['nmcli', 'dev', 'disconnect', 'wlan0'], capture_output=True)
                if result.returncode == 0:
                    self.current_network = None
                    return True
            return False
        except Exception as e:
            print(f"Disconnect error: {e}")
            return False

    def get_saved_networks(self) -> List[str]:
        """Get list of saved network profiles"""
        try:
            if self.mock:
                return list(self.config.get('saved_networks', {}).keys())

            if platform.system() == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profiles'],
                    capture_output=True,
                    text=True,
                    encoding='cp1252',
                    errors='replace'
                )

                if result.returncode == 0:
                    profiles = []
                    for line in result.stdout.split('\n'):
                        if 'All User Profile' in line or 'User Profile' in line:
                            # Extract profile name after the colon
                            if ':' in line:
                                profile = line.split(':', 1)[1].strip()
                                if profile:
                                    profiles.append(profile)
                    return profiles

            return list(self.config.get('saved_networks', {}).keys())
        except Exception as e:
            print(f"Error getting saved networks: {e}")
            return []

    def forget_network(self, ssid: str) -> bool:
        """Remove a saved network profile"""
        try:
            self.config.remove_saved_network(ssid)

            if not self.mock and platform.system() == "Windows":
                print(f"Deleting Windows profile: {ssid}")
                result = subprocess.run(
                    ['netsh', 'wlan', 'delete', 'profile', f'name={ssid}'],
                    capture_output=True,
                    text=True,
                    encoding='cp1252',
                    errors='replace'
                )
                if result.returncode == 0:
                    print(f"Profile deleted: {ssid}")
                    return True
                else:
                    print(f"Failed to delete profile: {result.stderr}")
                    return False
            elif not self.mock and platform.system() == "Linux":
                subprocess.run(['nmcli', 'connection', 'delete', ssid])

            return True
        except Exception as e:
            print(f"Error forgetting network: {e}")
            return False

    def _update_current_connection(self):
        """Update the current network connection status"""
        if self.mock:
            return

        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'interfaces'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    encoding='cp1252',
                    errors='replace'
                )

                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'SSID' in line and 'BSSID' not in line and ':' in line:
                            self.current_network = line.split(':', 1)[
                                1].strip()
                            print(
                                f"Current connection: {self.current_network}")
                            break

            elif platform.system() == "Linux":
                result = subprocess.run(
                    ['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.startswith('yes:'):
                            self.current_network = line.split(':', 1)[
                                1].strip()
                            break
        except Exception as e:
            print(f"Error updating connection status: {e}")

    def add_connection_callback(self, callback):
        """Add a callback function to be called on connection events"""
        self.connection_callbacks.append(callback)

    def _notify_callbacks(self, success: bool, ssid: str):
        """Notify all registered callbacks about connection events"""
        for callback in self.connection_callbacks:
            try:
                callback(success, ssid)
            except Exception as e:
                print(f"Error in connection callback: {e}")

    def _get_sample_networks(self):
        """Generate mock network data for testing"""
        print("Generating mock network data")
        return [
            {
                "ssid": "🏠 Home_WiFi_5G",
                "strength": 92,
                "secured": True,
                "connected": False,
                "band": "5GHz",
                "frequency": 5180
            },
            {
                "ssid": "🏠 Home_WiFi_2.4G",
                "strength": 85,
                "secured": True,
                "connected": False,
                "band": "2.4GHz",
                "frequency": 2412
            },
            {
                "ssid": "☕ CoffeeShop_Guest",
                "strength": 67,
                "secured": False,
                "connected": False,
                "band": "2.4GHz",
                "frequency": 2437
            },
            {
                "ssid": "🏢 Office_Network",
                "strength": 58,
                "secured": True,
                "connected": False,
                "band": "5GHz",
                "frequency": 5180
            },
            {
                "ssid": "👤 Neighbor_Network",
                "strength": 45,
                "secured": True,
                "connected": False,
                "band": "2.4GHz",
                "frequency": 2462
            },
            {
                "ssid": "📱 MyPhone_Hotspot",
                "strength": 40,
                "secured": True,
                "connected": False,
                "band": "2.4GHz",
                "frequency": 2437
            },
        ]
