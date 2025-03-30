from time import sleep
import string
import secrets

def gen(length, excluded_chars):
        all_characters = string.ascii_letters + string.digits + string.punctuation
        valid_characters = [char for char in all_characters if char not in excluded_chars]
        password = ""
        password = ''.join(secrets.choice(valid_characters) for _ in range(length))
        
        
                                      
                            
                
        return password
    
    
    
print("How long do you want the password to be? Enter here:")
length = input()

excluded_chars = input("Enter characters to exclude (if more, split them by spaces): ").split()

try:
    length = int(length)
    print(f"Generating a strong password of length: {length}")

    

    password = gen(length, excluded_chars)
    print(f"Your generated password is: {password}")

except ValueError:
    print("Please enter a valid number!")