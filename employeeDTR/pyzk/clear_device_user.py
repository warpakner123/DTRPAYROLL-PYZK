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

        # Clear all data
        users = conn.get_users()
        for user in users:
            conn.delete_user(user_id=user.user_id)
            print(user,"user deleted")
        
        conn.free_data()
        conn.clear_data()
        conn.restart()


    except Exception as e:
        print("Process failed: {}".format(e))
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()

if __name__ == "__main__":
    clear_device_user()