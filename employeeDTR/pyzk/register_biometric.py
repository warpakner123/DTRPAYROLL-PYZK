from zk import ZK, const
import time

def register_fingerprint(id, name, password):
    print('id',id)
    print('name',name)
    print('password',password)
    conn = None
    # create ZK instance
    zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
    try:
        conn = zk.connect()
        conn.disable_device()

        users = conn.get_users()
        num_users = len(users)
        user_device_id  = num_users + 1
        temp_id = 1
        print('users',users)
        for user in users:
            print('user:', user, 'type:', type(user))
            print('user:', user, 'type:', type(user))
            print('user_id:', user.user_id, 'type:', type(user.user_id))
            if int(user.user_id) == int(id):
                print('MATCHED USER ID')
                temp_id += 1


        print('temp_id',temp_id)
        



        conn.set_user(
            uid=user_device_id, 
            name=name, 
            privilege=const.USER_DEFAULT, 
            password=password, 
            # group_id=id, 
            user_id=id, 
            card=0
        )
        print('user_device_id',user_device_id)
        print('temp_id',temp_id)

        print("Please place your finger on the device...")
    
        try:
            if conn.enroll_user(uid=user_device_id, temp_id=temp_id, user_id=str(id)):
                print("Fingerprint enrolled successfully.")
        except Exception as e:
            print(e,"Enrollment failed, please try again.")


    except Exception as e:
        print("Process failed: {}".format(e))
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()
if __name__ == "__main__":
    register_fingerprint(2, 'John Doe', '123')