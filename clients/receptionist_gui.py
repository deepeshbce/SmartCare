import tkinter as tk
from tkinter import messagebox
import socket

def register_patient():
    # 1. Get data from the entry fields
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    symptoms = symptoms_entry.get().strip()
    category = category_var.get()
    
    # 2. Input Validation (Checking for empty or wrong data)
    if not name or not age or not symptoms:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
        
    # 3. Client/Server Networking
    try:
        # Create a socket and connect to the server (127.0.0.1 on Port 5000)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        
        # Format our message (e.g., "REGISTER:Deepesh:Emergency")
        message = f"REGISTER:{name}:{category}"
        
        # Send message to server
        client.send(message.encode('utf-8'))
        
        # Wait for the server to reply
        response = client.recv(1024).decode('utf-8')
        
        if response == "Success":
            # Dialog box showing success
            messagebox.showinfo("Success", f"{name} registered successfully as {category}!")
            
            # Clear the entry fields for the next patient
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            symptoms_entry.delete(0, tk.END)
            category_var.set("Normal")
        
        # Close the connection once the task is done
        client.close()
        
    except Exception as e:
        messagebox.showerror("Connection Error", "Cannot connect to server. Is it running?")

# --- GUI Setup ---
root = tk.Tk()
root.title("SmartCare - Receptionist")
root.geometry("400x450")
root.configure(bg="#f0f4f8") # Light blue/grey background

# Fonts
title_font = ("Helvetica", 16, "bold")
label_font = ("Arial", 12)

# Title Label using 'pack' layout
title_label = tk.Label(root, text="Patient Registration", font=title_font, bg="#f0f4f8", fg="#333")
title_label.pack(pady=20)

# Nested Frame: We create a 'frame' inside 'root' to hold the form cleanly
form_frame = tk.Frame(root, bg="#f0f4f8")
form_frame.pack(pady=10)

# Form Fields using 'grid' layout inside the frame
tk.Label(form_frame, text="Patient Name:", font=label_font, bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(form_frame, font=label_font, width=20)
name_entry.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Age:", font=label_font, bg="#f0f4f8").grid(row=1, column=0, sticky="w", pady=5)
age_entry = tk.Entry(form_frame, font=label_font, width=20)
age_entry.grid(row=1, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Symptoms:", font=label_font, bg="#f0f4f8").grid(row=2, column=0, sticky="w", pady=5)
symptoms_entry = tk.Entry(form_frame, font=label_font, width=20)
symptoms_entry.grid(row=2, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Category:", font=label_font, bg="#f0f4f8").grid(row=3, column=0, sticky="w", pady=5)

# Radio Buttons for Patient Category
category_var = tk.StringVar(value="Normal")
radio_frame = tk.Frame(form_frame, bg="#f0f4f8")
radio_frame.grid(row=3, column=1, sticky="w", pady=5, padx=10)

tk.Radiobutton(radio_frame, text="Normal", variable=category_var, value="Normal", bg="#f0f4f8").pack(anchor="w")
tk.Radiobutton(radio_frame, text="Emergency", variable=category_var, value="Emergency", bg="#f0f4f8", fg="red").pack(anchor="w")

# Event-Driven Button: 'command=register_patient' links the click event to our function
submit_btn = tk.Button(root, text="Register Patient", font=label_font, bg="#4CAF50", fg="white", command=register_patient)
submit_btn.pack(pady=30)

# Start the Tkinter Event Loop
root.mainloop()