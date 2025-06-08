# mininet_topology.py - Network Topology for Quantum Monitor
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import threading
import subprocess
import os

class QuantumNetworkTopology:
    def __init__(self):
        self.net = None
        self.server_host = None
        self.client_host = None
        self.switch = None
        self.attack_active = False
        
    def create_topology(self):
        """Create a simple network topology for quantum monitor demo"""
        info('*** Creating network topology for Quantum Monitor\n')
        
        # Create network
        self.net = Mininet(
            controller=Controller,
            switch=OVSKernelSwitch,
            link=TCLink,
            autoSetMacs=True,
            autoStaticArp=True
        )
        
        info('*** Adding controller\n')
        c0 = self.net.addController('c0')
        
        info('*** Adding switch\n')
        self.switch = self.net.addSwitch('s1')
        
        info('*** Adding hosts\n')
        # Server host (represents the Pi/Edge device)
        self.server_host = self.net.addHost(
            'server', 
            ip='10.0.0.1/24',
            mac='00:00:00:00:00:01'
        )
        
        # Client host (represents the Laptop/Remote node)
        self.client_host = self.net.addHost(
            'client',
            ip='10.0.0.2/24', 
            mac='00:00:00:00:00:02'
        )
        
        info('*** Creating links with normal network conditions\n')
        # Normal links with good network conditions
        self.net.addLink(
            self.server_host, 
            self.switch,
            bw=100,  # 100 Mbps
            delay='5ms',  # 5ms latency
            loss=0,  # No packet loss
            use_htb=True
        )
        
        self.net.addLink(
            self.client_host,
            self.switch, 
            bw=100,  # 100 Mbps
            delay='5ms',  # 5ms latency
            loss=0,  # No packet loss
            use_htb=True
        )
        
        info('*** Starting network\n')
        self.net.start()
        
        # Test connectivity
        info('*** Testing connectivity\n')
        result = self.net.ping([self.server_host, self.client_host])
        if result == 0:
            info('*** Network connectivity: OK\n')
        else:
            info('*** Network connectivity: FAILED\n')
        
        return self.net
    
    def simulate_normal_network(self):
        """Reset to normal network conditions"""
        info('*** Resetting to normal network conditions\n')
        
        # Reset server link
        self.server_host.cmd('tc qdisc del dev server-eth0 root 2>/dev/null')
        self.server_host.cmd('tc qdisc add dev server-eth0 root handle 1: htb default 30')
        self.server_host.cmd('tc class add dev server-eth0 parent 1: classid 1:1 htb rate 100mbit')
        self.server_host.cmd('tc class add dev server-eth0 parent 1:1 classid 1:30 htb rate 100mbit')
        self.server_host.cmd('tc qdisc add dev server-eth0 parent 1:30 handle 30: netem delay 5ms')
        
        # Reset client link  
        self.client_host.cmd('tc qdisc del dev client-eth0 root 2>/dev/null')
        self.client_host.cmd('tc qdisc add dev client-eth0 root handle 1: htb default 30')
        self.client_host.cmd('tc class add dev client-eth0 parent 1: classid 1:1 htb rate 100mbit')
        self.client_host.cmd('tc class add dev client-eth0 parent 1:1 classid 1:30 htb rate 100mbit')
        self.client_host.cmd('tc qdisc add dev client-eth0 parent 1:30 handle 30: netem delay 5ms')
        
        self.attack_active = False
        info('*** Normal network conditions restored\n')
    
    def simulate_dos_attack(self):
        """Simulate DoS attack with high latency and packet loss"""
        info('*** Simulating DoS attack - High latency + Packet loss\n')
        
        # Apply DoS conditions to client link (affecting client-to-server communication)
        self.client_host.cmd('tc qdisc del dev client-eth0 root 2>/dev/null')
        self.client_host.cmd('tc qdisc add dev client-eth0 root handle 1: htb default 30')
        self.client_host.cmd('tc class add dev client-eth0 parent 1: classid 1:1 htb rate 10mbit')  # Reduced bandwidth
        self.client_host.cmd('tc class add dev client-eth0 parent 1:1 classid 1:30 htb rate 10mbit')
        self.client_host.cmd('tc qdisc add dev client-eth0 parent 1:30 handle 30: netem delay 500ms loss 15%')  # High delay + loss
        
        self.attack_active = True
        info('*** DoS attack conditions applied\n')
    
    def simulate_flooding_attack(self):
        """Simulate connection flooding with bandwidth limitations"""
        info('*** Simulating Connection Flooding - Bandwidth exhaustion\n')
        
        # Apply flooding conditions - very limited bandwidth
        self.client_host.cmd('tc qdisc del dev client-eth0 root 2>/dev/null')
        self.client_host.cmd('tc qdisc add dev client-eth0 root handle 1: htb default 30')
        self.client_host.cmd('tc class add dev client-eth0 parent 1: classid 1:1 htb rate 1mbit')  # Very limited bandwidth
        self.client_host.cmd('tc class add dev client-eth0 parent 1:1 classid 1:30 htb rate 1mbit')
        self.client_host.cmd('tc qdisc add dev client-eth0 parent 1:30 handle 30: netem delay 100ms loss 5%')
        
        self.attack_active = True
        info('*** Connection flooding conditions applied\n')
    
    def simulate_congestion_attack(self):
        """Simulate network congestion with variable delays"""
        info('*** Simulating Network Congestion - Variable delays\n')
        
        # Apply congestion conditions - high jitter and variable delays
        self.client_host.cmd('tc qdisc del dev client-eth0 root 2>/dev/null')
        self.client_host.cmd('tc qdisc add dev client-eth0 root handle 1: htb default 30')
        self.client_host.cmd('tc class add dev client-eth0 parent 1: classid 1:1 htb rate 50mbit')  # Moderate bandwidth
        self.client_host.cmd('tc class add dev client-eth0 parent 1:1 classid 1:30 htb rate 50mbit')
        # High jitter: 200ms ± 100ms delay variation
        self.client_host.cmd('tc qdisc add dev client-eth0 parent 1:30 handle 30: netem delay 200ms 100ms distribution normal loss 2%')
        
        self.attack_active = True
        info('*** Network congestion conditions applied\n')
    
    def start_quantum_server(self):
        """Start the quantum server on the server host"""
        info('*** Starting Quantum Server on server host\n')
        
        # Start server in background
        server_cmd = f"""
        cd {os.getcwd()} && 
        export PYTHONPATH=$PYTHONPATH:{os.getcwd()} && 
        python3 -c "
import sys
sys.path.append('{os.getcwd()}')
from quantum_analyzer import QuantumNetworkAnalyzer
from quantum_server import QuantumNetworkMonitorServer
from flask import Flask, request, jsonify
import threading
import time

# Initialize components
quantum_analyzer = QuantumNetworkAnalyzer()
server = QuantumNetworkMonitorServer(quantum_analyzer, 'mininet_quantum_monitor.db')

# Flask app
app = Flask(__name__)

@app.route('/update', methods=['POST'])
def receive_update():
    try:
        data = request.json
        server.update_client_data(data)
        server.log_event('CLIENT_UPDATE', f'Received {{len(data)}} entries')
        return {{'status': 'success'}}
    except Exception as e:
        return {{'status': 'error', 'message': str(e)}}, 500

@app.route('/status', methods=['GET'])
def get_status():
    return server.get_status()

@app.route('/attack/<attack_type>')
def simulate_attack(attack_type):
    # This will be handled by Mininet controls
    return {{'status': f'{{attack_type}} attack noted'}}

if __name__ == '__main__':
    print('🔬 Quantum Server starting on Mininet host...')
    app.run(host='0.0.0.0', port=5000, debug=False)
"
        """
        
        # Execute server on server host
        self.server_host.cmd(f'nohup bash -c "{server_cmd}" > server.log 2>&1 &')
        time.sleep(3)  # Give server time to start
        
        # Check if server started
        result = self.server_host.cmd('curl -s http://10.0.0.1:5000/status')
        if result and 'current_data' in result:
            info('*** Quantum Server: STARTED\n')
            return True
        else:
            info('*** Quantum Server: FAILED TO START\n')
            return False
    
    def start_quantum_client(self):
        """Start the quantum client on the client host"""
        info('*** Starting Quantum Client on client host\n')
        
        client_cmd = f"""
        cd {os.getcwd()} && 
        export PYTHONPATH=$PYTHONPATH:{os.getcwd()} && 
        python3 -c "
import sys
sys.path.append('{os.getcwd()}')
import requests
import random
import time
import json
from datetime import datetime

class MininetQuantumClient:
    def __init__(self):
        self.server_url = 'http://10.0.0.1:5000'
        self.running = True
        
    def generate_random_data(self):
        data = []
        for i in range(1, 6):
            data.append({{
                'id': i,
                'random_value': round(random.uniform(0, 100), 2),
                'client_timestamp': datetime.now().isoformat()
            }})
        return data
    
    def send_update(self):
        try:
            data = self.generate_random_data()
            response = requests.post(
                f'{{self.server_url}}/update',
                json=data,
                timeout=10
            )
            if response.status_code == 200:
                print(f'✅ [MININET-CLIENT] Update successful at {{datetime.now().strftime(\"%H:%M:%S\")}}')
                return True
            else:
                print(f'❌ [MININET-CLIENT] Server returned {{response.status_code}}')
                return False
        except Exception as e:
            print(f'💥 [MININET-CLIENT] Error: {{e}}')
            return False
    
    def run(self):
        print('🔄 [MININET-CLIENT] Starting...')
        while self.running:
            self.send_update()
            time.sleep(5)

if __name__ == '__main__':
    client = MininetQuantumClient()
    try:
        client.run()
    except KeyboardInterrupt:
        print('🛑 [MININET-CLIENT] Stopped')
"
        """
        
        # Execute client on client host
        self.client_host.cmd(f'nohup bash -c "{client_cmd}" > client.log 2>&1 &')
        time.sleep(2)  # Give client time to start
        
        info('*** Quantum Client: STARTED\n')
        return True
    
    def show_network_status(self):
        """Show current network status and statistics"""
        info('\n*** Network Status ***\n')
        
        # Show current tc rules
        info('=== Server Host Network Config ===\n')
        server_tc = self.server_host.cmd('tc qdisc show dev server-eth0')
        info(f'{server_tc}\n')
        
        info('=== Client Host Network Config ===\n') 
        client_tc = self.client_host.cmd('tc qdisc show dev client-eth0')
        info(f'{client_tc}\n')
        
        # Test latency
        info('=== Network Latency Test ===\n')
        ping_result = self.client_host.cmd('ping -c 3 10.0.0.1')
        info(f'{ping_result}\n')
        
        # Check server status
        info('=== Quantum Server Status ===\n')
        try:
            status_result = self.client_host.cmd('curl -s http://10.0.0.1:5000/status')
            if status_result:
                info('Server is responding\n')
            else:
                info('Server is not responding\n')
        except:
            info('Server check failed\n')
    
    def interactive_cli(self):
        """Start interactive CLI for network control"""
        info('\n*** Starting Quantum Network Monitor CLI ***\n')
        info('Available commands:\n')
        info('  normal     - Reset to normal network conditions\n')
        info('  dos        - Simulate DoS attack\n')
        info('  flooding   - Simulate connection flooding\n')
        info('  congestion - Simulate network congestion\n')
        info('  status     - Show network status\n')
        info('  pingall    - Test connectivity\n')
        info('  exit       - Exit CLI\n')
        info('\n')
        
        while True:
            try:
                cmd = input('mininet-quantum> ').strip().lower()
                
                if cmd == 'normal':
                    self.simulate_normal_network()
                elif cmd == 'dos':
                    self.simulate_dos_attack()
                elif cmd == 'flooding':
                    self.simulate_flooding_attack()
                elif cmd == 'congestion':
                    self.simulate_congestion_attack()
                elif cmd == 'status':
                    self.show_network_status()
                elif cmd == 'pingall':
                    self.net.pingAll()
                elif cmd == 'exit':
                    break
                elif cmd == 'help':
                    info('Available commands: normal, dos, flooding, congestion, status, pingall, exit\n')
                else:
                    info(f'Unknown command: {cmd}. Type "help" for available commands.\n')
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
    
    def cleanup(self):
        """Clean up network and processes"""
        info('*** Cleaning up network\n')
        
        # Kill any running processes
        self.server_host.cmd('pkill -f "quantum"')
        self.client_host.cmd('pkill -f "quantum"')
        
        # Stop network
        if self.net:
            self.net.stop()

def main():
    """Main function to run the Mininet Quantum Network Monitor"""
    setLogLevel('info')
    
    topology = QuantumNetworkTopology()
    
    try:
        # Create network
        net = topology.create_topology()
        
        # Start quantum components
        if topology.start_quantum_server():
            if topology.start_quantum_client():
                info('\n*** Quantum Network Monitor is running! ***\n')
                info('*** Server: http://10.0.0.1:5000 ***\n')
                info('*** Monitor the network and test attacks ***\n')
                
                # Show initial status
                topology.show_network_status()
                
                # Start interactive CLI
                topology.interactive_cli()
            else:
                info('Failed to start quantum client\n')
        else:
            info('Failed to start quantum server\n')
            
    except Exception as e:
        info(f'Error: {e}\n')
    finally:
        topology.cleanup()

if __name__ == '__main__':
    main()