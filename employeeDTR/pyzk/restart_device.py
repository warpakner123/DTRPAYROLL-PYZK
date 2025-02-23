import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK


def restart_device():
    zk = ZK('192.168.1.201', port=4370, timeout=15, password=0, force_udp=True, ommit_ping=False)
    conn = None
    try:
        print("🔄 Attempting to connect to the device...")
        conn = zk.connect()
        if conn:
            print("✅ Connection successful! Restarting device...")
            conn.restart()
            print("✅ Device restarted successfully!")
        else:
            print("⚠️ Connection object is None, something went wrong.")
    except Exception as e:
        print(f"❌ Process terminated: {e}")
    finally:
        if conn:
            conn.disconnect()
            print("🔌 Disconnected from the device.")

            
if __name__ == "__main__":
    restart_device()