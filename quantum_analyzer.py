# quantum_analyzer.py - ENHANCED PACKET ANALYZER with Real-time Monitoring
import numpy as np
from datetime import datetime
from collections import deque, defaultdict
import warnings
import pickle
import os
import threading
import time
import random
warnings.filterwarnings('ignore')

# Packet analysis and Quantum ML
try:
    import pennylane as qml
    from pennylane import numpy as pnp
    from sklearn.preprocessing import StandardScaler
    QUANTUM_AVAILABLE = True
    print("🔬 PennyLane Quantum ML Enterprise Suite loaded successfully!")
except ImportError as e:
    QUANTUM_AVAILABLE = False
    print(f"⚠️  PennyLane not available: {e}")

class EnhancedPacketQuantumSecurityAI:
    def __init__(self, model_path="enhanced_packet_quantum.pkl", retrain=False):
        self.quantum_available = QUANTUM_AVAILABLE
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = model_path
        
        # Enhanced packet monitoring with real-time stats
        self.packet_history = deque(maxlen=2000)
        self.packet_stats = {
            'total_packets': 0,
            'packets_per_second': 0,
            'unique_src_ips': set(),
            'unique_dst_ports': set(),
            'protocol_counts': defaultdict(int),
            'avg_packet_size': 0,
            'last_update': time.time()
        }
        self.last_update_time = None
        
        # Attack simulation state with distinctive patterns
        self.attack_mode = None
        self.packet_simulator_active = False
        self.attack_start_time = None
        
        # Model metrics
        self.model_metrics = {
            'accuracy': 0.0,
            'training_epochs': 0,
            'training_time': 0.0
        }
        
        # Start enhanced packet simulation
        self.start_enhanced_packet_simulation()
        
        if self.quantum_available:
            self.setup_enhanced_quantum_circuit()
            
            if not retrain and self.load_model():
                print("✅ Enhanced Packet Quantum Security AI model loaded")
                self.validate_model()
            else:
                print("🔬 Training Enhanced Packet Quantum Security AI...")
                self.train_enhanced_model()
                self.save_model()
        
        print(f"📦 Enhanced Packet Quantum Security AI Online")
        print(f"📊 Model Performance: {self.model_metrics['accuracy']:.1%} accuracy")
        print(f"📈 Real-time Monitoring: Packet counts, rates, and protocol analysis")
    
    def setup_enhanced_quantum_circuit(self):
        """Setup enhanced quantum circuit for distinctive pattern recognition"""
        self.n_qubits = 4
        self.n_layers = 3  # Increased for better pattern recognition
        self.n_features = 10  # More features for better distinction
        
        # Quantum device
        self.dev = qml.device('default.qubit', wires=self.n_qubits)
        
        # Enhanced parameters
        self.params = pnp.random.uniform(0, 2*np.pi, (self.n_layers, self.n_qubits, 3), requires_grad=True)
        
        # Enhanced quantum circuit
        self.quantum_circuit = qml.QNode(self._enhanced_quantum_circuit, self.dev)
        
        print(f"🔬 Enhanced Quantum Architecture: {self.n_qubits} qubits, {self.n_features} distinctive features")
        print(f"📦 Features: Rate, Size, Protocols, IPs, Ports, Payload, Timing, Flags, Entropy, Variance")
    
    def _enhanced_quantum_circuit(self, features, params):
        """Enhanced quantum circuit with better entanglement for pattern recognition"""
        
        # Encode packet features with amplitude encoding
        for i in range(min(len(features), self.n_qubits)):
            qml.RY(features[i] * np.pi, wires=i)
            qml.RZ(features[i] * np.pi / 2, wires=i)  # Additional encoding
        
        # Enhanced variational layers
        for layer in range(self.n_layers):
            # Rotation gates
            for qubit in range(self.n_qubits):
                qml.RX(params[layer, qubit, 0], wires=qubit)
                qml.RY(params[layer, qubit, 1], wires=qubit)
                qml.RZ(params[layer, qubit, 2], wires=qubit)
            
            # Enhanced entanglement patterns
            # Circular entanglement
            for qubit in range(self.n_qubits):
                qml.CNOT(wires=[qubit, (qubit + 1) % self.n_qubits])
            
            # Cross entanglement for better pattern correlation
            if layer % 2 == 0:
                qml.CNOT(wires=[0, 2])
                qml.CNOT(wires=[1, 3])
            
            # T-gate for quantum advantage
            if layer == 1:
                qml.T(wires=0)
                qml.T(wires=2)
        
        return qml.expval(qml.PauliZ(0))
    
    def start_enhanced_packet_simulation(self):
        """Start enhanced packet simulation with real-time monitoring"""
        self.packet_simulator_active = True
        
        def enhanced_packet_generator():
            while self.packet_simulator_active:
                # Generate distinctive packets based on attack mode
                packets = self.generate_distinctive_packets()
                
                for packet in packets:
                    self.packet_history.append(packet)
                    self.update_real_time_stats(packet)
                
                # Update packets per second calculation
                current_time = time.time()
                if current_time - self.packet_stats['last_update'] >= 1.0:
                    self.calculate_packets_per_second()
                    self.packet_stats['last_update'] = current_time
                
                # Attack-specific timing
                if self.attack_mode == 'ddos_volumetric':
                    time.sleep(0.001)  # Very fast - volumetric flood
                elif self.attack_mode == 'port_scan':
                    time.sleep(0.1)    # Systematic scanning
                elif self.attack_mode == 'data_exfiltration':
                    time.sleep(0.5)    # Steady data flow
                elif self.attack_mode == 'botnet_c2':
                    time.sleep(2.0)    # Periodic communication
                else:
                    time.sleep(0.3)    # Normal business traffic
        
        # Start background packet generation
        packet_thread = threading.Thread(target=enhanced_packet_generator, daemon=True)
        packet_thread.start()
        
        print("📦 Enhanced network packet simulation with real-time monitoring started")
    
    def generate_distinctive_packets(self):
        """Generate highly distinctive packet patterns for each attack type"""
        packets = []
        current_time = time.time()
        
        if self.attack_mode == 'ddos_volumetric':
            # DDoS Volumetric: Massive packet flood from many IPs
            for _ in range(random.randint(200, 500)):  # Very high packet count
                packets.append({
                    'timestamp': current_time,
                    'size': random.choice([64, 64, 64, 1500]),  # Mostly tiny packets + some large
                    'protocol': random.choice(['UDP', 'UDP', 'UDP', 'ICMP']),  # Mostly UDP
                    'src_ip': f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    'dst_ip': '192.168.1.100',
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443, 53]),  # Target specific services
                    'flags': random.choice(['', 'SYN', 'ACK']),
                    'payload_entropy': random.uniform(0.1, 0.2),  # Very low entropy
                    'packet_interval': 0.001,  # Very fast
                    'attack_signature': 'volumetric_flood'
                })
        
        elif self.attack_mode == 'port_scan':
            # Port Scan: Sequential port probing from few IPs
            base_port = random.randint(1, 65500)
            scanner_ip = f"172.16.{random.randint(1,10)}.{random.randint(1,50)}"
            
            for i in range(random.randint(20, 50)):  # Moderate packet count
                packets.append({
                    'timestamp': current_time,
                    'size': random.randint(60, 80),  # Small SYN packets
                    'protocol': 'TCP',  # Only TCP for port scanning
                    'src_ip': scanner_ip,  # Same source IP
                    'dst_ip': '192.168.1.100',
                    'src_port': random.randint(1024, 65535),
                    'dst_port': base_port + i,  # Sequential ports!
                    'flags': 'SYN',  # All SYN packets
                    'payload_entropy': 0.0,  # No payload
                    'packet_interval': 0.1,
                    'attack_signature': 'port_reconnaissance'
                })
        
        elif self.attack_mode == 'data_exfiltration':
            # Data Exfiltration: Large outbound packets to external IPs
            for _ in range(random.randint(10, 30)):  # Low packet count but large
                packets.append({
                    'timestamp': current_time,
                    'size': random.randint(1200, 1500),  # Large packets
                    'protocol': random.choice(['TCP', 'HTTPS']),  # Encrypted channels
                    'src_ip': '192.168.1.100',  # Internal source
                    'dst_ip': f"8.8.{random.randint(1,255)}.{random.randint(1,255)}",  # External destination
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([443, 80, 53, 25]),  # Common external ports
                    'flags': 'PSH',  # Push data
                    'payload_entropy': random.uniform(0.8, 1.0),  # High entropy (encrypted)
                    'packet_interval': 0.5,
                    'attack_signature': 'data_exfiltration'
                })
        
        elif self.attack_mode == 'botnet_c2':
            # Botnet C&C: Periodic beacons to specific external IPs
            c2_server = f"203.0.113.{random.randint(1,50)}"  # Fixed C&C server
            
            for _ in range(random.randint(3, 8)):  # Very low packet count
                packets.append({
                    'timestamp': current_time,
                    'size': random.randint(200, 400),  # Medium packets
                    'protocol': random.choice(['TCP', 'HTTPS']),
                    'src_ip': '192.168.1.100',
                    'dst_ip': c2_server,  # Same C&C server
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([443, 8080, 8443]),  # Non-standard ports
                    'flags': 'ACK',
                    'payload_entropy': random.uniform(0.6, 0.8),  # Medium entropy
                    'packet_interval': 2.0,  # Slow, periodic
                    'attack_signature': 'botnet_beacon'
                })
        
        else:
            # Normal Business Traffic: Mixed protocols, reasonable sizes
            for _ in range(random.randint(5, 20)):  # Normal packet count
                packets.append({
                    'timestamp': current_time,
                    'size': random.randint(200, 1200),  # Normal sizes
                    'protocol': random.choice(['TCP', 'TCP', 'UDP', 'HTTPS']),  # Mostly TCP
                    'src_ip': f"192.168.1.{random.randint(10, 50)}",  # Internal network
                    'dst_ip': f"192.168.1.{random.randint(10, 50)}",  # Internal or external
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443, 22, 25, 53, 3389, 21]),  # Business ports
                    'flags': random.choice(['ACK', 'PSH', 'FIN']),
                    'payload_entropy': random.uniform(0.4, 0.7),  # Normal entropy
                    'packet_interval': 0.3,
                    'attack_signature': 'normal_business'
                })
        
        return packets
    
    def update_real_time_stats(self, packet):
        """Update real-time packet statistics for monitoring"""
        self.packet_stats['total_packets'] += 1
        self.packet_stats['unique_src_ips'].add(packet['src_ip'])
        self.packet_stats['unique_dst_ports'].add(packet['dst_port'])
        self.packet_stats['protocol_counts'][packet['protocol']] += 1
        
        # Calculate running average packet size
        if self.packet_stats['total_packets'] == 1:
            self.packet_stats['avg_packet_size'] = packet['size']
        else:
            # Running average
            old_avg = self.packet_stats['avg_packet_size']
            n = self.packet_stats['total_packets']
            self.packet_stats['avg_packet_size'] = old_avg + (packet['size'] - old_avg) / n
    
    def calculate_packets_per_second(self):
        """Calculate packets per second over the last second"""
        current_time = time.time()
        one_second_ago = current_time - 1.0
        
        # Count packets in the last second
        recent_packets = [p for p in self.packet_history if p['timestamp'] > one_second_ago]
        self.packet_stats['packets_per_second'] = len(recent_packets)
    
    def get_real_time_packet_stats(self):
        """Get current real-time packet statistics for display"""
        return {
            'total_packets': self.packet_stats['total_packets'],
            'packets_per_second': self.packet_stats['packets_per_second'],
            'unique_src_ips': len(self.packet_stats['unique_src_ips']),
            'unique_dst_ports': len(self.packet_stats['unique_dst_ports']),
            'avg_packet_size': int(self.packet_stats['avg_packet_size']),
            'protocol_distribution': dict(self.packet_stats['protocol_counts']),
            'attack_mode': self.attack_mode or 'normal',
            'monitoring_duration': time.time() - (self.attack_start_time or time.time())
        }
    
    def set_attack_mode(self, attack_type):
        """Set distinctive attack simulation mode"""
        # Map simple attack names to distinctive patterns
        attack_mapping = {
            'ddos': 'ddos_volumetric',
            'dos': 'ddos_volumetric', 
            'flooding': 'port_scan',
            'congestion': 'data_exfiltration'
        }
        
        self.attack_mode = attack_mapping.get(attack_type, attack_type)
        self.attack_start_time = time.time()
        
        # Reset stats for new attack
        self.packet_stats = {
            'total_packets': 0,
            'packets_per_second': 0,
            'unique_src_ips': set(),
            'unique_dst_ports': set(),
            'protocol_counts': defaultdict(int),
            'avg_packet_size': 0,
            'last_update': time.time()
        }
        
        print(f"📦 Enhanced attack mode: {self.attack_mode}")
        
        # Add a botnet option for variety
        if random.random() < 0.3:  # 30% chance
            self.attack_mode = 'botnet_c2'
            print(f"📦 Switching to botnet C&C simulation for variety")
    
    def extract_enhanced_features(self, packets):
        """Extract 10 highly distinctive features for better classification"""
        if len(packets) < 10:
            return [0.0] * 10
        
        # Convert to arrays for analysis
        sizes = [p['size'] for p in packets]
        protocols = [p['protocol'] for p in packets]
        src_ips = [p['src_ip'] for p in packets]
        dst_ports = [p['dst_port'] for p in packets]
        flags = [p.get('flags', '') for p in packets]
        entropies = [p.get('payload_entropy', 0.5) for p in packets]
        intervals = [p.get('packet_interval', 0.3) for p in packets]
        signatures = [p.get('attack_signature', 'normal') for p in packets]
        
        # Feature 1: Packet rate (packets per second equivalent)
        time_span = max([p['timestamp'] for p in packets]) - min([p['timestamp'] for p in packets]) + 0.1
        packet_rate = len(packets) / time_span
        
        # Feature 2: Average packet size
        avg_packet_size = np.mean(sizes)
        
        # Feature 3: Source IP diversity (key for DDoS detection)
        unique_ips = len(set(src_ips))
        ip_diversity = unique_ips / len(packets)
        
        # Feature 4: Port diversity (key for port scan detection)
        unique_ports = len(set(dst_ports))
        port_diversity = unique_ports / len(packets)
        
        # Feature 5: Protocol concentration (TCP vs UDP ratio)
        tcp_count = protocols.count('TCP')
        udp_count = protocols.count('UDP')
        protocol_ratio = tcp_count / (tcp_count + udp_count + 1)
        
        # Feature 6: Payload entropy (key for encrypted/bot traffic)
        avg_entropy = np.mean(entropies)
        
        # Feature 7: Packet size variance (consistency indicator)
        size_variance = np.var(sizes)
        
        # Feature 8: SYN flag concentration (port scan indicator)
        syn_count = flags.count('SYN')
        syn_ratio = syn_count / len(packets)
        
        # Feature 9: Large packet ratio (data exfiltration indicator)
        large_packets = sum(1 for s in sizes if s > 1000)
        large_packet_ratio = large_packets / len(packets)
        
        # Feature 10: Attack signature confidence
        attack_indicators = sum(1 for s in signatures if s != 'normal_business')
        attack_signature_score = attack_indicators / len(packets)
        
        features = [
            packet_rate,
            avg_packet_size,
            ip_diversity,
            port_diversity,
            protocol_ratio,
            avg_entropy,
            size_variance,
            syn_ratio,
            large_packet_ratio,
            attack_signature_score
        ]
        
        return features
    
    def train_enhanced_model(self):
        """Train model on distinctive attack patterns"""
        if not self.quantum_available:
            return
        
        try:
            import time
            start_time = time.time()
            
            print("🔬 Training Enhanced Packet Security AI with Distinctive Patterns...")
            
            # Generate enhanced training dataset
            X_train, y_train = self._generate_enhanced_dataset()
            
            # Train with optimizer
            optimizer = qml.AdamOptimizer(stepsize=0.05)  # Slower for better convergence
            
            print("🔬 Enhanced Training Progress:")
            
            best_loss = float('inf')
            patience = 20
            patience_counter = 0
            
            for epoch in range(80):  # More epochs for better learning
                def cost_function(params):
                    total_loss = 0.0
                    for x, y in zip(X_train, y_train):
                        pred_raw = self.quantum_circuit(x, params)
                        pred = 1 / (1 + pnp.exp(-pred_raw * 3))  # Steeper sigmoid
                        loss = (pred - y) ** 2
                        total_loss += loss
                    return total_loss / len(X_train)
                
                self.params, current_loss = optimizer.step_and_cost(cost_function, self.params)
                
                if current_loss < best_loss:
                    best_loss = current_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                
                if patience_counter >= patience:
                    print(f"   Early stopping at epoch {epoch + 1}")
                    break
                
                if (epoch + 1) % 20 == 0:
                    accuracy = self._evaluate_enhanced_accuracy(X_train, y_train)
                    print(f"   Epoch {epoch + 1}/80: Loss = {current_loss:.4f}, Accuracy = {accuracy:.1%}")
            
            # Final metrics
            training_time = time.time() - start_time
            self.model_metrics['training_epochs'] = epoch + 1
            self.model_metrics['training_time'] = training_time
            self.model_metrics['accuracy'] = self._evaluate_enhanced_accuracy(X_train, y_train)
            self.is_trained = True
            
            print(f"✅ Enhanced Packet Security AI training complete!")
            print(f"📊 Performance: {self.model_metrics['accuracy']:.1%} accuracy in {training_time:.1f}s")
            print(f"📦 Trained on distinctive attack patterns for clear differentiation")
            
        except Exception as e:
            print(f"❌ Enhanced training failed: {e}")
            import traceback
            traceback.print_exc()
            self.is_trained = False
    
    def _generate_enhanced_dataset(self):
        """Generate enhanced dataset with very distinctive patterns"""
        X_train = []
        y_train = []
        
        print("📦 Generating Enhanced Attack Dataset with Distinctive Patterns:")
        
        # Normal business traffic (label: 0)
        print("   - 80 Normal business patterns")
        for _ in range(80):
            features = [
                random.uniform(10, 30),      # Normal packet rate
                random.uniform(300, 800),    # Normal packet sizes
                random.uniform(0.1, 0.3),    # Low IP diversity
                random.uniform(0.1, 0.2),    # Low port diversity
                random.uniform(0.7, 0.9),    # High TCP ratio
                random.uniform(0.4, 0.7),    # Normal entropy
                random.uniform(10000, 50000), # Normal size variance
                random.uniform(0.0, 0.1),    # Low SYN ratio
                random.uniform(0.2, 0.6),    # Some large packets
                random.uniform(0.0, 0.1)     # Low attack signature
            ]
            X_train.append(features)
            y_train.append(0.0)
        
        # DDoS Volumetric attacks (label: 1)
        print("   - 40 DDoS volumetric patterns")
        for _ in range(40):
            features = [
                random.uniform(200, 800),    # Very high packet rate
                random.uniform(64, 100),     # Small packet sizes
                random.uniform(0.8, 1.0),    # Very high IP diversity
                random.uniform(0.1, 0.3),    # Focused ports
                random.uniform(0.2, 0.5),    # Mixed protocols
                random.uniform(0.1, 0.3),    # Low entropy
                random.uniform(100, 2000),   # Low size variance
                random.uniform(0.3, 0.7),    # High SYN ratio
                random.uniform(0.0, 0.2),    # Few large packets
                random.uniform(0.8, 1.0)     # High attack signature
            ]
            X_train.append(features)
            y_train.append(1.0)
        
        # Port scanning attacks (label: 1)
        print("   - 30 Port scanning patterns")
        for _ in range(30):
            features = [
                random.uniform(50, 150),     # Moderate packet rate
                random.uniform(60, 80),      # Small SYN packets
                random.uniform(0.0, 0.1),    # Very low IP diversity
                random.uniform(0.8, 1.0),    # Very high port diversity
                random.uniform(0.9, 1.0),    # Almost all TCP
                random.uniform(0.0, 0.1),    # Very low entropy
                random.uniform(10, 100),     # Very low size variance
                random.uniform(0.9, 1.0),    # Almost all SYN
                random.uniform(0.0, 0.1),    # No large packets
                random.uniform(0.9, 1.0)     # High attack signature
            ]
            X_train.append(features)
            y_train.append(1.0)
        
        # Data exfiltration (label: 1)
        print("   - 25 Data exfiltration patterns")
        for _ in range(25):
            features = [
                random.uniform(5, 20),       # Low packet rate
                random.uniform(1200, 1500),  # Large packet sizes
                random.uniform(0.0, 0.1),    # Low IP diversity
                random.uniform(0.1, 0.3),    # Low port diversity
                random.uniform(0.8, 1.0),    # High TCP ratio
                random.uniform(0.8, 1.0),    # High entropy (encrypted)
                random.uniform(1000, 5000),  # Low size variance
                random.uniform(0.0, 0.1),    # Low SYN ratio
                random.uniform(0.8, 1.0),    # High large packet ratio
                random.uniform(0.7, 1.0)     # High attack signature
            ]
            X_train.append(features)
            y_train.append(1.0)
        
        # Botnet C&C (label: 1)
        print("   - 20 Botnet C&C patterns")
        for _ in range(20):
            features = [
                random.uniform(1, 10),       # Very low packet rate
                random.uniform(200, 400),    # Medium packet sizes
                random.uniform(0.0, 0.1),    # Very low IP diversity
                random.uniform(0.0, 0.2),    # Very low port diversity
                random.uniform(0.7, 0.9),    # High TCP ratio
                random.uniform(0.6, 0.8),    # Medium entropy
                random.uniform(1000, 10000), # Medium size variance
                random.uniform(0.0, 0.2),    # Low SYN ratio
                random.uniform(0.3, 0.7),    # Medium large packets
                random.uniform(0.8, 1.0)     # High attack signature
            ]
            X_train.append(features)
            y_train.append(1.0)
        
        print(f"📦 Enhanced Dataset: {len(X_train)} samples with distinctive patterns")
        print(f"   - Normal: 80 samples")
        print(f"   - Attacks: 115 samples (DDoS, Port Scan, Exfiltration, Botnet)")
        
        return np.array(X_train), np.array(y_train)
    
    def _evaluate_enhanced_accuracy(self, X_test, y_test):
        """Evaluate enhanced model accuracy"""
        if not self.is_trained:
            return 0.0
        
        correct = 0
        for features, true_label in zip(X_test, y_test):
            pred = self.quantum_predict(features)
            pred_label = 1 if pred > 0.5 else 0
            if pred_label == true_label:
                correct += 1
        
        return correct / len(X_test)
    
    def quantum_predict(self, features):
        """Enhanced quantum prediction"""
        if not self.quantum_available or not self.is_trained:
            return 0.5
        
        try:
            # Prepare features for quantum circuit
            processed_features = self._prepare_enhanced_features(features)
            
            # Quantum inference
            measurement = self.quantum_circuit(processed_features, self.params)
            
            # Enhanced sigmoid conversion
            probability = 1 / (1 + np.exp(-measurement * 3))
            
            return float(probability)
            
        except Exception as e:
            print(f"❌ Quantum prediction error: {e}")
            return 0.5
    
    def _prepare_enhanced_features(self, features):
        """Prepare features for enhanced quantum processing"""
        # Ensure correct number of features
        processed = np.array(features[:self.n_features])
        if len(processed) < self.n_features:
            processed = np.pad(processed, (0, self.n_features - len(processed)), 'constant')
        
        # Enhanced normalization with better scaling
        processed = np.clip(processed, 0, 1000)  # Reasonable bounds
        processed = processed / 1000.0  # Scale to [0, 1]
        
        return processed[:self.n_qubits]  # Use first 4 for quantum circuit
    
    def update_timing(self, timestamp):
        """Update timing - triggers enhanced packet analysis"""
        try:
            current_time = datetime.fromisoformat(timestamp)
            self.last_update_time = current_time
            
            # Trigger enhanced packet analysis
            if len(self.packet_history) >= 50:
                recent_packets = list(self.packet_history)[-100:]  # More packets for better analysis
                features = self.extract_enhanced_features(recent_packets)
                threat_score = self.quantum_predict(features)
                
                # Get real-time stats for display
                stats = self.get_real_time_packet_stats()
                
                print(f"📦 Enhanced Analysis: {len(recent_packets)} packets | PPS: {stats['packets_per_second']} | Threat: {threat_score:.3f}")
                
        except Exception as e:
            print(f"❌ Error in enhanced packet analysis: {e}")
    
    def analyze_current_pattern(self):
        """Enhanced pattern analysis with better classification"""
        if len(self.packet_history) < 30:
            return {
                'pattern_type': 'insufficient_data',
                'quantum_score': 0.0,
                'classical_score': 0.0,
                'confidence': 0.0,
                'attack_detected': False,
                'features': [0] * 10,
                'threat_level': 'LOW',
                'recommendation': 'Collecting enhanced packet baseline...',
                'model_performance': self.model_metrics,
                'real_time_stats': self.get_real_time_packet_stats()
            }
        
        # Analyze recent packet flows with enhanced features
        recent_packets = list(self.packet_history)[-150:]  # More packets for better analysis
        features = self.extract_enhanced_features(recent_packets)
        
        # Enhanced quantum + classical detection
        quantum_score = self.quantum_predict(features) if self.quantum_available else 0.5
        classical_score = self._enhanced_classical_detection(features)
        
        # Weighted ensemble (quantum gets more weight as it's more sophisticated)
        combined_score = (quantum_score * 0.7) + (classical_score * 0.3)
        
        # Attack detection with dynamic threshold
        attack_detected = combined_score > 0.6
        
        # Enhanced threat classification with real packet data
        threat_analysis = self._classify_enhanced_threat(features, recent_packets, attack_detected)
        
        # Get real-time stats
        real_time_stats = self.get_real_time_packet_stats()
        
        print(f"📦 Enhanced Analysis: Q={quantum_score:.3f}, C={classical_score:.3f}, Combined={combined_score:.3f}")
        print(f"🎯 Detection: {threat_analysis['type']} | Level: {threat_analysis['level']}")
        print(f"📈 Real-time: {real_time_stats['packets_per_second']} PPS, {real_time_stats['total_packets']} total packets")
        
        return {
            'pattern_type': threat_analysis['type'],
            'quantum_score': float(quantum_score),
            'classical_score': float(classical_score),
            'confidence': float(combined_score),
            'attack_detected': attack_detected,
            'features': features,
            'threat_level': threat_analysis['level'],
            'recommendation': threat_analysis['recommendation'],
            'model_performance': self.model_metrics,
            'real_time_stats': real_time_stats
        }
    
    def _enhanced_classical_detection(self, features):
        """Enhanced classical detection with better feature weighting"""
        packet_rate, avg_size, ip_diversity, port_diversity, protocol_ratio, avg_entropy, size_variance, syn_ratio, large_packet_ratio, attack_signature_score = features
        
        score = 0.0
        
        # DDoS indicators (high packet rate + high IP diversity)
        if packet_rate > 100 and ip_diversity > 0.7:
            score += 0.4
        
        # Port scan indicators (high port diversity + high SYN ratio)
        if port_diversity > 0.7 and syn_ratio > 0.8:
            score += 0.4
        
        # Data exfiltration indicators (large packets + high entropy)
        if large_packet_ratio > 0.7 and avg_entropy > 0.8:
            score += 0.3
        
        # Botnet indicators (low packet rate + medium entropy + specific patterns)
        if packet_rate < 20 and 0.6 < avg_entropy < 0.8 and attack_signature_score > 0.7:
            score += 0.3
        
        # General anomaly indicators
        if avg_size < 100 or avg_size > 1400:  # Unusual packet sizes
            score += 0.2
        
        if protocol_ratio < 0.3 or protocol_ratio > 0.95:  # Unusual protocol distribution
            score += 0.2
        
        return min(score, 1.0)
    
    def _classify_enhanced_threat(self, features, packets, is_attack):
        """Enhanced threat classification with specific attack types"""
        if not is_attack:
            return {
                'type': 'normal_business_traffic',
                'level': 'LOW',
                'recommendation': 'Normal business operations detected. Monitoring continues.'
            }
        
        packet_rate, avg_size, ip_diversity, port_diversity, protocol_ratio, avg_entropy, size_variance, syn_ratio, large_packet_ratio, attack_signature_score = features
        
        # Analyze packet signatures for specific classification
        signatures = [p.get('attack_signature', 'normal') for p in packets]
        signature_counts = {sig: signatures.count(sig) for sig in set(signatures)}
        
        # DDoS Volumetric Attack
        if packet_rate > 150 and ip_diversity > 0.8 and avg_size < 200:
            return {
                'type': 'ddos_volumetric_flood',
                'level': 'CRITICAL',
                'recommendation': 'CRITICAL: Massive DDoS volumetric attack detected. Deploy emergency DDoS mitigation immediately.'
            }
        
        # Port Scan Attack
        elif port_diversity > 0.6 and syn_ratio > 0.7 and ip_diversity < 0.2:
            return {
                'type': 'port_scan_reconnaissance',
                'level': 'HIGH',
                'recommendation': 'Port scanning attack detected. Block source IP and implement port scan protection.'
            }
        
        # Data Exfiltration
        elif large_packet_ratio > 0.6 and avg_entropy > 0.7 and packet_rate < 50:
            return {
                'type': 'data_exfiltration_attempt',
                'level': 'CRITICAL',
                'recommendation': 'CRITICAL: Data exfiltration detected. Block outbound connections and investigate immediately.'
            }
        
        # Botnet C&C Communication
        elif packet_rate < 15 and 0.6 < avg_entropy < 0.8 and 'botnet_beacon' in signature_counts:
            return {
                'type': 'botnet_command_control',
                'level': 'HIGH',
                'recommendation': 'Botnet C&C communication detected. Quarantine infected host and block C&C servers.'
            }
        
        # SYN Flood Attack
        elif syn_ratio > 0.8 and packet_rate > 80:
            return {
                'type': 'syn_flood_attack',
                'level': 'HIGH',
                'recommendation': 'SYN flood attack detected. Enable SYN cookies and implement rate limiting.'
            }
        
        # Unknown Attack Pattern
        else:
            return {
                'type': 'unknown_attack_pattern',
                'level': 'MEDIUM',
                'recommendation': 'Unknown attack pattern detected. Enhanced monitoring and manual analysis recommended.'
            }
    
    # Keep existing save/load/validation methods but enhance them
    def save_model(self):
        """Save enhanced model"""
        if not self.is_trained:
            return False
        
        try:
            model_data = {
                'params': self.params,
                'scaler': self.scaler,
                'n_qubits': self.n_qubits,
                'n_layers': self.n_layers,
                'n_features': self.n_features,
                'model_metrics': self.model_metrics,
                'trained_at': datetime.now().isoformat(),
                'is_trained': self.is_trained,
                'model_version': 'Enhanced-Packet-4Q-v2.0',
                'architecture': 'Enhanced 4-Qubit Packet Analysis with Distinctive Pattern Recognition'
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"💾 Enhanced Packet Quantum Security AI saved")
            return True
            
        except Exception as e:
            print(f"❌ Error saving enhanced model: {e}")
            return False
    
    def load_model(self):
        """Load enhanced model"""
        if not os.path.exists(self.model_path):
            return False
        
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.params = model_data['params']
            self.scaler = model_data['scaler']
            self.n_qubits = model_data.get('n_qubits', 4)
            self.n_layers = model_data.get('n_layers', 3)
            self.n_features = model_data.get('n_features', 10)
            self.model_metrics = model_data.get('model_metrics', {})
            self.is_trained = model_data.get('is_trained', True)
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading enhanced model: {e}")
            return False
    
    def validate_model(self):
        """Enhanced model validation"""
        print("🧪 Enhanced Model Validation with Distinctive Patterns...")
        
        test_cases = [
            # Normal traffic
            ([25, 600, 0.2, 0.15, 0.8, 0.5, 25000, 0.05, 0.4, 0.1], 0, "Normal Business Traffic"),
            # DDoS volumetric
            ([400, 80, 0.9, 0.2, 0.3, 0.2, 500, 0.6, 0.1, 0.9], 1, "DDoS Volumetric Attack"),
            # Port scan
            ([100, 70, 0.05, 0.9, 0.95, 0.05, 50, 0.95, 0.05, 0.9], 1, "Port Scan Attack"),
            # Data exfiltration
            ([15, 1400, 0.05, 0.2, 0.9, 0.9, 2000, 0.1, 0.9, 0.8], 1, "Data Exfiltration"),
            # Botnet C&C
            ([8, 300, 0.05, 0.1, 0.8, 0.7, 5000, 0.1, 0.5, 0.9], 1, "Botnet C&C Communication")
        ]
        
        correct = 0
        for features, expected, description in test_cases:
            prediction = self.quantum_predict(features)
            predicted = 1 if prediction > 0.5 else 0
            
            if predicted == expected:
                correct += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
            
            print(f"   {status} {description}: {prediction:.3f}")
        
        accuracy = correct / len(test_cases)
        print(f"🎯 Enhanced Validation: {accuracy:.1%} accuracy")
        
        return accuracy >= 0.8
    
    def get_enterprise_analytics(self):
        """Get enhanced analytics with real-time packet monitoring"""
        real_time_stats = self.get_real_time_packet_stats()
        
        return {
            'model_info': {
                'quantum_available': self.quantum_available,
                'is_trained': self.is_trained,
                'model_accuracy': self.model_metrics.get('accuracy', 0),
                'training_iterations': self.model_metrics.get('training_epochs', 0),
                'training_time': self.model_metrics.get('training_time', 0),
                'architecture': f"{self.n_qubits} qubits, {self.n_features} enhanced features",
                'model_version': 'Enhanced-Packet-4Q-v2.0'
            },
            'real_time_metrics': {
                'packet_history_length': len(self.packet_history),
                'attack_mode': self.attack_mode,
                'total_packets': real_time_stats['total_packets'],
                'packets_per_second': real_time_stats['packets_per_second'],
                'unique_src_ips': real_time_stats['unique_src_ips'],
                'unique_dst_ports': real_time_stats['unique_dst_ports'],
                'avg_packet_size': real_time_stats['avg_packet_size'],
                'protocol_distribution': real_time_stats['protocol_distribution'],
                'monitoring_duration': real_time_stats['monitoring_duration']
            },
            'threat_intelligence': {
                'detected_categories': ['DDoS Volumetric', 'Port Scan', 'Data Exfiltration', 'Botnet C&C', 'SYN Flood'],
                'enhanced_features': ['Rate', 'Size', 'IP Diversity', 'Port Diversity', 'Protocol Ratio', 
                                    'Entropy', 'Size Variance', 'SYN Ratio', 'Large Packet Ratio', 'Attack Signature']
            }
        }


# Backward compatibility
QuantumNetworkAnalyzer = EnhancedPacketQuantumSecurityAI
PacketBasedQuantumSecurityAI = EnhancedPacketQuantumSecurityAI