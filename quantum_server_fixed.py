# quantum_server_fixed.py - Fixed Enhanced Server
import sqlite3
import json
import threading
import time
from datetime import datetime
from collections import deque

class QuantumNetworkMonitorServer:
    def __init__(self, quantum_analyzer, db_path="quantum_network_monitor.db"):
        self.db_path = db_path
        self.quantum_analyzer = quantum_analyzer
        self.client_last_seen = None
        self.monitoring_active = True
        
        # Attack detection
        self.attack_history = deque(maxlen=20)
        self.state_snapshots = []
        
        # Setup database with error handling
        try:
            self.setup_database()
        except Exception as e:
            print(f"❌ Database setup error: {e}")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_client_health, daemon=True)
        self.monitor_thread.start()
    
    def setup_database(self):
        """Initialize the SQLite database with quantum analysis tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Main data table
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
            
            # Quantum analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantum_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    pattern_type TEXT,
                    quantum_score REAL,
                    classical_score REAL,
                    confidence REAL,
                    attack_detected BOOLEAN,
                    features TEXT
                )
            ''')
            
            # State snapshots table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_state_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    state_data TEXT,
                    trigger_reason TEXT,
                    quantum_analysis TEXT
                )
            ''')
            
            # Initialize 5 entries if empty
            cursor.execute("SELECT COUNT(*) FROM client_data")
            if cursor.fetchone()[0] == 0:
                for i in range(1, 6):
                    cursor.execute(
                        "INSERT INTO client_data (id, random_value, timestamp, client_timestamp) VALUES (?, ?, ?, ?)",
                        (i, 0.0, datetime.now().isoformat(), datetime.now().isoformat())
                    )
            
            conn.commit()
            conn.close()
            print("🗄️  Quantum database initialized")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            # Create minimal fallback
            self._create_fallback_database()
    
    def _create_fallback_database(self):
        """Create minimal database if main setup fails"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_data (
                    id INTEGER PRIMARY KEY,
                    random_value REAL,
                    timestamp TEXT,
                    client_timestamp TEXT
                )
            ''')
            
            # Add basic entries
            for i in range(1, 6):
                cursor.execute(
                    "INSERT OR REPLACE INTO client_data (id, random_value, timestamp, client_timestamp) VALUES (?, ?, ?, ?)",
                    (i, 0.0, datetime.now().isoformat(), datetime.now().isoformat())
                )
            
            conn.commit()
            conn.close()
            print("🗄️  Fallback database created")
            
        except Exception as e:
            print(f"❌ Fallback database error: {e}")
    
    def log_event(self, event_type, details=""):
        """Log connection events with error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='connection_log'")
            if cursor.fetchone():
                cursor.execute(
                    "INSERT INTO connection_log (event_type, timestamp, details) VALUES (?, ?, ?)",
                    (event_type, datetime.now().isoformat(), details)
                )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Log event error: {e}")
    
    def update_client_data(self, data):
        """Update client data and perform quantum analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for entry in data:
                cursor.execute(
                    "UPDATE client_data SET random_value = ?, timestamp = ?, client_timestamp = ? WHERE id = ?",
                    (entry['random_value'], datetime.now().isoformat(), entry['client_timestamp'], entry['id'])
                )
            
            conn.commit()
            conn.close()
            
            # Update timing for quantum analysis
            self.client_last_seen = datetime.now()
            
            # Perform quantum analysis with error handling
            try:
                if hasattr(self.quantum_analyzer, 'update_timing'):
                    self.quantum_analyzer.update_timing(data[0]['client_timestamp'])
                
                analysis = self.quantum_analyzer.analyze_current_pattern()
                self.store_quantum_analysis(analysis)
                
                # Check for attacks
                if analysis.get('attack_detected', False):
                    self.handle_attack_detection(analysis)
                
                print(f"📊 [SERVER] Updated {len(data)} entries | Risk: {analysis.get('confidence', 0):.2f}")
                
            except Exception as e:
                print(f"❌ Quantum analysis error: {e}")
            
        except Exception as e:
            print(f"❌ [SERVER] Update error: {e}")
    
    def store_quantum_analysis(self, analysis):
        """Store quantum analysis results with error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quantum_analysis'")
            if cursor.fetchone():
                cursor.execute('''
                    INSERT INTO quantum_analysis 
                    (timestamp, pattern_type, quantum_score, classical_score, confidence, attack_detected, features)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    analysis.get('pattern_type', 'unknown'),
                    analysis.get('quantum_score', 0.0),
                    analysis.get('classical_score', 0.0),
                    analysis.get('confidence', 0.0),
                    analysis.get('attack_detected', False),
                    json.dumps(analysis.get('features', []))
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Store analysis error: {e}")
    
    def handle_attack_detection(self, analysis):
        """Handle detected attacks"""
        try:
            attack_type = analysis.get('pattern_type', 'unknown')
            confidence = analysis.get('confidence', 0.0)
            
            print(f"🚨 [QUANTUM] Attack detected: {attack_type} (confidence: {confidence:.2f})")
            
            # Log attack
            self.log_event("ATTACK_DETECTED", f"{attack_type} - confidence: {confidence:.2f}")
            
            # Save state if high confidence attack
            if confidence > 0.8:
                self.save_client_state(f"High confidence {attack_type} attack", analysis)
                
        except Exception as e:
            print(f"❌ Attack handling error: {e}")
    
    def save_client_state(self, reason, quantum_analysis=None):
        """Save current client state with quantum analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current state
            cursor.execute("SELECT * FROM client_data")
            current_state = cursor.fetchall()
            
            state_json = json.dumps([{
                'id': row[0], 
                'random_value': row[1], 
                'timestamp': row[2],
                'client_timestamp': row[3]
            } for row in current_state])
            
            quantum_json = json.dumps(quantum_analysis) if quantum_analysis else None
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='client_state_snapshots'")
            if cursor.fetchone():
                cursor.execute(
                    "INSERT INTO client_state_snapshots (timestamp, state_data, trigger_reason, quantum_analysis) VALUES (?, ?, ?, ?)",
                    (datetime.now().isoformat(), state_json, reason, quantum_json)
                )
            
            conn.commit()
            conn.close()
            print(f"💾 [SERVER] State saved: {reason}")
            
        except Exception as e:
            print(f"❌ Save state error: {e}")
    
    def monitor_client_health(self):
        """Background monitoring with quantum analysis"""
        while self.monitoring_active:
            try:
                if self.client_last_seen:
                    time_since_last = (datetime.now() - self.client_last_seen).total_seconds()
                    
                    if time_since_last > 15:
                        print(f"⚠️  [SERVER] Client connection lost! Last seen: {time_since_last:.1f}s ago")
                        self.log_event("CLIENT_DISCONNECTED", f"No updates for {time_since_last:.1f} seconds")
                        self.save_client_state("Connection timeout detected")
                        self.client_last_seen = None
                
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(5)
    
    def get_status(self):
        """Get comprehensive status including quantum analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current data
            cursor.execute("SELECT * FROM client_data ORDER BY id")
            current_data = cursor.fetchall()
            
            # Get recent logs with error handling
            recent_logs = []
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='connection_log'")
                if cursor.fetchone():
                    cursor.execute("SELECT * FROM connection_log ORDER BY timestamp DESC LIMIT 10")
                    recent_logs = cursor.fetchall()
            except:
                pass
            
            # Get quantum analysis with error handling
            quantum_analysis = []
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quantum_analysis'")
                if cursor.fetchone():
                    cursor.execute("SELECT * FROM quantum_analysis ORDER BY timestamp DESC LIMIT 10")
                    quantum_analysis = cursor.fetchall()
            except:
                pass
            
            # Get saved snapshots with error handling
            snapshots = []
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='client_state_snapshots'")
                if cursor.fetchone():
                    cursor.execute("SELECT * FROM client_state_snapshots ORDER BY timestamp DESC LIMIT 5")
                    snapshots = cursor.fetchall()
            except:
                pass
            
            conn.close()
            
            return {
                'current_data': current_data,
                'recent_logs': recent_logs,
                'quantum_analysis': quantum_analysis,
                'saved_snapshots': snapshots,
                'client_last_seen': self.client_last_seen.isoformat() if self.client_last_seen else None,
                'status': 'connected' if self.client_last_seen and (datetime.now() - self.client_last_seen).total_seconds() < 10 else 'disconnected'
            }
            
        except Exception as e:
            print(f"❌ Get status error: {e}")
            
            # Return minimal status on error
            return {
                'current_data': [],
                'recent_logs': [],
                'quantum_analysis': [],
                'saved_snapshots': [],
                'client_last_seen': None,
                'status': 'error',
                'error': str(e)
            }