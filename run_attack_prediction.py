#!/usr/bin/env python3
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
