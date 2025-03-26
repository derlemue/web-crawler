import bcrypt

def main():
    password = input("🔐 Passwort eingeben: ").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print(f"\n✅ Bcrypt-Hash:\n{hashed.decode()}")

if __name__ == "__main__":
    main()
