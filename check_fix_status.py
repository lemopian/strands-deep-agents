"""
Quick diagnostic to check if the fix is properly installed.
"""

import sys

def check_fix():
    """Check if the tool result ordering fix is present."""
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()
    
    # Try to read the event_loop.py file
    event_loop_path = sys.executable.replace('/bin/python3', '/lib/python3.12/site-packages/strands/event_loop/event_loop.py')
    
    try:
        with open(event_loop_path, 'r') as f:
            content = f.read()
            
        # Check for the fix
        if "FIX: Ensure tool results are ordered to match the ORIGINAL tool_uses order" in content:
            print("✅ FIX IS PRESENT in event_loop.py")
            
            # Check for debug logs
            if "BEFORE REORDER - tool_results count" in content:
                print("✅ DEBUG LOGS ARE PRESENT")
            else:
                print("❌ DEBUG LOGS ARE MISSING")
            
            # Count how many times "REORDERING" appears
            reorder_count = content.count("REORDERING - Original message tool IDs")
            print(f"✅ Found {reorder_count} reordering implementation(s)")
            
            # Check the line we're supposed to be at
            lines = content.split('\n')
            for i, line in enumerate(lines[385:395], start=386):
                print(f"Line {i}: {line[:80]}")
            
        else:
            print("❌ FIX IS NOT PRESENT in event_loop.py")
            print(f"   File location: {event_loop_path}")
            
    except FileNotFoundError:
        print(f"❌ Could not find event_loop.py at: {event_loop_path}")
    except Exception as e:
        print(f"❌ Error checking fix: {e}")


if __name__ == "__main__":
    check_fix()

