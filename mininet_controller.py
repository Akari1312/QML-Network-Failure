# mininet_controller.py - Integration layer between Mininet and Quantum Monitor
import subprocess
import threading
import time
import requests
import json
from datetime import datetime

class MininetQuantumController:
    def __init__(self):
        self.mininet_process = None
        self.monitoring_active = False
        self.network_stats = {}
        
    def start_mininet_topology(self):
        """Start the Mininet topology in background"""
        print("🌐 Starting Mininet topology...")
        
        try:
            # Start Mininet topology
            self.mininet_process = subprocess.Popen(
                ['sudo', 'python3', 'mininet_topology.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            time.sleep(5)  # Give topology time to start
            
            if self.mininet_process.poll() is None:
                print("✅ Mininet topology started successfully")
                return True
            else:
                print("❌ Failed to start Mininet topology")
                return False
                
        except Exception as e:
            print(f"❌ Error starting Mininet: {e}")
            return False
    
    def send_mininet_command(self, command):
        """Send command to Mininet topology"""
        try:
            if self.mininet_process and self.mininet_process.poll() is None:
                self.mininet_process.stdin.write(f"{command}\n")
                self.mininet_process.stdin.flush()
                return True
        except Exception as e:
            print(f"❌ Error sending command to Mininet: {e}")
        return False
    
    def apply_network_attack(self, attack_type):
        """Apply network attack simulation via Mininet"""
        print(f"🚨 Applying {attack_type} attack via Mininet...")
        
        # Commands to send to Mininet CLI
        attack_commands = {
            'dos': 'dos',
            'flooding': 'flooding', 
            'congestion': 'congestion',
            'normal': 'normal'
        }
        
        if attack_type in attack_commands:
            return self.send_mininet_command(attack_commands[attack_type])
        return False
    
    def get_network_statistics(self):
        """Get network statistics from Mininet hosts"""
        try:
            # This would typically query Mininet for real network stats
            # For now, we'll simulate the data
            return {
                'server_host': {
                    'ip': '10.0.0.1',
                    'status': 'active',
                    'packets_sent': 1250,
                    'packets_received': 1180
                },
                'client_host': {
                    'ip': '10.0.0.2', 
                    'status': 'active',
                    'packets_sent': 1180,
                    'packets_received': 1150
                },
                'link_status': {
                    'bandwidth': '100Mbps',
                    'latency': '5ms',
                    'packet_loss': '0%'
                }
            }
        except Exception as e:
            print(f"❌ Error getting network stats: {e}")
            return {}
    
    def monitor_network_health(self):
        """Monitor network health and performance"""
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                stats = self.get_network_statistics()
                self.network_stats = stats
                
                # You could add network health checks here
                # For example, detecting high latency or packet loss
                
                time.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                print(f"❌ Error in network monitoring: {e}")
                time.sleep(5)
    
    def start_monitoring(self):
        """Start network monitoring in background thread"""
        monitor_thread = threading.Thread(target=self.monitor_network_health)
        monitor_thread.daemon = True
        monitor_thread.start()
        print("📊 Network monitoring started")
    
    def stop_mininet(self):
        """Stop Mininet topology"""
        print("🛑 Stopping Mininet topology...")
        
        self.monitoring_active = False
        
        if self.mininet_process:
            try:
                # Send exit command
                self.send_mininet_command('exit')
                
                # Wait for process to terminate
                self.mininet_process.wait(timeout=10)
                
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't stop gracefully
                self.mininet_process.terminate()
                self.mininet_process.wait(timeout=5)
                
            except Exception as e:
                print(f"Error stopping Mininet: {e}")
        
        # Clean up any remaining Mininet processes
        try:
            subprocess.run(['sudo', 'mn', '-c'], check=False, capture_output=True)
        except:
            pass
        
        print("✅ Mininet stopped")

# Integration functions for the main quantum app
def integrate_with_quantum_app():
    """Integration functions to add to the main quantum app"""
    
    # This would be added to the main Flask app
    mininet_controller = MininetQuantumController()
    
    def enhanced_attack_simulation(attack_type):
        """Enhanced attack simulation using Mininet"""
        print(f"🌐 Applying {attack_type} via Mininet network simulation")
        
        # Apply Mininet network conditions
        mininet_controller.apply_network_attack(attack_type)
        
        # Also apply application-level attack simulation
        # (your existing attack_simulator code)
        
        return True
    
    def get_enhanced_network_status():
        """Get enhanced network status including Mininet stats"""
        # Combine quantum analysis with Mininet network stats
        network_stats = mininet_controller.get_network_statistics()
        
        return {
            'mininet_stats': network_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    return {
        'controller': mininet_controller,
        'enhanced_attack': enhanced_attack_simulation,
        'enhanced_status': get_enhanced_network_status
    }

# Standalone testing
if __name__ == '__main__':
    print("🧪 Testing Mininet integration...")
    
    controller = MininetQuantumController()
    
    try:
        # Start topology
        if controller.start_mininet_topology():
            print("✅ Topology started")
            
            # Start monitoring
            controller.start_monitoring()
            
            # Test different attacks
            attacks = ['normal', 'dos', 'flooding', 'congestion', 'normal']
            
            for attack in attacks:
                print(f"\n🧪 Testing {attack} attack...")
                controller.apply_network_attack(attack)
                
                # Monitor for 30 seconds
                for i in range(6):
                    stats = controller.get_network_statistics()
                    print(f"📊 Network stats: {stats}")
                    time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    finally:
        controller.stop_mininet()