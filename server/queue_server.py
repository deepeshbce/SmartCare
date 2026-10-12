import socket
import threading

# This list will hold our patients
patient_queue = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        try:
            # Receive data from the client (up to 1024 bytes)
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break # Client disconnected
            
            # Our custom message format uses colons, e.g., "REGISTER:Deepesh:Emergency"
            parts = msg.split(':')
            command = parts[0]
            
            if command == "REGISTER":
                name = parts[1]
                p_type = parts[2]
                
                if p_type == "Emergency":
                    # EMERGENCY Priority: Insert at the front of the list (index 0)
                    patient_queue.insert(0, f"{name} (Emergency)")
                else:
                    # NORMAL: Add to the end of the list
                    patient_queue.append(f"{name} (Normal)")
                    
                conn.send("Success".encode('utf-8'))
                
            elif command == "NEXT":
                if len(patient_queue) > 0:
                    # pop(0) removes and returns the first patient in the list
                    next_patient = patient_queue.pop(0)
                    conn.send(next_patient.encode('utf-8'))
                else:
                    conn.send("Queue is empty".encode('utf-8'))
                    
            elif command == "GET_QUEUE":
                # Join the list into a single comma-separated string to send to the GUI
                queue_str = ",".join(patient_queue)
                if queue_str == "":
                    queue_str = "Empty"
                conn.send(queue_str.encode('utf-8'))
                
        except Exception as e:
            print(f"[ERROR] Connection lost with {addr}: {e}")
            break
            
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    # 127.0.0.1 means "this local computer". Port 5000 is an open channel we choose to use.
    host = '127.0.0.1' 
    port = 5000
    
    # Create the socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen() # Start listening for incoming connections
    
    print(f"[STARTING] Hospital Server is running on {host}:{port}")
    
    while True:
        # accept() waits here until a new client connects
        conn, addr = server.accept()
        
        # Multithreading: Create a new background thread for every client that connects
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        # threading.active_count() - 1 gives us the number of connected clients
        print(f"[ACTIVE CLIENTS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()