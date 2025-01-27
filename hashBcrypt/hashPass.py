import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    # Hash password 
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def main():
    print("=== Program Hash Password dengan bcrypt ===")
    
    password = input("Masukkan password: ").strip()
    
    if not password:
        print("Password tidak boleh kosong!")
        return

    hashed_password = hash_password(password)
    
    # Tampilkan hasil hash
    print("\nPassword yang dihash:")
    print(hashed_password.decode('utf-8')) 

if __name__ == "__main__":
    main()