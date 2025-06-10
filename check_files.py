#!/usr/bin/env python3
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
        print("\n💡 Please save the missing files from the artifacts before running.")
        return False
    else:
        print("✅ All required files are present!")
        print("🚀 You can now run: python3 run_attack_prediction.py")
        return True

if __name__ == '__main__':
    check_files()
