# simplified_main_app.py - SIMPLIFIED WITH BASIC ATTACKS ONLY
import threading
import time
import sys
import json
import subprocess
import os
from datetime import datetime
from flask import Flask, request, jsonify

# Import simplified components
try:
    from quantum_analyzer_simplified_fixed import EnhancedPacketQuantumSecurityAI as QuantumNetworkAnalyzer
    from attack_simulator import NetworkAttackSimulator
    from quantum_server_fixed import QuantumNetworkMonitorServer
    from quantum_client_fixed import QuantumNetworkClient
    QUANTUM_IMPORTS = True
    print("✅ Simplified Quantum Security AI loaded!")
except ImportError as e:
    print(f"❌ Critical import error: {e}")
    sys.exit(1)

class SimplifiedPacketQuantumNetworkMonitor:
    def __init__(self):
        print("📦 Initializing Simplified Quantum Network Security System...")
        
        # Initialize components
        self.quantum_analyzer = QuantumNetworkAnalyzer()
        self.server = QuantumNetworkMonitorServer(self.quantum_analyzer)
        
        # Create client and attack simulator
        self.attack_simulator = NetworkAttackSimulator(None)
        self.client = QuantumNetworkClient(self.attack_simulator)
        self.attack_simulator.client = self.client
        
        # Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        print("✅ Simplified Quantum Security System initialized")
        
    def setup_routes(self):
        """Setup Flask routes - SIMPLIFIED VERSION"""
        
        @self.app.route('/')
        def quantum_dashboard():
            try:
                return self.render_simplified_dashboard()
            except Exception as e:
                print(f"❌ Dashboard error: {e}")
                return f"<h1>Dashboard Error</h1><p>{str(e)}</p>", 500
        
        @self.app.route('/update', methods=['POST'])
        def receive_update():
            try:
                data = request.json
                if not data:
                    return jsonify({'status': 'error', 'message': 'No data received'}), 400
                
                self.server.update_client_data(data)
                self.server.log_event("CLIENT_UPDATE", f"Received {len(data)} entries")
                return jsonify({'status': 'success', 'message': 'Data updated'})
            except Exception as e:
                print(f"❌ [SERVER] Error processing update: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        # Client control routes
        @self.app.route('/start_client')
        def start_client():
            try:
                self.client.start()
                self.server.log_event("CLIENT_STARTED", "Client started")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error starting client: {e}", 500
        
        @self.app.route('/stop_client')
        def stop_client():
            try:
                self.client.stop()
                self.server.log_event("CLIENT_STOPPED", "Client stopped")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error stopping client: {e}", 500
        
        # SIMPLIFIED: Only basic attack simulations
        @self.app.route('/simulate_ddos')
        def simulate_ddos():
            try:
                self.enhanced_attack_simulation('ddos_volumetric')
                self.server.log_event("DDOS_SIMULATION", "DDoS attack simulation started")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error simulating DDoS: {e}", 500
        
        @self.app.route('/simulate_portscan')
        def simulate_portscan():
            try:
                self.enhanced_attack_simulation('port_scan')
                self.server.log_event("PORTSCAN_SIMULATION", "Port scan simulation started")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error simulating port scan: {e}", 500
        
        @self.app.route('/simulate_exfiltration')
        def simulate_exfiltration():
            try:
                self.enhanced_attack_simulation('data_exfiltration')
                self.server.log_event("EXFILTRATION_SIMULATION", "Data exfiltration simulation started")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error simulating exfiltration: {e}", 500
        
        @self.app.route('/stop_attack')
        def stop_attack():
            try:
                self.enhanced_stop_attack()
                self.server.log_event("ATTACK_STOPPED", "Attack simulation stopped")
                return '<script>window.location.href="/"</script>'
            except Exception as e:
                return f"Error stopping attack: {e}", 500
        
        # Analytics route
        @self.app.route('/packet_analytics')
        def packet_analytics():
            try:
                analytics = self.quantum_analyzer.get_enterprise_analytics()
                return jsonify(analytics)
            except Exception as e:
                return jsonify({'error': f'Analytics not available: {e}'}), 500
        
        # Attack prediction API endpoint
        @self.app.route('/api/attack_prediction')
        def attack_prediction_api():
            try:
                analysis = self.quantum_analyzer.analyze_current_pattern()
                return jsonify({
                    'predicted_attack': analysis.get('predicted_attack_type', 'unknown'),
                    'confidence': analysis.get('attack_confidence', 0.0),
                    'probability_scores': analysis.get('attack_probability_scores', {}),
                    'attack_details': analysis.get('attack_details', {}),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def enhanced_attack_simulation(self, attack_type):
        """Start attack simulation"""
        print(f"🎯 Starting {attack_type} attack simulation")
        
        # Set attack mode
        if hasattr(self.quantum_analyzer, 'set_attack_mode'):
            self.quantum_analyzer.set_attack_mode(attack_type)
        
        # Apply application-level attack simulation
        if attack_type == 'ddos_volumetric':
            self.attack_simulator.start_dos_attack()
        elif attack_type == 'port_scan':
            self.attack_simulator.start_flooding_attack()
        elif attack_type == 'data_exfiltration':
            self.attack_simulator.start_congestion_attack()
    
    def enhanced_stop_attack(self):
        """Stop all attack simulations"""
        print("✅ Stopping all attack simulations...")
        
        # Stop packet simulation
        if hasattr(self.quantum_analyzer, 'set_attack_mode'):
            self.quantum_analyzer.set_attack_mode(None)
        
        # Stop application-level attacks
        self.attack_simulator.stop_attack()
    
    def get_enhanced_status(self):
        """Get system status"""
        try:
            # Get base status
            status_data = self.server.get_status()
            
            # Add analytics
            try:
                packet_analytics = self.quantum_analyzer.get_enterprise_analytics()
                status_data['packet_analytics'] = packet_analytics
            except Exception as e:
                print(f"Warning: Could not get packet analytics: {e}")
                status_data['packet_analytics'] = {}
            
            # Add attack prediction
            try:
                analysis = self.quantum_analyzer.analyze_current_pattern()
                status_data['attack_prediction'] = {
                    'predicted_attack': analysis.get('predicted_attack_type', 'unknown'),
                    'confidence': analysis.get('attack_confidence', 0.0),
                    'probability_scores': analysis.get('attack_probability_scores', {}),
                    'attack_details': analysis.get('attack_details', {})
                }
            except Exception as e:
                print(f"Warning: Could not get attack prediction: {e}")
                status_data['attack_prediction'] = {}
            
            return status_data
        except Exception as e:
            print(f"❌ Error getting status: {e}")
            return {
                'current_data': [],
                'recent_logs': [],
                'quantum_analysis': [],
                'saved_snapshots': [],
                'client_last_seen': None,
                'status': 'error',
                'packet_analytics': {},
                'attack_prediction': {},
                'error': str(e)
            }
    
    def render_simplified_dashboard(self):
        """Render simplified dashboard"""
        try:
            status_data = self.get_enhanced_status()
            
            current_data = status_data.get('current_data', [])
            attack_prediction = status_data.get('attack_prediction', {})
            
            # Get packet analytics
            try:
                packet_analytics = status_data.get('packet_analytics', {})
                model_info = packet_analytics.get('model_info', {})
                real_time_metrics = packet_analytics.get('real_time_metrics', {})
                
                # Extract stats
                total_packets = real_time_metrics.get('total_packets', 0)
                packets_per_second = real_time_metrics.get('packets_per_second', 0)
                unique_ips = real_time_metrics.get('unique_src_ips', 0)
                unique_ports = real_time_metrics.get('unique_dst_ports', 0)
                avg_packet_size = real_time_metrics.get('avg_packet_size', 0)
                protocol_dist = real_time_metrics.get('protocol_distribution', {})
                attack_mode = real_time_metrics.get('attack_mode', 'normal')
                
                model_accuracy = model_info.get('model_accuracy', 0) * 100
                attack_types_supported = model_info.get('attack_types_supported', 0)
                
            except Exception as e:
                print(f"Warning: Error getting analytics: {e}")
                total_packets = 0
                packets_per_second = 0
                unique_ips = 0
                unique_ports = 0
                avg_packet_size = 0
                protocol_dist = {}
                attack_mode = 'normal'
                model_accuracy = 0
                attack_types_supported = 0
            
            # Extract attack prediction
            predicted_attack = attack_prediction.get('predicted_attack', 'unknown')
            attack_confidence = attack_prediction.get('confidence', 0.0)
            probability_scores = attack_prediction.get('probability_scores', {})
            attack_details = attack_prediction.get('attack_details', {})
            
            status = status_data.get('status', 'unknown')
            status_icon = "🟢" if status == "connected" else "🔴"
            
            client_status = "🟢 RUNNING" if self.client.running else "🔴 STOPPED"
            attack_status = "🚨 ACTIVE" if self.attack_simulator.attack_active else "✅ NONE"
            
            # Protocol display
            protocol_display = ", ".join([f"{k}: {v}" for k, v in protocol_dist.items()]) if protocol_dist else "No protocols detected"
            
            # Attack details
            attack_description = attack_details.get('description', 'No specific attack detected')
            attack_severity = attack_details.get('severity', 'LOW')
            attack_mitigation = attack_details.get('mitigation', 'Continue normal monitoring')
            
            # Severity colors
            severity_colors = {
                'LOW': '#28a745',
                'MEDIUM': '#ffc107', 
                'HIGH': '#fd7e14',
                'CRITICAL': '#dc3545'
            }
            severity_color = severity_colors.get(attack_severity, '#6c757d')
            
            # Top 3 scores
            top_scores = sorted(probability_scores.items(), key=lambda x: x[1], reverse=True)[:3] if probability_scores else []
            
            # HTML Dashboard
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>🎯 Simplified Quantum Security AI</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #333; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); }}
                    .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #667eea; }}
                    .header h1 {{ color: #667eea; font-size: 2.2em; margin: 0; }}
                    .prediction-banner {{ background: linear-gradient(135deg, {severity_color}, {severity_color}dd); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }}
                    .prediction-title {{ font-size: 1.6em; font-weight: bold; margin-bottom: 10px; }}
                    .prediction-details {{ font-size: 1.0em; opacity: 0.9; }}
                    .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
                    .status-card {{ padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
                    .card-green {{ background: linear-gradient(135deg, #28a745, #20c997); }}
                    .card-red {{ background: linear-gradient(135deg, #dc3545, #e74c3c); }}
                    .card-blue {{ background: linear-gradient(135deg, #007bff, #0056b3); }}
                    .metric-box {{ background: linear-gradient(135deg, #f8f9fa, #e9ecef); border: 2px solid #dee2e6; border-radius: 10px; padding: 20px; margin: 15px 0; }}
                    .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; }}
                    .metric-item {{ background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
                    .metric-value {{ font-size: 1.6em; font-weight: bold; color: #667eea; }}
                    .metric-label {{ color: #6c757d; margin-top: 5px; }}
                    .probability-scores {{ margin: 15px 0; }}
                    .score-item {{ display: inline-block; margin: 5px; padding: 8px 15px; background: #f8f9fa; border-radius: 20px; border: 2px solid #dee2e6; }}
                    .score-high {{ border-color: #dc3545; background: #f8d7da; }}
                    .score-medium {{ border-color: #ffc107; background: #fff3cd; }}
                    .score-low {{ border-color: #28a745; background: #d4edda; }}
                    .control-panel {{ background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 25px; border-radius: 10px; margin: 20px 0; }}
                    .control-section {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 8px; vertical-align: top; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
                    .btn {{ background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 10px 16px; border: none; border-radius: 8px; text-decoration: none; margin: 5px; display: inline-block; font-weight: bold; transition: all 0.3s; }}
                    .btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
                    .btn-danger {{ background: linear-gradient(135deg, #dc3545, #c82333); }}
                    .btn-success {{ background: linear-gradient(135deg, #28a745, #1e7e34); }}
                    .btn-warning {{ background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529; }}
                    .btn-info {{ background: linear-gradient(135deg, #17a2b8, #138496); }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                    th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #dee2e6; }}
                    th {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; font-weight: bold; }}
                    tr:hover {{ background: #f8f9fa; }}
                </style>
                <script>
                    function autoRefresh() {{
                        setTimeout(function(){{ window.location.reload(); }}, 3000);
                    }}
                    window.onload = autoRefresh;
                </script>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎯 Simplified Quantum Security AI</h1>
                        <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 1.1em;">
                            Real-Time Attack Detection & Network Security Analysis
                        </p>
                        <div style="margin-top: 15px;">
                            <span style="background: #667eea; color: white; padding: 5px 15px; border-radius: 15px; font-weight: bold;">
                                🔬 Quantum ML • 🎯 {attack_types_supported} Attack Types • 📊 {model_accuracy:.1f}% Accuracy
                            </span>
                        </div>
                    </div>
                    
                    <div class="prediction-banner">
                        <div class="prediction-title">
                            🎯 DETECTED: {predicted_attack.replace('_', ' ').upper()}
                        </div>
                        <div class="prediction-details">
                            Confidence: {attack_confidence:.1%} | Severity: {attack_severity} | {attack_description}
                        </div>
                    </div>
                    
                    <div class="metric-box">
                        <h3 style="color: #667eea; margin-bottom: 15px;">📈 Real-Time Packet Monitoring</h3>
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
                        </div>
                        <div style="margin-top: 15px; padding: 15px; background: white; border-radius: 8px;">
                            <strong>Protocol Distribution:</strong> {protocol_display}
                        </div>
                    </div>
                    
                    <div class="metric-box">
                        <h3 style="color: #667eea; margin-bottom: 15px;">🎯 Attack Probability Scores</h3>
                        <div class="probability-scores">
            """
            
            # Add probability scores
            for attack_type, score in top_scores:
                score_class = 'score-high' if score > 0.7 else ('score-medium' if score > 0.3 else 'score-low')
                display_name = attack_type.replace('_', ' ').title()
                html += f"""
                    <div class="score-item {score_class}">
                        <strong>{display_name}:</strong> {score:.1%}
                    </div>
                """
            
            if not top_scores:
                html += '<div class="score-item">No attack probabilities calculated yet</div>'
            
            html += f"""
                        </div>
                        <div style="margin-top: 15px; padding: 15px; background: white; border-radius: 8px;">
                            <strong>Recommended Action:</strong> {attack_mitigation}
                        </div>
                    </div>
                    
                    <div class="status-grid">
                        <div class="status-card card-{'green' if status == 'connected' else 'red'}">
                            {status_icon} Server<br>{status.upper()}
                        </div>
                        <div class="status-card card-{'green' if self.client.running else 'red'}">
                            📡 Client<br>{client_status}
                        </div>
                        <div class="status-card card-{'red' if self.attack_simulator.attack_active else 'green'}">
                            🚨 Attack Sim<br>{attack_status}
                        </div>
                        <div class="status-card card-blue">
                            🎯 AI Detection<br>✅ ONLINE
                        </div>
                    </div>
                    
                    <div class="control-panel">
                        <h3 style="color: #667eea;">🎯 Simplified Attack Simulation Control</h3>
                        
                        <div class="control-section">
                            <h4>Client Operations</h4>
                            <a href="/start_client" class="btn btn-success">▶️ Start Monitor</a>
                            <a href="/stop_client" class="btn btn-danger">⏹️ Stop Monitor</a>
                        </div>
                        
                        <div class="control-section">
                            <h4>Basic Attack Simulations</h4>
                            <a href="/simulate_ddos" class="btn btn-danger">💥 DDoS Attack</a>
                            <a href="/simulate_portscan" class="btn btn-warning">🔍 Port Scan</a>
                            <a href="/simulate_exfiltration" class="btn btn-warning">📤 Data Theft</a>
                            <a href="/stop_attack" class="btn btn-success">✅ Stop Attack</a>
                        </div>
                        
                        <div class="control-section">
                            <h4>System Tools</h4>
                            <a href="/" class="btn">🔄 Refresh</a>
                            <a href="/packet_analytics" class="btn btn-info" target="_blank">📊 Analytics</a>
                            <a href="/api/attack_prediction" class="btn btn-info" target="_blank">🎯 API</a>
                        </div>
                    </div>
                    
                    <h3 style="color: #667eea;">📊 Current Network Data</h3>
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
            
            # Add data rows
            try:
                for row in current_data[:5]:
                    if len(row) >= 4:
                        entry_id, value, server_time, client_time = row[:4]
                        server_display = server_time[11:19] if server_time else "N/A"
                        client_display = client_time[11:19] if client_time else "N/A"
                        
                        html += f"""
                            <tr>
                                <td><strong>Monitor #{entry_id}</strong></td>
                                <td style="font-weight: bold; color: #667eea;">{value:.2f}</td>
                                <td>{server_display}</td>
                                <td>{client_display}</td>
                            </tr>
                        """
            except Exception as e:
                html += f"""
                    <tr>
                        <td colspan="4" style="text-align: center; color: #dc3545;">Error displaying data: {str(e)}</td>
                    </tr>
                """
            
            if not current_data:
                html += """
                    <tr>
                        <td colspan="4" style="text-align: center; color: #6c757d;">No data available - Start the client monitor</td>
                    </tr>
                """
            
            html += f"""
                        </tbody>
                    </table>
                    
                    <div style="background: linear-gradient(135deg, #fff3cd, #ffeaa7); border: 2px solid #ffc107; border-radius: 10px; padding: 20px; margin: 25px 0;">
                        <h4 style="color: #856404;">💡 Simplified Attack Detection Demo</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 15px;">
                            <div>
                                <strong>🎯 Attack Types:</strong>
                                <ul style="margin: 10px 0;">
                                    <li>DDoS Volumetric Floods</li>
                                    <li>Port Scan Attacks</li>
                                    <li>Data Exfiltration</li>
                                </ul>
                            </div>
                            <div>
                                <strong>🔬 AI Features:</strong>
                                <ul style="margin: 10px 0;">
                                    <li>8 packet analysis features</li>
                                    <li>Real-time probability scoring</li>
                                    <li>Quantum + Classical ML</li>
                                    <li>Automated threat classification</li>
                                </ul>
                            </div>
                            <div>
                                <strong>🎮 How to Test:</strong>
                                <ol style="margin: 10px 0;">
                                    <li>Start the client monitor</li>
                                    <li>Click an attack simulation button</li>
                                    <li>Watch AI detect the attack type</li>
                                    <li>See probability scores update</li>
                                </ol>
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; color: #6c757d; margin-top: 30px; padding-top: 20px; border-top: 2px solid #dee2e6;">
                        <div style="font-size: 1.1em; margin-bottom: 10px;">
                            🔄 Auto-refresh every 3s | 🕐 {datetime.now().strftime('%H:%M:%S')} | 📅 {datetime.now().strftime('%Y-%m-%d')}
                        </div>
                        <div style="font-size: 0.9em;">
                            🎯 Simplified Quantum Security AI v1.0 | 
                            🔬 Quantum ML: {'Active' if self.quantum_analyzer.quantum_available else 'Classical'} | 
                            📈 Live Analysis: {total_packets:,} packets processed |
                            🛡️ Current Threat: {attack_severity}
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            print(f"❌ Error rendering dashboard: {e}")
            import traceback
            traceback.print_exc()
            
            return f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>🎯 Dashboard Error</h1>
                <p style="color: #dc3545;">Error: {str(e)}</p>
                <p><a href="/" style="color: #007bff;">Try Again</a></p>
            </body>
            </html>
            """
    
    def run_server(self):
        """Run the Flask server"""
        host = '0.0.0.0'
        port = 5000
        
        print(f"🌐 Starting Simplified Quantum Security Server on {host}:{port}")
        print(f"💻 Access: http://localhost:{port}")
        
        try:
            self.app.run(host=host, port=port, debug=False, use_reloader=False)
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def run_client_loop(self):
        """Run the client loop"""
        time.sleep(3)
        try:
            self.client.start()
            self.client.run_loop()
        except Exception as e:
            print(f"❌ Client loop error: {e}")
    
    def start(self):
        """Start the system"""
        print("🎯 SIMPLIFIED QUANTUM SECURITY AI")
        print("=" * 60)
        print("🌐 Dashboard: http://localhost:5000")
        print("🎯 Attack Detection: DDoS, Port Scan, Data Exfiltration")
        print("🔬 Quantum ML: Real-time threat classification")
        print("🎮 Demo Ready: Try the attack simulations!")
        print("=" * 60)
        
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
            print("\n🎯 Simplified Quantum Security System stopped")
            self.cleanup()
    
    def cleanup(self):
        """Clean up components"""
        print("🧹 Cleaning up system...")
        
        # Stop packet simulation
        if hasattr(self.quantum_analyzer, 'packet_simulator_active'):
            self.quantum_analyzer.packet_simulator_active = False
        
        # Stop client
        self.client.stop()
        
        print("✅ Cleanup complete")

if __name__ == '__main__':
    print("🎯 SIMPLIFIED QUANTUM SECURITY AI - BASIC ATTACKS ONLY")
    print("🐧 Running in WSL (Windows Subsystem for Linux)")
    
    # Initialize and start system
    monitor = SimplifiedPacketQuantumNetworkMonitor()
    monitor.start()