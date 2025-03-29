import os
import hashlib
import json
import base64
import customtkinter as ctk
from cryptography.fernet import Fernet
from tkinter import messagebox

# Paths
BASE_DIR = "//home//axel//Desktop//PRHA//python//password_manager//"
USER_FILE = os.path.join(BASE_DIR, "user.json")
PASSWORDS_FILE = os.path.join(BASE_DIR, "passwords.enc")

# Global variables
encryption_key = None
passwords = []

# --------- Key Derivation ---------
def derive_key(master_password):
    hash = hashlib.sha256(master_password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hash[:32]))

# --------- User Management ---------
def save_user(master_password):
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    with open(USER_FILE, "w") as f:
        json.dump({"master_hash": hashed_password}, f)

def check_login(master_password):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as f:
        user_data = json.load(f)
    hashed_input = hashlib.sha256(master_password.encode()).hexdigest()
    return hashed_input == user_data["master_hash"]

# --------- Password Encryption ---------
def save_passwords(passwords):
    encrypted_data = encryption_key.encrypt(json.dumps(passwords).encode())
    with open(PASSWORDS_FILE, "wb") as f:
        f.write(encrypted_data)

def load_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return []
    with open(PASSWORDS_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = encryption_key.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)


def smooth_transition(new_frame_func):
    
    for widget in app.winfo_children():
        fade_out(widget)
    app.after(500, new_frame_func)

def fade_out(widget, step=0):
    
    if step < 10:
        widget.place_forget()
        app.after(50, lambda: fade_out(widget, step + 1))
    else:
        widget.place_forget()  

def fade_in(widget, step=0):
    
    if step < 10:
        widget.place(relx=0.5, rely=0.5, anchor="center")
        app.after(50, lambda: fade_in(widget, step + 1))
    else:
        widget.place(relx=0.5, rely=0.5, anchor="center")

# --------- GUI Screens ---------
def show_main_app():
    smooth_transition(main_screen)

def save_password():
    site = site_entry.get()
    password = password_entry.get()
    passwords.append({"site": site, "password": password})
    save_passwords(passwords)
    site_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

def show_saved_passwords():
    smooth_transition(saved_passwords_screen)

# --------- Main App Screen ---------
def main_screen():
    global site_entry, password_entry

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Password Manager", font=("Arial", 28, "bold")).pack(pady=15)

    site_entry = ctk.CTkEntry(frame, placeholder_text="Website")
    site_entry.pack(pady=5, padx=20)

    password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=5, padx=20)

    save_btn = animated_button(frame, "Save Password", save_password)
    save_btn.pack(pady=10)

    show_btn = animated_button(frame, "Show Saved Passwords", show_saved_passwords)
    show_btn.pack(pady=10)

    global passwords
    passwords = load_passwords()

# --------- Saved Passwords Screen ---------
def saved_passwords_screen():
    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Saved Passwords", font=("Arial", 22, "bold")).pack(pady=15)

    
    scrollable_frame = ctk.CTkScrollableFrame(frame)
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    checkboxes = [] 

    for entry in passwords:
        site_label = ctk.CTkLabel(scrollable_frame, text=f"{entry['site']}: {entry['password']}")
        site_label.pack(pady=5)
        
        delete_checkbox = ctk.CTkCheckBox(scrollable_frame, text=f"Delete {entry['site']}")
        delete_checkbox.pack(pady=5)
        checkboxes.append((delete_checkbox, entry))

    delete_btn = animated_button(frame, "Delete Selected", lambda: confirm_delete(checkboxes))
    delete_btn.pack(pady=20)

    back_btn = animated_button(frame, "Back", show_main_app)
    back_btn.pack(pady=20)

def confirm_delete(checkboxes):
   
    selected_sites = [entry for cb, entry in checkboxes if cb.get()]
    
    if not selected_sites:
        messagebox.showwarning("No Selection", "No passwords selected for deletion.")
        return
    
    response = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete {len(selected_sites)} selected passwords?")
    
    if response:
        delete_selected_passwords(selected_sites)

def delete_selected_passwords(selected_sites):
    global passwords
    passwords = [entry for entry in passwords if entry not in selected_sites]
    save_passwords(passwords)
    messagebox.showinfo("Success", "Selected passwords deleted successfully!")
    show_saved_passwords()

# --------- Login Handler ---------
def handle_login():
    global encryption_key

    master_password = password_entry.get()

    if os.path.exists(USER_FILE):
        if check_login(master_password):
            encryption_key = derive_key(master_password)
            show_main_app()
        else:
            error_label = ctk.CTkLabel(app, text="Invalid password.", text_color="red")
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            app.after(2000, error_label.destroy)
    else:
        save_user(master_password)
        encryption_key = derive_key(master_password)
        save_passwords([])
        show_main_app()

# --------- Login Screen ---------
def show_login_screen():
    global password_entry

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Welcome to Password Manager", font=("Arial", 24, "bold")).pack(pady=15)

    password_entry = ctk.CTkEntry(frame, placeholder_text="Master Password", show="*")
    password_entry.pack(pady=10, padx=20)

    login_btn = animated_button(frame, "Login / Register", handle_login)
    login_btn.pack(pady=15)

# --------- Animated Button ---------
def animated_button(parent, text, command):
    btn = ctk.CTkButton(parent, text=text, command=command, corner_radius=10, fg_color="#3a7ca5")
    btn.bind("<Enter>", lambda e: btn.configure(fg_color="#2b8a3e"))  # Hover green
    btn.bind("<Leave>", lambda e: btn.configure(fg_color="#3a7ca5"))  # Back to blue
    return btn

# --------- App Setup ---------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("500x600")
app.title("Password Manager")

show_login_screen()

app.mainloop()
