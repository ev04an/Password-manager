import json
import os
import base64
import secrets
import string
from cryptography.fernet import Fernet

# File to store passwords
PASSWORDS_FILE = "passwords.json"
KEY_FILE = "secret.key"

# Generate or load the encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

# Encrypt data
def encrypt(data, cipher):
    return cipher.encrypt(data.encode()).decode()

# Decrypt data
def decrypt(data, cipher):
    return cipher.decrypt(data.encode()).decode()

# Load existing passwords
def load_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r") as file:
        return json.load(file)

# Save passwords
def save_passwords(passwords):
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Generate a random strong password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Add a new password
def save_password(service, password, cipher):
    passwords = load_passwords()
    passwords[service] = encrypt(password, cipher)
    save_passwords(passwords)
    print(f"Password saved for {service}.")

# Retrieve a password
def retrieve_password(service, cipher):
    passwords = load_passwords()
    if service in passwords:
        return decrypt(passwords[service], cipher)
    else:
        return None

# Update an existing password
def update_password(service, cipher):
    passwords = load_passwords()
    if service in passwords:
        new_password = input("Enter new password: ")
        passwords[service] = encrypt(new_password, cipher)
        save_passwords(passwords)
        print(f"Password updated for {service}.")
    else:
        print("Service not found!")

# Delete a stored password
def delete_password(service):
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        save_passwords(passwords)
        print(f"Deleted password for {service}.")
    else:
        print("Service not found!")

# Show all saved services
def list_services():
    passwords = load_passwords()
    if passwords:
        print("\nStored Services:")
        for service in passwords.keys():
            print(f"- {service}")
    else:
        print("No passwords saved yet.")

# Main menu
def main():
    cipher = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Save Password")
        print("2. Retrieve Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Show All Saved Services")
        print("6. Generate Secure Password")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Enter service name: ")
            password = input("Enter password (or leave blank to generate one): ")
            if not password:
                password = generate_password()
                print(f"Generated password: {password}")
            save_password(service, password, cipher)

        elif choice == "2":
            service = input("Enter service name: ")
            password = retrieve_password(service, cipher)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("Service not found!")

        elif choice == "3":
            service = input("Enter service name: ")
            update_password(service, cipher)

        elif choice == "4":
            service = input("Enter service name to delete: ")
            delete_password(service)

        elif choice == "5":
            list_services()

        elif choice == "6":
            length = int(input("Enter password length (default is 12): ") or 12)
            print(f"Generated Password: {generate_password(length)}")

        elif choice == "7":
            print("Exiting Password Manager. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()


