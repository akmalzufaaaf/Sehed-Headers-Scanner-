import bcrypt

def verify_password(input_password, stored_hash):
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash):
        print("Password benar!")
    else:
        print("Password salah!")

def main():
    print("=== Program Verifikasi Password dengan bcrypt ===")
    
    stored_hash = input("Masukkan hash yang tersimpan di database: ").strip().encode('utf-8')
    
    input_password = input("Masukkan password untuk verifikasi: ").strip()
    
    if not input_password:
        print("Password tidak boleh kosong!")
        return

    verify_password(input_password, stored_hash)

if __name__ == "__main__":
    main()