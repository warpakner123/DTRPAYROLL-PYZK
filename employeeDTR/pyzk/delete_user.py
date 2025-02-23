from zk import ZK, const

# Replace with your device's IP and port, and set the correct password (123)
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)

def delete_user_fingerprint():
    try:
        conn = zk.connect()
        conn.disable_device()  # Prevent user interactions during the update

        user_id = ''  # Replace with the target user ID
        uid = 8  # Fingerprint index (0-9)

        # Check if user exists by comparing user_id directly
        users = conn.get_users()
        print(f"Users on device: {users}")  # Print users to confirm

        # Debug: print user_id and the ids in users
        for user in users:
            print(f"Checking user: {user.name}, user_id: {user.user_id}")

        # Correct comparison for user_id
        user_exists = any(int(user.user_id) == user_id for user in users)
        if not user_exists:
            print(f"User {user_id} does not exist.")
            return

        # Attempt to delete the entire user (not just a fingerprint template)
        print(f"Attempting to delete User {uid}")
        conn.delete_user(uid)
        print(f"User {uid} deleted successfully.")

        conn.enable_device()
        conn.disconnect()

    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'message'):
            print(f"Error message: {e.message}")
        else:
            print("No message available")

if __name__ == "__main__":
    delete_user_fingerprint()
