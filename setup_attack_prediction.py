#!/usr/bin/env python3
# setup_attack_prediction.py - Setup Enhanced Attack Type Prediction System

import os
import sys

def create_startup_script():
    """Create a startup script for the enhanced attack prediction system"""
    print("📝 Creating startup script for Enhanced Attack Prediction System...")
    
    startup_content = '''#!/usr/bin/env python3
# run_attack_prediction.py - Start Enhanced Attack Type Prediction System

import sys
import os

def main():
    print("🎯 Starting Enhanced Packet Quantum Security AI - Attack Type Prediction")
    print("=" * 80)
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    try:
        # Import the enhanced main app with attack prediction
        from enhanced_main_app_with_prediction import EnhancedPacketQuantumNetworkMonitor
        
        # Initialize and start the system
        monitor = EnhancedPacketQuantumNetworkMonitor()
        monitor.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required files are in the current directory:")
        print("   - enhanced_main_app_with_prediction.py")
        print("   - quantum_analyzer_enhanced_prediction.py")
        print("   - quantum_server_fixed.py")
        print("   - quantum_client_fixed.py")
        print("   - attack_simulator.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
    
    with open('run_attack_prediction.py', 'w') as f:
        f.write(startup_content)
    
    # Make executable on Unix systems
    try:
        os.chmod('run_attack_prediction.py', 0o755)
    except:
        pass
    
    print("✅ Startup script created: run_attack_prediction.py")

def create_file_checker():
    """Create a file checker script"""
    print("📝 Creating file checker...")
    
    checker_content = '''#!/usr/bin/env python3
# check_files.py - Check if all required files are present

import os

def check_files():
    """Check if all required files are present"""
    required_files = [
        'enhanced_main_app_with_prediction.py',
        'quantum_analyzer_enhanced_prediction.py',
        'quantum_server_fixed.py',
        'quantum_client_fixed.py',
        'attack_simulator.py'
    ]
    
    print("🔍 Checking required files...")
    print("=" * 50)
    
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - MISSING")
            missing_files.append(filename)
    
    print("=" * 50)
    
    if missing_files:
        print(f"❌ Missing {len(missing_files)} required files:")
        for filename in missing_files:
            print(f"   - {filename}")
        print("\\n💡 Please save the missing files from the artifacts before running.")
        return False
    else:
        print("✅ All required files are present!")
        print("🚀 You can now run: python3 run_attack_prediction.py")
        return True

if __name__ == '__main__':
    check_files()
'''
    
    with open('check_files.py', 'w') as f:
        f.write(checker_content)
    
    try:
        os.chmod('check_files.py', 0o755)
    except:
        pass
    
    print("✅ File checker created: check_files.py")

def main():
    """Main setup function"""
    print("🎯 Enhanced Attack Type Prediction System - Setup Tool")
    print("=" * 70)
    
    print("📋 This setup tool will help you get the enhanced attack prediction system running.")
    print()
    
    # Create startup script
    create_startup_script()
    
    # Create file checker
    create_file_checker()
    
    print()
    print("=" * 70)
    print("✅ Setup completed successfully!")
    print()
    print("📋 Next Steps:")
    print("1. Save all the artifact files to your project directory:")
    print("   - enhanced_main_app_with_prediction.py")
    print("   - quantum_analyzer_enhanced_prediction.py")
    print("   - quantum_server_fixed.py")
    print("   - quantum_client_fixed.py")
    print("   - attack_simulator.py (should already exist)")
    print()
    print("2. Check if all files are present:")
    print("   python3 check_files.py")
    print()
    print("3. Start the enhanced attack prediction system:")
    print("   python3 run_attack_prediction.py")
    print()
    print("4. Open your browser and go to:")
    print("   http://localhost:5000")
    print()
    print("🎯 New Features You'll See:")
    print("   - Real-time attack type prediction")
    print("   - Specific attack classification (DDoS, Port Scan, etc.)")
    print("   - Probability scores for each attack type")
    print("   - Enhanced threat severity levels")
    print("   - Detailed mitigation recommendations")
    print("   - Advanced attack simulation buttons")
    print("   - Live confidence scoring")
    print()
    print("🎮 Try the Enhanced Attack Simulations:")
    print("   - 💥 DDoS Volumetric - Massive packet flood simulation")
    print("   - 🔍 Port Scan - Network reconnaissance simulation")
    print("   - 📤 Data Exfiltration - Large file theft simulation")
    print("   - 🤖 Botnet C&C - Malware communication simulation")
    print("   - ⚡ SYN Flood - Connection exhaustion simulation")

if __name__ == "__main__":
    main()