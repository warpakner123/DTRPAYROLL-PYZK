from zk import ZK, const

def clear_device_user():
    conn = None
    # create ZK instance
    zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False, verbose=True)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()

        users = conn.get_users()
        
        print('USERSSSS', users)


    except Exception as e:
        print("Process failed: {}".format(e))
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()

if __name__ == "__main__":
    clear_device_user()