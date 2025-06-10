#!/usr/bin/env python3
# setup_fixed_system.py - Complete Setup and Diagnostic Tool

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check and install required dependencies"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('requests', 'requests'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
    ]
    
    optional_packages = [
        ('pennylane', 'pennylane')
    ]
    
    missing_required = []
    missing_optional = []
    
    # Check required packages
    for package_name, pip_name in required_packages:
        if importlib.util.find_spec(package_name) is None:
            missing_required.append((package_name, pip_name))
        else:
            print(f"✅ {package_name} found")
    
    # Check optional packages
    for package_name, pip_name in optional_packages:
        if importlib.util.find_spec(package_name) is None:
            missing_optional.append((package_name, pip_name))
        else:
            print(f"✅ {package_name} found")
    
    # Install missing required packages
    if missing_required:
        print(f"\n📦 Installing missing required packages...")
        for package_name, pip_name in missing_required:
            try:
                print(f"Installing {pip_name}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name])
                print(f"✅ {pip_name} installed")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {pip_name}")
                return False
    
    # Inform about optional packages
    if missing_optional:
        print(f"\n⚠️  Optional packages missing (quantum features will be disabled):")
        for package_name, pip_name in missing_optional:
            print(f"   - {pip_name}: pip install {pip_name}")
    
    return True

def create_fixed_files():
    """Create all fixed system files"""
    print("\n📝 Creating fixed system files...")
    
    # The files are already created via artifacts above
    # This function serves as a placeholder for future file creation needs
    
    files_to_check = [
        'enhanced_main_app_fixed.py',
        'quantum_analyzer_fixed.py', 
        'quantum_server_fixed.py',
        'quantum_client_fixed.py',
        'attack_simulator.py'  # This should already exist
    ]
    
    existing_files = []
    missing_files = []
    
    for filename in files_to_check:
        if os.path.exists(filename):
            existing_files.append(filename)
            print(f"✅ {filename} found")
        else:
            missing_files.append(filename)
            print(f"❌ {filename} missing")
    
    if missing_files:
        print(f"\n⚠️  Missing files detected. Please ensure all files are in the same directory:")
        for filename in missing_files:
            print(f"   - {filename}")
        return False
    
    return True

def test_imports():
    """Test importing fixed modules"""
    print("\n🧪 Testing module imports...")
    
    try:
        # Test basic imports
        import sqlite3
        print("✅ sqlite3 available")
        
        import threading
        print("✅ threading available")
        
        import json
        print("✅ json available")
        
        import datetime
        print("✅ datetime available")
        
        # Test if we can import our fixed modules
        if os.path.exists('quantum_analyzer_fixed.py'):
            sys.path.insert(0, '.')
            from quantum_analyzer_fixed import EnhancedPacketQuantumSecurityAI
            print("✅ quantum_analyzer_fixed imports successfully")
            
            # Test basic functionality
            analyzer = EnhancedPacketQuantumSecurityAI()
            print("✅ QuantumAnalyzer initializes successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def create_startup_script():
    """Create a startup script"""
    print("\n📄 Creating startup script...")
    
    startup_content = '''#!/usr/bin/env python3
# run_fixed_system.py - Startup script for fixed system

import sys
import os

def main():
    print("🚀 Starting Enhanced Packet Quantum Security AI - Fixed Version")
    print("=" * 70)
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    try:
        from enhanced_main_app_fixed import EnhancedPacketQuantumNetworkMonitor
        
        # Initialize and start the system
        monitor = EnhancedPacketQuantumNetworkMonitor()
        monitor.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all fixed files are in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
    
    with open('run_fixed_system.py', 'w') as f:
        f.write(startup_content)
    
    # Make executable on Unix systems
    try:
        os.chmod('run_fixed_system.py', 0o755)
    except:
        pass
    
    print("✅ Startup script created: run_fixed_system.py")
    return True

def run_diagnostics():
    """Run comprehensive diagnostics"""
    print("\n🔬 Running system diagnostics...")
    
    # Test database creation
    try:
        import sqlite3
        test_db = "test_quantum.db"
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
        cursor.execute("INSERT INTO test (data) VALUES (?)", ("test_data",))
        conn.commit()
        conn.close()
        os.remove(test_db)
        print("✅ Database functionality working")
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    # Test Flask
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask working")
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        return False
    
    # Test threading
    try:
        import threading
        import time
        
        def test_thread():
            time.sleep(0.1)
        
        thread = threading.Thread(target=test_thread)
        thread.start()
        thread.join()
        print("✅ Threading working")
    except Exception as e:
        print(f"❌ Threading test failed: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🔧 Enhanced Packet Quantum Security AI - Setup & Diagnostic Tool")
    print("=" * 70)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check and install dependencies
    if not check_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Step 3: Check files
    if not create_fixed_files():
        print("❌ File check failed")
        sys.exit(1)
    
    # Step 4: Test imports
    if not test_imports():
        print("❌ Import tests failed")
        sys.exit(1)
    
    # Step 5: Run diagnostics
    if not run_diagnostics():
        print("❌ System diagnostics failed")
        sys.exit(1)
    
    # Step 6: Create startup script
    if not create_startup_script():
        print("❌ Startup script creation failed")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ Setup completed successfully!")
    print("\n🚀 To start the system:")
    print("   python3 run_fixed_system.py")
    print("\n🌐 Once running, access the dashboard at:")
    print("   http://localhost:5000")
    print("\n📦 Features available:")
    print("   - Real-time packet monitoring")
    print("   - Quantum ML threat detection")
    print("   - Attack simulation (DDoS, Port Scan, Data Exfiltration)")
    print("   - Web dashboard with live updates")
    print("   - Database logging and analysis")
    print("\n⚠️  Note: If you see validation failures, that's normal for the demo.")
    print("   The system will still function with classical detection.")

if __name__ == "__main__":
    main()