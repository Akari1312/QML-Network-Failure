# better_network_demo.py - Server with controllable client
import sqlite3
import json
import threading
import time
import random
import signal
import sys
from datetime import datetime
from flask import Flask, request, jsonify
import requests

# =============================================================================
# SERVER COMPONENT (always stays running)
# =============================================================================

class NetworkMonitorServer:
    def __init__(self, db_path="network_monitor.db"):
        self.db_path = db_path
        self.setup_database()
        self.client_last_seen = None
        self.monitoring_active = True
        
        # Start background monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_client_health)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def setup_database(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main data table that client updates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_data (
                id INTEGER PRIMARY KEY,
                random_value REAL,
                timestamp TEXT,
                client_timestamp TEXT
            )
        ''')
        
        # Connection log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                timestamp TEXT,
                details TEXT
            )
        ''')
        
        # State snapshots table (create immediately)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_state_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                state_data TEXT
            )
        ''')
        
        # Initialize 5 entries if they don't exist
        cursor.execute("SELECT COUNT(*) FROM client_data")
        if cursor.fetchone()[0] == 0:
            for i in range(1, 6):
                cursor.execute(
                    "INSERT INTO client_data (id, random_value, timestamp, client_timestamp) VALUES (?, ?, ?, ?)",
                    (i, 0.0, datetime.now().isoformat(), datetime.now().isoformat())
                )
        
        conn.commit()
        conn.close()
        print("🗄️  Database initialized with 5 entries")
    
    def log_event(self, event_type, details=""):
        """Log connection events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO connection_log (event_type, timestamp, details) VALUES (?, ?, ?)",
            (event_type, datetime.now().isoformat(), details)
        )
        conn.commit()
        conn.close()
    
    def update_client_data(self, data):
        """Update the 5 entries with new data from client"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for entry in data:
            cursor.execute(
                "UPDATE client_data SET random_value = ?, timestamp = ?, client_timestamp = ? WHERE id = ?",
                (entry['random_value'], datetime.now().isoformat(), entry['client_timestamp'], entry['id'])
            )
        
        conn.commit()
        conn.close()
        
        # Update last seen time
        self.client_last_seen = datetime.now()
        print(f"📊 [SERVER] Updated {len(data)} entries from Client at {self.client_last_seen.strftime('%H:%M:%S')}")
    
    def monitor_client_health(self):
        """Background thread to monitor client connection health"""
        while self.monitoring_active:
            if self.client_last_seen:
                time_since_last = (datetime.now() - self.client_last_seen).total_seconds()
                
                # If no update for more than 15 seconds (3x the normal 5-second interval)
                if time_since_last > 15:
                    print(f"⚠️  [SERVER] Client connection lost! Last seen: {time_since_last:.1f} seconds ago")
                    self.log_event("CLIENT_DISCONNECTED", f"No updates for {time_since_last:.1f} seconds")
                    self.save_client_state()
                    # Reset to avoid spam
                    self.client_last_seen = None
            
            time.sleep(5)  # Check every 5 seconds
    
    def save_client_state(self):
        """Save current client state when connection is lost"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current state
        cursor.execute("SELECT * FROM client_data")
        current_state = cursor.fetchall()
        
        # Save state snapshot
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_state_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                state_data TEXT
            )
        ''')
        
        state_json = json.dumps([{
            'id': row[0], 
            'random_value': row[1], 
            'timestamp': row[2],
            'client_timestamp': row[3]
        } for row in current_state])
        
        cursor.execute(
            "INSERT INTO client_state_snapshots (timestamp, state_data) VALUES (?, ?)",
            (datetime.now().isoformat(), state_json)
        )
        
        conn.commit()
        conn.close()
        print("💾 [SERVER] Client state saved!")
    
    def get_status(self):
        """Get current system status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current data
        cursor.execute("SELECT * FROM client_data ORDER BY id")
        current_data = cursor.fetchall()
        
        # Get recent logs
        cursor.execute("SELECT * FROM connection_log ORDER BY timestamp DESC LIMIT 10")
        recent_logs = cursor.fetchall()
        
        # Get saved snapshots (with error handling)
        try:
            cursor.execute("SELECT * FROM client_state_snapshots ORDER BY timestamp DESC LIMIT 5")
            snapshots = cursor.fetchall()
        except sqlite3.OperationalError:
            # Table doesn't exist yet
            snapshots = []
        
        conn.close()
        
        return {
            'current_data': current_data,
            'recent_logs': recent_logs,
            'saved_snapshots': snapshots,
            'client_last_seen': self.client_last_seen.isoformat() if self.client_last_seen else None,
            'status': 'connected' if self.client_last_seen and (datetime.now() - self.client_last_seen).total_seconds() < 10 else 'disconnected'
        }

# =============================================================================
# CLIENT COMPONENT (controllable)
# =============================================================================

class NetworkClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.running = False
        self.update_interval = 5
        self.failed_attempts = 0
    
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
            
            print(f"📤 [CLIENT] Sending update at {datetime.now().strftime('%H:%M:%S')}")
            
            response = requests.post(
                f"{self.server_url}/update",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ [CLIENT] Update successful")
                self.failed_attempts = 0
                return True
            else:
                print(f"❌ [CLIENT] Server returned {response.status_code}")
                self.failed_attempts += 1
                return False
                
        except Exception as e:
            print(f"💥 [CLIENT] Error: {e}")
            self.failed_attempts += 1
            return False
    
    def start(self):
        """Start the client"""
        self.running = True
        print("🔄 [CLIENT] Starting...")
    
    def stop(self):
        """Stop the client"""
        self.running = False
        print("🛑 [CLIENT] Stopped - simulating network failure!")
    
    def run_loop(self):
        """Client update loop"""
        while True:
            if self.running:
                self.send_update()
            time.sleep(self.update_interval)

# =============================================================================
# FLASK WEB SERVER WITH CONTROL
# =============================================================================

app = Flask(__name__)
server = NetworkMonitorServer()
client = NetworkClient()

@app.route('/')
def home():
    """Dashboard with client control"""
    status_data = server.get_status()
    
    current_data = status_data['current_data']
    recent_logs = status_data['recent_logs']
    snapshots = status_data['saved_snapshots']
    
    status = status_data['status']
    status_color = "#28a745" if status == "connected" else "#dc3545"
    status_icon = "🟢" if status == "connected" else "🔴"
    
    last_seen = status_data['client_last_seen']
    if last_seen:
        last_time = datetime.fromisoformat(last_seen)
        time_diff = (datetime.now() - last_time).total_seconds()
        last_seen_display = f"{last_time.strftime('%H:%M:%S')} ({time_diff:.1f}s ago)"
    else:
        last_seen_display = "Never"
    
    client_status = "🟢 RUNNING" if client.running else "🔴 STOPPED"
    client_color = "#28a745" if client.running else "#dc3545"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Network Monitor Dashboard</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                padding: 30px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }}
            .status-card {{
                background: {status_color};
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }}
            .control-panel {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: center;
            }}
            .client-status {{
                background: {client_color};
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                display: inline-block;
                margin: 10px;
                font-weight: bold;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }}
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #eee;
            }}
            tr:hover {{
                background: #f8f9fa;
            }}
            .value {{
                font-family: 'Courier New', monospace;
                font-weight: bold;
                color: #007bff;
            }}
            .timestamp {{
                color: #6c757d;
                font-size: 0.9em;
            }}
            .section-title {{
                font-size: 24px;
                margin: 30px 0 15px 0;
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }}
            .btn {{
                background: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
            }}
            .btn:hover {{
                background: #0056b3;
            }}
            .btn-danger {{
                background: #dc3545;
            }}
            .btn-danger:hover {{
                background: #c82333;
            }}
            .btn-success {{
                background: #28a745;
            }}
            .btn-success:hover {{
                background: #218838;
            }}
        </style>
        <script>
            function autoRefresh() {{
                setTimeout(function(){{
                    window.location.reload();
                }}, 3000);
            }}
            window.onload = autoRefresh;
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Network Monitor Dashboard</h1>
                <p>Quantum-Enhanced Network Failure Detection Demo</p>
            </div>
            
            <div class="status-card">
                {status_icon} Server Status: {status.upper()} | Last Update: {last_seen_display}
            </div>
            
            <div class="control-panel">
                <h3>🎮 Client Control Panel</h3>
                <div class="client-status">{client_status}</div><br>
                <a href="/start_client" class="btn btn-success">▶️ Start Client</a>
                <a href="/stop_client" class="btn btn-danger">⏹️ Stop Client (Simulate Failure)</a>
                <a href="/" class="btn">🔄 Refresh</a>
            </div>
            
            <h2 class="section-title">📊 Current Data (5 Entries)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Entry ID</th>
                        <th>Random Value</th>
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
                        <td><strong>#{entry_id}</strong></td>
                        <td class="value">{value:.2f}</td>
                        <td class="timestamp">{server_display}</td>
                        <td class="timestamp">{client_display}</td>
                    </tr>
        """
    
    html += """
                </tbody>
            </table>
            
            <h2 class="section-title">📋 Recent Connection Events</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Event Type</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add recent logs
    for log in recent_logs:
        log_id, event_type, timestamp, details = log
        time_display = timestamp[11:19] if timestamp else "N/A"
        
        if "UPDATE" in event_type:
            event_color = "#28a745"
            event_icon = "✅"
        elif "DISCONNECTED" in event_type:
            event_color = "#dc3545"
            event_icon = "⚠️"
        else:
            event_color = "#007bff"
            event_icon = "ℹ️"
        
        html += f"""
                    <tr>
                        <td class="timestamp">{time_display}</td>
                        <td style="color: {event_color}; font-weight: bold;">{event_icon} {event_type}</td>
                        <td>{details}</td>
                    </tr>
        """
    
    # Add saved snapshots section
    html += """
                </tbody>
            </table>
            
            <h2 class="section-title">💾 Saved State Snapshots</h2>
            <table>
                <thead>
                    <tr>
                        <th>Snapshot Time</th>
                        <th>Entries Saved</th>
                        <th>Trigger Reason</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    if snapshots:
        for snapshot in snapshots:
            snap_id, snap_time, snap_data = snapshot
            time_display = snap_time[11:19] if snap_time else "N/A"
            state_data = json.loads(snap_data)
            entries_count = len(state_data)
            
            html += f"""
                        <tr>
                            <td class="timestamp">{time_display}</td>
                            <td class="value">{entries_count} entries</td>
                            <td>Client disconnection detected</td>
                        </tr>
            """
    else:
        html += """
                        <tr>
                            <td colspan="3" style="text-align: center; color: #6c757d;">
                                No state snapshots saved yet. Stop the client to see state saving in action!
                            </td>
                        </tr>
        """
    
    html += f"""
                </tbody>
            </table>
            
            <div style="text-align: center; color: #6c757d; margin-top: 30px;">
                <p>🔄 Auto-refreshing every 3 seconds | Last updated: {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/update', methods=['POST'])
def receive_update():
    """Endpoint for client to send updates"""
    try:
        data = request.json
        server.update_client_data(data)
        server.log_event("CLIENT_UPDATE", f"Received {len(data)} entries")
        return jsonify({'status': 'success', 'message': 'Data updated'})
    except Exception as e:
        print(f"❌ [SERVER] Error processing update: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/start_client')
def start_client():
    """Start the client"""
    client.start()
    server.log_event("CLIENT_STARTED", "Client manually started via web interface")
    return f'<script>window.location.href="/"</script>'

@app.route('/stop_client')
def stop_client():
    """Stop the client to simulate failure"""
    client.stop()
    server.log_event("CLIENT_MANUALLY_STOPPED", "Client manually stopped to simulate network failure")
    return f'<script>window.location.href="/"</script>'

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_server():
    """Run the Flask server"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def run_client_loop():
    """Run the client loop"""
    time.sleep(2)  # Wait for server to start
    client.start()  # Auto-start client
    client.run_loop()

if __name__ == '__main__':
    print("🚀 Network Monitor Demo with State Saving")
    print("=" * 50)
    print("🌐 Server: http://localhost:5000")
    print("💡 Use the web interface to start/stop client")
    print("📊 Watch state saving when client disconnects!")
    print("=" * 50)
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Start client loop in background thread
    client_thread = threading.Thread(target=run_client_loop)
    client_thread.daemon = True
    client_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped")
        sys.exit(0)