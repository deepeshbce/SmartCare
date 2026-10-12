import tkinter as tk
from tkinter import messagebox
import socket
import threading
import queue
import time

# 1. Thread-safe queue for sending data from the background thread to the GUI
gui_queue = queue.Queue()

# 2. Network setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 5000))
except Exception as e:
    # If the server isn't running, show an error and stop the script
    print("Error: Could not connect to the server.")
    exit()

def fetch_queue_from_server():
    """BACKGROUND THREAD: Asks the server for the queue every 2 seconds."""
    while True:
        try:
            # Send our GET_QUEUE command
            client.send("GET_QUEUE".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            
            # Put the response into the safe queue for Tkinter to read
            gui_queue.put(response)
            
            # Pause this background thread for 2 seconds before asking again
            time.sleep(2) 
        except Exception as e:
            print("Disconnected from server.")
            break

def update_gui_from_queue():
    """MAIN THREAD: Safely checks the queue and updates the Tkinter Listbox."""
    try:
        # Check if there is new data from the background thread
        while not gui_queue.empty():
            queue_data = gui_queue.get_nowait()
            
            # Clear the current listbox on screen
            queue_listbox.delete(0, tk.END)
            
            if queue_data == "Empty":
                queue_listbox.insert(tk.END, "No patients waiting.")
            else:
                # The server sends data like "Deepesh (Normal),Rahul (Emergency)"
                # We split it by the comma and insert each person into the listbox
                patients = queue_data.split(",")
                for p in patients:
                    queue_listbox.insert(tk.END, p)
    except queue.Empty:
        pass
    
    # root.after schedules this function to run again in 500 milliseconds (Thread-safe Tkinter loop)
    root.after(500, update_gui_from_queue)

def call_next_patient():
    """Sends the NEXT command to the server to call a patient into the doctor's room."""
    try:
        client.send("NEXT".encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        
        if response == "Queue is empty":
            messagebox.showinfo("Notice", "No patients in the queue.")
        else:
            messagebox.showinfo("Next Patient", f"Please call: {response}")
    except:
        messagebox.showerror("Error", "Lost connection to server.")

# --- GUI Setup ---
root = tk.Tk()
root.title("SmartCare - Doctor Dashboard")
root.geometry("400x400")
root.configure(bg="#f0f4f8")

tk.Label(root, text="Doctor Dashboard", font=("Helvetica", 16, "bold"), bg="#f0f4f8").pack(pady=15)
tk.Label(root, text="Live Patient Queue:", font=("Arial", 12), bg="#f0f4f8").pack()

# Listbox widget to display multiple items (the queue)
queue_listbox = tk.Listbox(root, width=40, height=12, font=("Arial", 12))
queue_listbox.pack(pady=10)

# Button to call the next patient
call_btn = tk.Button(root, text="Call Next Patient", font=("Arial", 12), bg="#2196F3", fg="white", command=call_next_patient)
call_btn.pack(pady=10)

# --- Start Multithreading ---
# We create a daemon thread (it automatically dies when we close the GUI)
bg_thread = threading.Thread(target=fetch_queue_from_server, daemon=True)
bg_thread.start()

# Start the safe GUI updater loop
root.after(500, update_gui_from_queue)

# Start the Tkinter Event Loop
root.mainloop()