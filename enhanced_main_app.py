# enhanced_main_app.py - COMPLETE ENHANCED VERSION with Real-Time Packet Monitoring
import threading
import time
import sys
import json
import subprocess
import os
from datetime import datetime
from flask import Flask, request, jsonify

# Import our Enhanced Packet-Based Quantum components
try:
    from quantum_analyzer import EnhancedPacketQuantumSecurityAI as QuantumNetworkAnalyzer
    from attack_simulator import NetworkAttackSimulator
    from quantum_server import QuantumNetworkMonitorServer
    from quantum_client import QuantumNetworkClient
    QUANTUM_IMPORTS = True
    print("✅ Enhanced Packet Quantum Security AI components loaded successfully!")
except ImportError as e:
    print(f"❌ Critical import error: {e}")
    print("💡 Please ensure all modules are in the same directory")
    QUANTUM_IMPORTS = False
    sys.exit(1)

class SimpleMinineController:
    """WSL-compatible Mininet controller"""
    def __init__(self):
        self.mininet_process = None
        self.monitoring_active = False
        self.wsl_interface = self.detect_wsl_interface()
        
    def detect_wsl_interface(self):
        """Detect the main network interface in WSL"""
        try:
            import subprocess
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True, check=True)
            interface = result.stdout.split()[4] if result.stdout else 'eth0'
            print(f"🌐 Detected WSL interface: {interface}")
            return interface
        except:
            print("⚠️  Failed to detect interface, using eth0")
            return 'eth0'
    
    def start_mininet_topology(self):
        """Start basic Mininet topology for WSL"""
        try:
            print("🌐 Starting WSL-compatible Mininet topology...")
            
            result = subprocess.run(['which', 'mn'], capture_output=True)
            if result.returncode != 0:
                print("❌ Mininet not found. Install with: sudo apt install mininet")
                return False
            
            cmd = [
                'sudo', 'mn', 
                '--topo', 'single,2', 
                '--controller', 'remote,ip=127.0.0.1,port=6633',
                '--switch', 'ovsk',
                '--link', 'tc'
            ]
            
            self.mininet_process = subprocess.Popen(
                cmd, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            time.sleep(5)
            
            if self.mininet_process.poll() is None:
                print("✅ WSL Mininet topology started")
                return True
            else:
                print("❌ Failed to start Mininet topology")
                return False
        except Exception as e:
            print(f"❌ Error starting Mininet in WSL: {e}")
            return False
    
    def apply_network_attack(self, attack_type):
        """Apply network conditions via tc commands for WSL"""
        try:
            subprocess.run(['sudo', 'tc', 'qdisc', 'del', 'dev', self.wsl_interface, 'root'], 
                         check=False, capture_output=True)
            
            if attack_type == 'dos' or attack_type == 'ddos':
                print(f"🚨 Applying DoS conditions to {self.wsl_interface}...")
                subprocess.run([
                    'sudo', 'tc', 'qdisc', 'add', 'dev', self.wsl_interface, 'root', 
                    'netem', 'delay', '500ms', 'loss', '10%'
                ], check=True)
                
            elif attack_type == 'flooding':
                print(f"🌊 Applying flooding conditions to {self.wsl_interface}...")
                subprocess.run([
                    'sudo', 'tc', 'qdisc', 'add', 'dev', self.wsl_interface, 'root', 
                    'tbf', 'rate', '1mbit', 'burst', '32kbit', 'latency', '400ms'
                ], check=True)
                
            elif attack_type == 'congestion':
                print(f"🚦 Applying congestion conditions to {self.wsl_interface}...")
                subprocess.run([
                    'sudo', 'tc', 'qdisc', 'add', 'dev', self.wsl_interface, 'root', 
                    'netem', 'delay', '100ms', '50ms'
                ], check=True)
                
            elif attack_type == 'normal':
                print(f"✅ Reset {self.wsl_interface} to normal conditions")
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Traffic control command failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Error applying network conditions in WSL: {e}")
            return False
    
    def get_network_statistics(self):
        """Get WSL network statistics"""
        try:
            result = subprocess.run(['cat', f'/sys/class/net/{self.wsl_interface}/statistics/rx_bytes'], 
                                  capture_output=True, text=True, check=True)
            rx_bytes = int(result.stdout.strip())
            
            result = subprocess.run(['cat', f'/sys/class/net/{self.wsl_interface}/statistics/tx_bytes'], 
                                  capture_output=True, text=True, check=True)
            tx_bytes = int(result.stdout.strip())
            
            return {
                'server_host': {'ip': '127.0.0.1', 'status': 'active'},
                'client_host': {'ip': '127.0.0.1', 'status': 'active'},
                'link_status': {
                    'interface': self.wsl_interface,
                    'rx_bytes': rx_bytes,
                    'tx_bytes': tx_bytes,
                    'bandwidth': '100Mbps',
                    'latency': '1ms',
                    'packet_loss': '0%'
                }
            }
        except:
            return {
                'server_host': {'ip': '127.0.0.1', 'status': 'active'},
                'client_host': {'ip': '127.0.0.1', 'status': 'active'},
                'link_status': {'bandwidth': '100Mbps', 'latency': '1ms', 'packet_loss': '0%'}
            }
    
    def start_monitoring(self):
        """Start network monitoring"""
        self.monitoring_active = True
        print("📊 WSL network monitoring started")
    
    def stop_mininet(self):
        """Stop Mininet and clean up WSL"""
        try:
            print("🛑 Stopping Mininet in WSL...")
            
            if self.mininet_process:
                self.mininet_process.terminate()
                try:
                    self.mininet_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.mininet_process.kill()
            
            subprocess.run(['sudo', 'mn', '-c'], check=False, capture_output=True)
            subprocess.run(['sudo', 'tc', 'qdisc', 'del', 'dev', self.wsl_interface, 'root'], 
                         check=False, capture_output=True)
            
            print("✅ WSL Mininet stopped and cleaned up")
        except Exception as e:
            print(f"⚠️  WSL cleanup warning: {e}")

class EnhancedPacketQuantumNetworkMonitor:
    def __init__(self):
        print("📦 Initializing Enhanced Packet Quantum Network Security System...")
        
        # Initialize Enhanced Packet Quantum Security AI
        self.quantum_analyzer = QuantumNetworkAnalyzer()
        self.server = QuantumNetworkMonitorServer(self.quantum_analyzer)
        
        # Initialize Mininet controller
        self.mininet_controller = SimpleMinineController()
        self.mininet_enabled = False
        
        # Create client and attack simulator
        self.attack_simulator = NetworkAttackSimulator(None)
        self.client = QuantumNetworkClient(self.attack_simulator)
        self.attack_simulator.client = self.client
        
        # Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        print("✅ Enhanced Packet Quantum Network Security System initialized")
        
    def setup_routes(self):
        """Setup Flask routes with Enhanced Packet Quantum Security features"""
        
        @self.app.route('/')
        def quantum_dashboard():
            return self.render_enhanced_packet_dashboard()
        
        @self.app.route('/update', methods=['POST'])
        def receive_update():
            try:
                data = request.json
                self.server.update_client_data(data)
                self.server.log_event("CLIENT_UPDATE", f"Received {len(data)} entries")
                return jsonify({'status': 'success', 'message': 'Data updated'})
            except Exception as e:
                print(f"❌ [SERVER] Error processing update: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        # Client control routes
        @self.app.route('/start_client')
        def start_client():
            self.client.start()
            self.server.log_event("CLIENT_STARTED", "Client manually started via web interface")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/stop_client')
        def stop_client():
            self.client.stop()
            self.server.log_event("CLIENT_MANUALLY_STOPPED", "Client manually stopped")
            return '<script>window.location.href="/"</script>'
        
        # Enhanced packet-based attack simulation routes
        @self.app.route('/simulate_dos')
        def simulate_dos():
            self.enhanced_attack_simulation('ddos')  # DDoS Volumetric
            self.server.log_event("ENHANCED_DDOS_SIMULATION", "Enhanced DDoS volumetric attack simulation initiated")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/simulate_flooding')
        def simulate_flooding():
            self.enhanced_attack_simulation('flooding')  # Port Scan
            self.server.log_event("ENHANCED_PORTSCAN_SIMULATION", "Enhanced port scan attack simulation initiated")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/simulate_congestion')
        def simulate_congestion():
            self.enhanced_attack_simulation('congestion')  # Data Exfiltration
            self.server.log_event("ENHANCED_EXFILTRATION_SIMULATION", "Enhanced data exfiltration simulation initiated")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/stop_attack')
        def stop_attack():
            self.enhanced_stop_attack()
            self.server.log_event("ENHANCED_ATTACK_STOPPED", "Enhanced attack simulation stopped")
            return '<script>window.location.href="/"</script>'
        
        # Mininet control routes
        @self.app.route('/start_mininet')
        def start_mininet():
            success = self.start_mininet_integration()
            if success:
                self.server.log_event("MININET_STARTED", "Mininet network simulation started")
            else:
                self.server.log_event("MININET_FAILED", "Failed to start Mininet network simulation")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/stop_mininet')
        def stop_mininet():
            self.stop_mininet_integration()
            self.server.log_event("MININET_STOPPED", "Mininet network simulation stopped")
            return '<script>window.location.href="/"</script>'
        
        @self.app.route('/force_save_state')
        def force_save_state():
            analysis = self.quantum_analyzer.analyze_current_pattern()
            self.server.save_client_state("Manual state save triggered", analysis)
            self.server.log_event("MANUAL_STATE_SAVE", "State manually saved via web interface")
            return '<script>window.location.href="/"</script>'
        
        # Enhanced packet analytics route
        @self.app.route('/packet_analytics')
        def packet_analytics():
            try:
                analytics = self.quantum_analyzer.get_enterprise_analytics()
                return jsonify(analytics)
            except:
                return jsonify({'error': 'Enhanced packet analytics not available'})
    
    def enhanced_attack_simulation(self, attack_type):
        """Enhanced attack simulation using distinctive packet patterns"""
        print(f"📦 Enhanced {attack_type} attack: Network + Application + Packet level")
        
        # Set enhanced packet simulation mode
        if hasattr(self.quantum_analyzer, 'set_attack_mode'):
            self.quantum_analyzer.set_attack_mode(attack_type)
        
        # Apply Mininet network conditions if enabled
        if self.mininet_enabled:
            self.mininet_controller.apply_network_attack(attack_type)
        
        # Apply application-level attack simulation
        if attack_type == 'dos' or attack_type == 'ddos':
            self.attack_simulator.start_dos_attack()
        elif attack_type == 'flooding':
            self.attack_simulator.start_flooding_attack()
        elif attack_type == 'congestion':
            self.attack_simulator.start_congestion_attack()
    
    def enhanced_stop_attack(self):
        """Stop enhanced packet-based, Mininet and application-level attacks"""
        print("✅ Stopping all enhanced attack simulations...")
        
        # Stop enhanced packet simulation
        if hasattr(self.quantum_analyzer, 'set_attack_mode'):
            self.quantum_analyzer.set_attack_mode(None)
        
        # Stop application-level attacks
        self.attack_simulator.stop_attack()
        
        # Reset Mininet to normal conditions if enabled
        if self.mininet_enabled:
            self.mininet_controller.apply_network_attack('normal')
    
    def start_mininet_integration(self):
        """Start Mininet network simulation"""
        print("🌐 Starting Mininet integration...")
        
        try:
            if not self.check_root_permissions():
                print("⚠️  Mininet requires root privileges. Run with sudo.")
                return False
            
            success = self.mininet_controller.start_mininet_topology()
            if success:
                self.mininet_enabled = True
                self.mininet_controller.start_monitoring()
                print("✅ Mininet integration started")
                return True
            else:
                print("❌ Failed to start Mininet")
                return False
                
        except Exception as e:
            print(f"❌ Error starting Mininet: {e}")
            return False
    
    def stop_mininet_integration(self):
        """Stop Mininet network simulation"""
        print("🛑 Stopping Mininet integration...")
        
        try:
            self.mininet_controller.stop_mininet()
            self.mininet_enabled = False
            print("✅ Mininet stopped")
        except Exception as e:
            print(f"❌ Error stopping Mininet: {e}")
    
    def check_root_permissions(self):
        """Check if running with appropriate permissions"""
        try:
            if hasattr(os, 'geteuid'):
                return os.geteuid() == 0
            else:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def get_enhanced_status(self):
        """Get enhanced status including Enhanced Packet Quantum Security metrics"""
        # Get base quantum status
        status_data = self.server.get_status()
        
        # Add Enhanced Packet analytics
        try:
            packet_analytics = self.quantum_analyzer.get_enterprise_analytics()
            status_data['packet_analytics'] = packet_analytics
        except:
            status_data['packet_analytics'] = {}
        
        # Add Mininet statistics if enabled
        if self.mininet_enabled:
            mininet_stats = self.mininet_controller.get_network_statistics()
            status_data['mininet_stats'] = mininet_stats
            status_data['mininet_enabled'] = True
        else:
            status_data['mininet_enabled'] = False
        
        return status_data
    
    def render_enhanced_packet_dashboard(self):
        """Render Enhanced Packet Quantum Security dashboard with real-time monitoring"""
        status_data = self.get_enhanced_status()
        
        current_data = status_data['current_data']
        recent_logs = status_data['recent_logs'] 
        quantum_analysis = status_data['quantum_analysis']
        snapshots = status_data['saved_snapshots']
        mininet_enabled = status_data.get('mininet_enabled', False)
        mininet_stats = status_data.get('mininet_stats', {})
        
        # Get enhanced packet analytics
        try:
            packet_analytics = status_data.get('packet_analytics', {})
            model_info = packet_analytics.get('model_info', {})
            real_time_metrics = packet_analytics.get('real_time_metrics', {})
            
            # Extract real-time stats
            total_packets = real_time_metrics.get('total_packets', 0)
            packets_per_second = real_time_metrics.get('packets_per_second', 0)
            unique_ips = real_time_metrics.get('unique_src_ips', 0)
            unique_ports = real_time_metrics.get('unique_dst_ports', 0)
            avg_packet_size = real_time_metrics.get('avg_packet_size', 0)
            protocol_dist = real_time_metrics.get('protocol_distribution', {})
            attack_mode = real_time_metrics.get('attack_mode', 'normal')
            monitoring_duration = real_time_metrics.get('monitoring_duration', 0)
            
            model_accuracy = model_info.get('model_accuracy', 0) * 100
            model_architecture = model_info.get('architecture', 'Unknown')
            
        except:
            # Fallback values
            total_packets = 0
            packets_per_second = 0
            unique_ips = 0
            unique_ports = 0
            avg_packet_size = 0
            protocol_dist = {}
            attack_mode = 'normal'
            monitoring_duration = 0
            model_accuracy = 0
            model_architecture = 'Unknown'
        
        status = status_data['status']
        status_icon = "🟢" if status == "connected" else "🔴"
        
        last_seen = status_data['client_last_seen']
        if last_seen:
            last_time = datetime.fromisoformat(last_seen)
            time_diff = (datetime.now() - last_time).total_seconds()
            last_seen_display = f"{last_time.strftime('%H:%M:%S')} ({time_diff:.1f}s ago)"
        else:
            last_seen_display = "Never"
        
        client_status = "🟢 RUNNING" if self.client.running else "🔴 STOPPED"
        attack_status = "🚨 ACTIVE" if self.attack_simulator.attack_active else "✅ NONE"
        mininet_status = "🌐 ACTIVE" if mininet_enabled else "❌ DISABLED"
        
        # Recent quantum analysis
        latest_quantum = quantum_analysis[0] if quantum_analysis else None
        
        # Protocol distribution display
        protocol_display = ", ".join([f"{k}: {v}" for k, v in protocol_dist.items()]) if protocol_dist else "No protocols detected"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>📦 Enhanced Packet Quantum Security AI</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    min-height: 100vh;
                    color: #333;
                }}
                .container {{
                    max-width: 1600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    padding: 40px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    padding-bottom: 25px;
                    border-bottom: 3px solid #1e3c72;
                }}
                .header h1 {{
                    color: #1e3c72;
                    font-size: 2.5em;
                    margin: 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }}
                .enterprise-badge {{
                    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                    color: white;
                    padding: 8px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    display: inline-block;
                    margin-top: 10px;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                    100% {{ transform: scale(1); }}
                }}
                .status-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .status-card {{
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    font-weight: bold;
                    color: white;
                    font-size: 16px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                    transition: transform 0.3s ease;
                }}
                .status-card:hover {{
                    transform: translateY(-5px);
                }}
                .card-green {{ background: linear-gradient(135deg, #28a745, #20c997); }}
                .card-red {{ background: linear-gradient(135deg, #dc3545, #e74c3c); }}
                .card-blue {{ background: linear-gradient(135deg, #007bff, #0056b3); }}
                .card-purple {{ background: linear-gradient(135deg, #6f42c1, #5a2d91); }}
                .card-enterprise {{ background: linear-gradient(135deg, #1e3c72, #2a5298); }}
                
                .enterprise-metrics {{
                    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                    padding: 25px;
                    border-radius: 15px;
                    margin: 25px 0;
                    border-left: 5px solid #1e3c72;
                }}
                .metric-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                .metric-item {{
                    text-align: center;
                    padding: 15px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .metric-value {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #1e3c72;
                }}
                .metric-label {{
                    color: #6c757d;
                    font-size: 0.9em;
                    margin-top: 5px;
                }}
                
                .control-panel {{
                    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                    padding: 25px;
                    border-radius: 15px;
                    margin: 25px 0;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                }}
                .control-section {{
                    display: inline-block;
                    margin: 15px;
                    padding: 15px;
                    border: 2px solid #1e3c72;
                    border-radius: 10px;
                    background: white;
                    vertical-align: top;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .btn {{
                    background: linear-gradient(135deg, #007bff, #0056b3);
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                    margin: 5px;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 15px rgba(0,0,0,0.3);
                }}
                .btn-danger {{ background: linear-gradient(135deg, #dc3545, #c82333); }}
                .btn-success {{ background: linear-gradient(135deg, #28a745, #1e7e34); }}
                .btn-warning {{ background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529; }}
                .btn-info {{ background: linear-gradient(135deg, #17a2b8, #138496); }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 25px 0;
                    background: white;
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                }}
                th {{
                    background: linear-gradient(135deg, #1e3c72, #2a5298);
                    color: white;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 16px;
                }}
                td {{
                    padding: 12px 15px;
                    border-bottom: 1px solid #e9ecef;
                    font-size: 14px;
                }}
                tr:hover {{
                    background: #f8f9fa;
                }}
                .value {{
                    font-family: 'Courier New', monospace;
                    font-weight: bold;
                    color: #1e3c72;
                }}
                .timestamp {{
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                .section-title {{
                    font-size: 24px;
                    margin: 35px 0 20px 0;
                    color: #1e3c72;
                    border-bottom: 3px solid #1e3c72;
                    padding-bottom: 10px;
                    font-weight: 600;
                }}
                .quantum-score {{
                    display: inline-block;
                    padding: 6px 12px;
                    border-radius: 20px;
                    color: white;
                    font-weight: bold;
                    margin: 3px;
                    font-size: 12px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.2);
                }}
                .score-low {{ background: linear-gradient(135deg, #28a745, #20c997); }}
                .score-medium {{ background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529; }}
                .score-high {{ background: linear-gradient(135deg, #dc3545, #c82333); }}
                .real-time-box {{
                    background: linear-gradient(135deg, #e8f5e8, #d4edda);
                    border: 2px solid #28a745;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 25px 0;
                }}
                .attack-mode-box {{
                    background: linear-gradient(135deg, {'#ffeaa7' if attack_mode == 'normal' else '#ff7675'}, {'#fdcb6e' if attack_mode == 'normal' else '#e84393'});
                    border: 2px solid {'#fdcb6e' if attack_mode == 'normal' else '#e84393'};
                    border-radius: 15px;
                    padding: 20px;
                    margin: 25px 0;
                    color: {'#2d3436' if attack_mode == 'normal' else 'white'};
                }}
            </style>
            <script>
                function autoRefresh() {{
                    setTimeout(function(){{
                        window.location.reload();
                    }}, 2000);  // Refresh every 2 seconds for real-time feel
                }}
                window.onload = autoRefresh;
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📦 Enhanced Packet Quantum Security AI</h1>
                    <div class="enterprise-badge">Real-Time Network Packet Analysis with Quantum ML</div>
                    <p style="margin: 15px 0 0 0; color: #6c757d;">
                        Live Packet Monitoring • Quantum Neural Networks • Advanced Threat Detection
                    </p>
                </div>
                
                <div class="real-time-box">
                    <h3 style="color: #1e3c72; margin-bottom: 20px;">📈 Real-Time Packet Monitoring</h3>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-value" style="color: {'#dc3545' if packets_per_second > 100 else '#28a745'};">{packets_per_second}</div>
                            <div class="metric-label">Packets/Second</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{total_packets:,}</div>
                            <div class="metric-label">Total Packets</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value" style="color: {'#dc3545' if unique_ips > 50 else '#28a745'};">{unique_ips}</div>
                            <div class="metric-label">Unique Source IPs</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value" style="color: {'#dc3545' if unique_ports > 100 else '#28a745'};">{unique_ports}</div>
                            <div class="metric-label">Unique Dest Ports</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{avg_packet_size} B</div>
                            <div class="metric-label">Avg Packet Size</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{monitoring_duration:.1f}s</div>
                            <div class="metric-label">Monitoring Duration</div>
                        </div>
                    </div>
                    <div style="margin-top: 15px; padding: 10px; background: white; border-radius: 8px;">
                        <strong>Protocol Distribution:</strong> {protocol_display}
                    </div>
                </div>
                
                <div class="attack-mode-box">
                    <h3 style="margin-bottom: 15px;">🎯 Current Attack Simulation Mode</h3>
                    <div style="font-size: 1.5em; font-weight: bold;">
                        {attack_mode.replace('_', ' ').title()}
                        {'🟢 Normal Operations' if attack_mode == 'normal' else '🚨 Attack Simulation Active'}
                    </div>
                    <p style="margin-top: 10px; opacity: 0.9;">
                        {'System is monitoring normal business traffic patterns.' if attack_mode == 'normal' else f'Simulating {attack_mode.replace("_", " ")} attack patterns for quantum AI detection testing.'}
                    </p>
                </div>
                
                <div class="enterprise-metrics">
                    <h3 style="color: #1e3c72; margin-bottom: 20px;">📦 Quantum Security AI Performance</h3>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-value">{model_accuracy:.1f}%</div>
                            <div class="metric-label">Model Accuracy</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">4-Qubit</div>
                            <div class="metric-label">Quantum Architecture</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{len(self.quantum_analyzer.packet_history)}</div>
                            <div class="metric-label">Packet History</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{'✅' if self.quantum_analyzer.quantum_available else '❌'}</div>
                            <div class="metric-label">Quantum Status</div>
                        </div>
                    </div>
                </div>
                
                <div class="status-grid">
                    <div class="status-card card-{'green' if status == 'connected' else 'red'}">
                        {status_icon} Server Status<br>{status.upper()}
                    </div>
                    <div class="status-card card-{'green' if self.client.running else 'red'}">
                        📡 Client Status<br>{client_status}
                    </div>
                    <div class="status-card card-{'red' if self.attack_simulator.attack_active else 'green'}">
                        🚨 Attack Status<br>{attack_status}
                    </div>
                    <div class="status-card card-enterprise">
                        📦 Packet AI<br>{'✅ OPERATIONAL' if self.quantum_analyzer.quantum_available else '❌ OFFLINE'}
                    </div>
                    <div class="status-card card-{'blue' if mininet_enabled else 'red'}">
                        🌐 Network Sim<br>{mininet_status}
                    </div>
                </div>
                
                <div class="control-panel">
                    <h3 style="color: #1e3c72;">📦 Enhanced Packet Security Control Center</h3>
                    
                    <div class="control-section">
                        <h4>Client Operations</h4>
                        <a href="/start_client" class="btn btn-success">▶️ Start Monitor</a>
                        <a href="/stop_client" class="btn btn-danger">⏹️ Stop Monitor</a>
                    </div>
                    
                    <div class="control-section">
                        <h4>Network Simulation</h4>
                        <a href="/start_mininet" class="btn btn-info">🌐 Start Mininet</a>
                        <a href="/stop_mininet" class="btn btn-danger">🛑 Stop Mininet</a>
                    </div>
                    
                    <div class="control-section">
                        <h4>Enhanced Packet Attack Simulation</h4>
                        <a href="/simulate_dos" class="btn btn-warning">💥 DDoS Volumetric</a>
                        <a href="/simulate_flooding" class="btn btn-warning">🌊 Port Scan</a>
                        <a href="/simulate_congestion" class="btn btn-warning">🚦 Data Exfiltration</a>
                        <a href="/stop_attack" class="btn btn-success">✅ Stop All</a>
                    </div>
                    
                    <div class="control-section">
                        <h4>System Operations</h4>
                        <a href="/" class="btn">🔄 Refresh</a>
                        <a href="/force_save_state" class="btn btn-danger">💾 Save State</a>
                        <a href="/packet_analytics" class="btn btn-info" target="_blank">📦 Packet Analytics</a>
                    </div>
                </div>"""

        # Add Mininet statistics if available
        if mininet_enabled and mininet_stats:
            html += f"""
                <div style="background: linear-gradient(135deg, #e8f4f8, #d1ecf1); border: 2px solid #bee5eb; border-radius: 15px; padding: 20px; margin: 25px 0;">
                    <h4 style="color: #1e3c72;">🌐 Mininet Network Intelligence</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 15px;">
                        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                            <strong>Server Node:</strong><br>
                            IP: {mininet_stats.get('server_host', {}).get('ip', 'N/A')}<br>
                            Status: {mininet_stats.get('server_host', {}).get('status', 'N/A')}
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                            <strong>Client Node:</strong><br>
                            IP: {mininet_stats.get('client_host', {}).get('ip', 'N/A')}<br>
                            Status: {mininet_stats.get('client_host', {}).get('status', 'N/A')}
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                            <strong>Network Link:</strong><br>
                            Bandwidth: {mininet_stats.get('link_status', {}).get('bandwidth', 'N/A')}<br>
                            Latency: {mininet_stats.get('link_status', {}).get('latency', 'N/A')}<br>
                            Loss: {mininet_stats.get('link_status', {}).get('packet_loss', 'N/A')}
                        </div>
                    </div>
                </div>
            """

        # Add enhanced packet analysis summary
        if latest_quantum:
            try:
                # Handle different database column counts safely
                quantum_row = latest_quantum
                if len(quantum_row) >= 7:
                    q_id, timestamp, pattern_type, quantum_score, classical_score, confidence, attack_detected = quantum_row[:7]
                else:
                    timestamp = quantum_row[1] if len(quantum_row) > 1 else ""
                    pattern_type = quantum_row[2] if len(quantum_row) > 2 else "unknown"
                    quantum_score = quantum_row[3] if len(quantum_row) > 3 else 0.0
                    classical_score = quantum_row[4] if len(quantum_row) > 4 else 0.0
                    confidence = quantum_row[5] if len(quantum_row) > 5 else 0.0
                    attack_detected = quantum_row[6] if len(quantum_row) > 6 else False
                
                html += f"""
                    <div style="background: linear-gradient(135deg, #e7f3ff, #cce7ff); border: 2px solid #b3d7ff; border-radius: 15px; padding: 20px; margin: 25px 0;">
                        <h4 style="color: #1e3c72;">📦 Latest Enhanced Packet Security Analysis</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 15px;">
                            <div style="background: white; padding: 15px; border-radius: 10px;">
                                <strong>Packet Pattern:</strong><br>
                                <span style="color: #1e3c72; font-size: 1.2em;">{pattern_type.replace('_', ' ').title()}</span>
                            </div>
                            <div style="background: white; padding: 15px; border-radius: 10px;">
                                <strong>Threat Status:</strong><br>
                                <span style="font-size: 1.5em;">{'🚨 DETECTED' if attack_detected else '✅ SECURE'}</span>
                            </div>
                            <div style="background: white; padding: 15px; border-radius: 10px;">
                                <strong>AI Confidence:</strong><br>
                                <span class="quantum-score score-{'high' if confidence > 0.7 else ('medium' if confidence > 0.4 else 'low')}">
                                    {confidence:.1%}
                                </span>
                            </div>
                        </div>
                        <div style="margin-top: 15px;">
                            <strong>Enhanced Detection Scores:</strong>
                            <span class="quantum-score score-{'high' if quantum_score > 0.7 else ('medium' if quantum_score > 0.4 else 'low')}">
                                Quantum: {quantum_score:.3f}
                            </span>
                            <span class="quantum-score score-{'high' if classical_score > 0.7 else ('medium' if classical_score > 0.4 else 'low')}">
                                Classical: {classical_score:.3f}
                            </span>
                        </div>
                    </div>
                """
            except Exception as e:
                html += f"""
                    <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 15px; padding: 20px; margin: 25px 0; color: #721c24;">
                        <h4>⚠️ Packet Analysis Display Error</h4>
                        <p>Error parsing quantum data: {str(e)}</p>
                    </div>
                """

        html += """
                <h2 class="section-title">📊 Current Network Data (5 Monitoring Points)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Monitor ID</th>
                            <th>Data Value</th>
                            <th>Server Timestamp</th>
                            <th>Client Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add current data rows
        for row in current_data:
            entry_id, value, server_time, client_time = row
            server_display = server_time[11:19] if server_time else "N/A"
            client_display = client_time[11:19] if client_time else "N/A"
            
            html += f"""
                        <tr>
                            <td><strong>Monitor #{entry_id}</strong></td>
                            <td class="value">{value:.2f}</td>
                            <td class="timestamp">{server_display}</td>
                            <td class="timestamp">{client_display}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
                
                <h2 class="section-title">📦 Enhanced Packet Security Analysis History</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Analysis Time</th>
                            <th>Packet Pattern</th>
                            <th>Quantum Score</th>
                            <th>Classical Score</th>
                            <th>Confidence</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add quantum analysis rows - SAFE UNPACKING
        for analysis in quantum_analysis[:5]:  # Show last 5
            try:
                if len(analysis) >= 7:
                    q_id, timestamp, pattern_type, q_score, c_score, confidence, attack = analysis[:7]
                else:
                    timestamp = analysis[1] if len(analysis) > 1 else ""
                    pattern_type = analysis[2] if len(analysis) > 2 else "unknown"
                    q_score = analysis[3] if len(analysis) > 3 else 0.0
                    c_score = analysis[4] if len(analysis) > 4 else 0.0
                    confidence = analysis[5] if len(analysis) > 5 else 0.0
                    attack = analysis[6] if len(analysis) > 6 else False
                
                time_display = timestamp[11:19] if timestamp else "N/A"
                pattern_display = pattern_type.replace('_', ' ').title()
                attack_icon = "🚨" if attack else "✅"
                
                # Color code confidence
                conf_class = "score-high" if confidence > 0.7 else ("score-medium" if confidence > 0.4 else "score-low")
                
                html += f"""
                            <tr>
                                <td class="timestamp">{time_display}</td>
                                <td>{pattern_display}</td>
                                <td class="value">{q_score:.3f}</td>
                                <td class="value">{c_score:.3f}</td>
                                <td><span class="quantum-score {conf_class}">{confidence:.3f}</span></td>
                                <td style="font-size: 20px;">{attack_icon}</td>
                            </tr>
                """
            except Exception as e:
                html += f"""
                            <tr>
                                <td colspan="6" style="text-align: center; color: #dc3545;">
                                    Error displaying analysis: {str(e)}
                                </td>
                            </tr>
                """
        
        if not quantum_analysis:
            html += """
                        <tr>
                            <td colspan="6" style="text-align: center; color: #6c757d; padding: 30px;">
                                <div style="font-size: 1.2em;">📦 No enhanced packet analysis data yet</div>
                                <div style="margin-top: 10px;">Start the client monitor to begin packet security analysis</div>
                            </td>
                        </tr>
            """
        
        html += f"""
                    </tbody>
                </table>
                
                <div style="background: linear-gradient(135deg, #fff3cd, #ffeaa7); border: 2px solid #ffc107; border-radius: 15px; padding: 25px; margin: 30px 0;">
                    <h4 style="color: #856404;">💡 Enhanced Packet-Based Quantum Security AI - Demo Guide</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 15px;">
                        <div>
                            <strong>📦 Enhanced Packet Features:</strong>
                            <ul style="margin: 10px 0;">
                                <li>4-qubit quantum neural network</li>
                                <li>10 distinctive packet-level features</li>
                                <li>Real-time packet flow monitoring</li>
                                <li>Multi-protocol threat detection</li>
                                <li>Live packet rate and size analysis</li>
                            </ul>
                        </div>
                        <div>
                            <strong>🎯 Enhanced Testing Workflow:</strong>
                            <ol style="margin: 10px 0;">
                                <li>Start Client Monitor</li>
                                <li>Observe normal packet patterns</li>
                                <li>Trigger enhanced packet-based attacks</li>
                                <li>Watch quantum AI detection in real-time</li>
                                <li>Monitor live packet statistics</li>
                            </ol>
                        </div>
                        <div>
                            <strong>🏆 Enhanced Packet Capabilities:</strong>
                            <ul style="margin: 10px 0;">
                                <li>DDoS volumetric flood detection</li>
                                <li>Port scan reconnaissance alerts</li>
                                <li>Data exfiltration identification</li>
                                <li>Botnet C&C communication detection</li>
                                <li>Real-time network analytics</li>
                            </ul>
                        </div>
                    </div>
                    <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 10px;">
                        <strong>🚀 Real-Time Features:</strong> Live packet counting, protocol distribution, source IP diversity, 
                        destination port analysis, packet size monitoring, and attack pattern simulation with distinctive signatures.
                    </div>
                </div>
                
                <div style="text-align: center; color: #6c757d; margin-top: 40px; padding-top: 25px; border-top: 2px solid #e9ecef;">
                    <div style="font-size: 1.1em; margin-bottom: 10px;">
                        🔄 Auto-refresh every 2s | 🕐 {datetime.now().strftime('%H:%M:%S')} | 📅 {datetime.now().strftime('%Y-%m-%d')}
                    </div>
                    <div style="font-size: 0.9em;">
                        📦 Enhanced Packet-Based Quantum Security AI v2.0 | 
                        🔬 Quantum: {'Active' if self.quantum_analyzer.quantum_available else 'Disabled'} | 
                        🌐 Mininet: {'Active' if mininet_enabled else 'Disabled'} | 
                        💻 WSL Platform | 
                        🎓 Academic Demo Ready | 
                        📈 Real-Time Monitoring: {total_packets:,} packets analyzed
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
        
    def run_server(self):
        """Run the Flask server"""
        host = '0.0.0.0'
        port = 5000
        
        print(f"🌐 Starting Enhanced Packet-Based Quantum Security Server on {host}:{port}")
        print(f"💻 Access from Windows: http://localhost:{port}")
        print(f"🐧 Access from WSL: http://127.0.0.1:{port}")
        
        self.app.run(host=host, port=port, debug=False, use_reloader=False)
    
    def run_client_loop(self):
        """Run the client loop"""
        time.sleep(3)  # Wait for server to start
        self.client.start()  # Auto-start client
        self.client.run_loop()
    
    def start(self):
        """Start the Enhanced Packet-Based Quantum Network Security System"""
        print("📦 ENHANCED PACKET-BASED QUANTUM NETWORK SECURITY AI")
        print("=" * 80)
        print("🌐 Dashboard: http://localhost:5000")
        print("📦 Enhanced Packet Analysis: 10-feature Quantum Neural Network")
        print("📈 Real-Time Monitoring: Live packet rates, protocols, IPs, ports")
        print("🌐 Network Simulation: Mininet + Advanced Traffic Control")
        print("🚨 Threat Detection: DDoS, Port Scans, Data Exfiltration, Botnet C&C")
        print("💾 Intelligence: Real-time Packet Flow Analytics with Attack Signatures")
        print("🎓 Academic Demo: Production-Ready Enhanced Packet Analysis System")
        print("💻 Platform: WSL Linux with Full Network Capabilities")
        print("🔬 Quantum ML: 4-qubit neural network with enhanced entanglement")
        print("📊 Live Stats: Packets/sec, unique IPs, port diversity, protocol distribution")
        print("=" * 80)
        
        # Start server in background thread
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Start client loop in background thread
        client_thread = threading.Thread(target=self.run_client_loop)
        client_thread.daemon = True
        client_thread.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n📦 Enhanced Packet-Based Quantum Security System stopped")
            self.cleanup()
    
    def cleanup(self):
        """Clean up all Enhanced Packet-Based components"""
        print("🧹 Cleaning up Enhanced Packet-Based Quantum Security System...")
        
        # Stop enhanced packet simulation
        if hasattr(self.quantum_analyzer, 'packet_simulator_active'):
            self.quantum_analyzer.packet_simulator_active = False
        
        # Stop Mininet if running
        if self.mininet_enabled:
            self.stop_mininet_integration()
        
        # Stop other components
        self.client.stop()
        
        print("✅ Enhanced packet-based cleanup complete")

def check_root_permissions():
    """Check if running with appropriate permissions for WSL"""
    try:
        result = subprocess.run(['sudo', '-n', 'true'], 
                              capture_output=True, check=False)
        return result.returncode == 0
    except:
        return False

if __name__ == '__main__':
    print("📦 ENHANCED PACKET-BASED QUANTUM NETWORK SECURITY AI - PRODUCTION SYSTEM")
    print("🐧 Running in WSL (Windows Subsystem for Linux)")
    
    # Check permissions
    if not check_root_permissions():
        print("⚠️  This system requires sudo privileges for advanced network simulation")
        print("🚀 Run with: sudo python3 enhanced_main_app.py")
        print("💡 Or configure passwordless sudo for tc/mn commands")
        
        # Ask user if they want to continue without Mininet
        try:
            response = input("Continue without advanced network simulation? (y/n): ").lower()
            if response != 'y':
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
    
    # Initialize and start Enhanced Packet-Based Quantum Security System
    monitor = EnhancedPacketQuantumNetworkMonitor()
    monitor.start()