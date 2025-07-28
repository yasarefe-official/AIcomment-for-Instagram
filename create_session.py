import instaloader
import getpass

# Get username and password from the user
username = input("Enter your Instagram username: ")
password = getpass.getpass("Enter your Instagram password: ")

# Create an Instaloader instance
L = instaloader.Instaloader()

try:
    # Login and save the session
    L.login(username, password)
    L.save_session_to_file(f"./{username}")
    print(f"Session file created successfully as '{username}'!")
    print("You can now use this session file with the main application.")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please make sure your credentials are correct and try again.")
    print("If you have 2FA enabled, you might need to handle that separately.")
