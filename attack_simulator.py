# attack_simulator.py - Network Attack Simulations
import threading
import time
import random

class NetworkAttackSimulator:
    def __init__(self, client):
        self.client = client
        self.attack_active = False
        self.attack_type = None
        self.attack_thread = None
    
    def start_dos_attack(self):
        """Simulate DoS attack with connection timeouts"""
        self.stop_attack()  # Stop any existing attack
        self.attack_type = 'dos'
        self.attack_active = True
        self.attack_thread = threading.Thread(target=self._dos_attack_pattern)
        self.attack_thread.daemon = True
        self.attack_thread.start()
        print("🚨 DoS Attack simulation started")
    
    def start_flooding_attack(self):
        """Simulate connection flooding attack"""
        self.stop_attack()
        self.attack_type = 'flooding'
        self.attack_active = True
        self.attack_thread = threading.Thread(target=self._flooding_attack_pattern)
        self.attack_thread.daemon = True
        self.attack_thread.start()
        print("🚨 Connection Flooding simulation started")
    
    def start_congestion_attack(self):
        """Simulate network congestion"""
        self.stop_attack()
        self.attack_type = 'congestion'
        self.attack_active = True
        self.attack_thread = threading.Thread(target=self._congestion_attack_pattern)
        self.attack_thread.daemon = True
        self.attack_thread.start()
        print("🚨 Network Congestion simulation started")
    
    def stop_attack(self):
        """Stop current attack simulation"""
        if self.attack_active:
            self.attack_active = False
            self.attack_type = None
            print("✅ Attack simulation stopped")
    
    def _dos_attack_pattern(self):
        """DoS attack pattern - random long delays"""
        while self.attack_active and self.client.running:
            if random.random() < 0.3:  # 30% chance of timeout
                print("💥 [ATTACK] DoS timeout simulation...")
                time.sleep(random.uniform(15, 25))
            else:
                time.sleep(random.uniform(4, 6))
    
    def _flooding_attack_pattern(self):
        """Flooding attack pattern - very rapid requests"""
        while self.attack_active and self.client.running:
            print("🌊 [ATTACK] Flooding rapid requests...")
            time.sleep(random.uniform(0.5, 2.0))
    
    def _congestion_attack_pattern(self):
        """Congestion pattern - gradually increasing delays"""
        base_delay = 5.0
        while self.attack_active and self.client.running:
            print(f"🚦 [ATTACK] Congestion delay: {base_delay:.1f}s...")
            time.sleep(base_delay + random.uniform(0, 5))
            base_delay = min(base_delay * 1.1, 15.0)  # Gradually increase
    
    def get_timing_override(self):
        """Get current attack timing override"""
        if not self.attack_active:
            return None
        
        if self.attack_type == 'dos':
            # DoS handled by attack thread
            return 'dos_active'
        elif self.attack_type == 'flooding':
            return random.uniform(0.5, 2.0)
        elif self.attack_type == 'congestion':
            return random.uniform(7, 12)
        
        return None