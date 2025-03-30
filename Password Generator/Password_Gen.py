import tkinter as tk
import string
import secrets
import time

#methods----------
def save_password(password):
    try:
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
        with open("generated_passwords.txt", "a") as file:
            file.write(f"U generated this password:{password} at {formatted_time}\n")  
        result_label.config(text=f"Password saved to file.")
    except Exception as e:
        result_label.config(text=f"Error saving password: {e}")
        
def generate_password():
    try:
                length = int(length_entry.get())
        
        
        excluded = excluded_entry.get().split()
        
        
        all_characters = string.ascii_letters + string.digits + string.punctuation
        valid_characters = [char for char in all_characters if char not in excluded]
        
        
        if not valid_characters:
            result_label.config(text="No valid characters available after exclusions. Please adjust exclusions.")
            return
        
        
        password = ''.join(secrets.choice(valid_characters) for _ in range(length))
        
        
        
        save_password(password)
        
        
        length_entry.delete(0, tk.END)
        excluded_entry.delete(0, tk.END)

    except ValueError:
        
        result_label.config(text="Please enter a valid number for length.")
#------------------------------------------------------------------------------------------



root = tk.Tk()
root.title("Password Generator")


length_label = tk.Label(root, text="Enter password length:", font=("Arial", 15))
length_label.pack(pady=5)

length_entry = tk.Entry(root, fg="black", bg="white", font=("Arial", 15))
length_entry.pack(pady=5)

excluded_label = tk.Label(root, text="Enter characters to exclude (separate by spaces):", font=("Arial", 14))
excluded_label.pack(pady=5)

excluded_entry = tk.Entry(root, fg="black", bg="white", font=("Arial", 15))
excluded_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Password", command=generate_password, width=25, height=2, font=("Arial", 14))
generate_button.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=5)

root.mainloop()
