#!/usr/bin/env python3
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
