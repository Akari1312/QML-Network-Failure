# quantum_client.py - Enhanced Client with Attack Simulation (FIXED)
import requests
import random
import time
import threading
from datetime import datetime

class QuantumNetworkClient:
    def __init__(self, attack_simulator, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.running = False
        self.update_interval = 5
        self.failed_attempts = 0
        self.max_failed_attempts = 3
        self.attack_simulator = attack_simulator
        self.client_thread = None
        
        print(f"🔗 [CLIENT] Initialized with server: {self.server_url}")
    
    def generate_random_data(self):
        """Generate 5 entries with random data"""
        data = []
        for i in range(1, 6):
            data.append({
                'id': i,
                'random_value': round(random.uniform(0, 100), 2),
                'client_timestamp': datetime.now().isoformat()
            })
        return data
    
    def send_update(self):
        """Send update to server"""
        try:
            data = self.generate_random_data()
            
            response = requests.post(
                f"{self.server_url}/update",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ [CLIENT] Update successful at {datetime.now().strftime('%H:%M:%S')}")
                self.failed_attempts = 0
                return True
            else:
                print(f"❌ [CLIENT] Server returned {response.status_code}")
                self.failed_attempts += 1
                return False
                
        except requests.exceptions.Timeout:
            print(f"⏰ [CLIENT] Request timeout")
            self.failed_attempts += 1
            return False
        except requests.exceptions.ConnectionError:
            print(f"🔌 [CLIENT] Connection error - server may be down")
            self.failed_attempts += 1
            return False
        except Exception as e:
            print(f"💥 [CLIENT] Error: {e}")
            self.failed_attempts += 1
            return False
    
    def start(self):
        """Start the client"""
        if not self.running:
            self.running = True
            self.failed_attempts = 0
            print("🔄 [CLIENT] Starting...")
            
            # Start client loop in a separate thread
            self.client_thread = threading.Thread(target=self.run_loop, daemon=True)
            self.client_thread.start()
        else:
            print("⚠️  [CLIENT] Already running")
    
    def stop(self):
        """Stop the client"""
        if self.running:
            self.running = False
            if self.attack_simulator:
                self.attack_simulator.stop_attack()
            print("🛑 [CLIENT] Stopped")
        else:
            print("⚠️  [CLIENT] Already stopped")
    
    def is_running(self):
        """Check if client is running"""
        return self.running
    
    def get_status(self):
        """Get client status"""
        return {
            'running': self.running,
            'failed_attempts': self.failed_attempts,
            'server_url': self.server_url,
            'update_interval': self.update_interval,
            'attack_active': self.attack_simulator.attack_active if self.attack_simulator else False,
            'attack_type': self.attack_simulator.attack_type if self.attack_simulator else None
        }
    
    def run_loop(self):
        """Client update loop with attack simulation"""
        print("🔄 [CLIENT] Starting update loop...")
        
        while self.running:
            # Check if we should continue running
            if self.failed_attempts >= self.max_failed_attempts:
                print(f"❌ [CLIENT] Too many failed attempts ({self.failed_attempts}), stopping...")
                self.running = False
                break
            
            # Send update to server
            self.send_update()
            
            # Determine sleep interval based on attack simulation
            sleep_interval = self.get_sleep_interval()
            
            # Sleep with periodic checks for stop signal
            start_time = time.time()
            while (time.time() - start_time) < sleep_interval and self.running:
                time.sleep(0.5)  # Check every 0.5 seconds if we should stop
        
        print("🛑 [CLIENT] Update loop stopped")
    
    def get_sleep_interval(self):
        """Get sleep interval based on attack simulation"""
        if not self.attack_simulator:
            return self.update_interval
        
        # Check for attack timing override
        timing_override = self.attack_simulator.get_timing_override()
        
        if timing_override == 'dos_active':
            # DoS attack thread handles timing, use shorter check interval
            return 1.0
        elif timing_override is not None:
            # Use attack-specific timing
            return timing_override
        else:
            # Normal timing
            return self.update_interval
    
    def test_connection(self):
        """Test connection to server"""
        try:
            response = requests.get(f"{self.server_url}/status", timeout=5)
            if response.status_code == 200:
                print("✅ [CLIENT] Server connection test successful")
                return True
            else:
                print(f"❌ [CLIENT] Server returned {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ [CLIENT] Connection test failed: {e}")
            return False
    
    def set_update_interval(self, interval):
        """Set update interval (in seconds)"""
        if interval > 0:
            self.update_interval = interval
            print(f"⏱️  [CLIENT] Update interval set to {interval} seconds")
        else:
            print("❌ [CLIENT] Invalid interval, must be > 0")
    
    def reset_failed_attempts(self):
        """Reset failed attempts counter"""
        self.failed_attempts = 0
        print("🔄 [CLIENT] Failed attempts counter reset")


# Standalone testing function
def test_quantum_client():
    """Test the quantum client standalone"""
    print("🧪 Testing Quantum Network Client...")
    
    # Create a mock attack simulator for testing
    class MockAttackSimulator:
        def __init__(self):
            self.attack_active = False
            self.attack_type = None
        
        def get_timing_override(self):
            return None
        
        def stop_attack(self):
            self.attack_active = False
    
    # Create client with mock simulator
    mock_simulator = MockAttackSimulator()
    client = QuantumNetworkClient(mock_simulator)
    
    # Test connection
    print("\n1. Testing server connection...")
    if client.test_connection():
        print("✅ Server is reachable")
    else:
        print("❌ Server is not reachable - make sure server is running")
        return
    
    # Test single update
    print("\n2. Testing single update...")
    success = client.send_update()
    if success:
        print("✅ Single update successful")
    else:
        print("❌ Single update failed")
    
    # Test client status
    print("\n3. Testing client status...")
    status = client.get_status()
    print(f"Status: {status}")
    
    # Test start/stop
    print("\n4. Testing start/stop functionality...")
    client.start()
    time.sleep(3)  # Let it run for a few seconds
    client.stop()
    
    print("✅ Client test completed")


if __name__ == '__main__':
    # Run standalone test
    test_quantum_client()