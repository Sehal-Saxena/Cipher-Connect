# # server.py
# import socket
# import threading
# import json
# from rsa import RSA
# from sdes import SDES

# class ChatServer:
#     def __init__(self):
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.host = 'localhost'
#         self.port = 5555
#         self.clients = {}  # {client_socket: {'name': name, 'public_key': key}}
#         self.encryption_method = None
#         self.sdes_key = "1010101010"  # Default SDES key (10 bits)
        
#     def select_encryption(self):
#         while True:
#             print("\n=== Chat Server Configuration ===")
#             print("Select encryption method:")
#             print("1. RSA")
#             print("2. SDES")
#             choice = input("Enter your choice (1/2): ").strip()
            
#             if choice == "1":
#                 self.encryption_method = "RSA"
#                 print("\nSelected RSA encryption")
#                 break
#             elif choice == "2":
#                 self.encryption_method = "SDES"
#                 print("\nSelected SDES encryption")
#                 # Optionally allow custom SDES key
#                 custom_key = input("Enter 10-bit key for SDES (press Enter for default key): ").strip()
#                 if custom_key and len(custom_key) == 10 and all(bit in '01' for bit in custom_key):
#                     self.sdes_key = custom_key
#                 print(f"Using SDES key: {self.sdes_key}")
#                 break
#             else:
#                 print("Invalid choice. Please select 1 or 2.")
    
#     def start_server(self):
#         self.server.bind((self.host, self.port))
#         self.server.listen()
#         print(f"\nServer is running on {self.host}:{self.port}")
#         print(f"Encryption method: {self.encryption_method}")
#         print("Waiting for connections...\n")
        
#         while True:
#             client_socket, address = self.server.accept()
#             print(f"New connection from {address}")
#             threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
    
#     def handle_client(self, client_socket, address):
#         try:
#             # First, send encryption method to client
#             encryption_data = {
#                 'method': self.encryption_method,
#                 'sdes_key': self.sdes_key if self.encryption_method == "SDES" else None
#             }
#             client_socket.send(json.dumps(encryption_data).encode())
            
#             # Receive client's initial data (name and public key if RSA)
#             init_data = json.loads(client_socket.recv(1024).decode())
#             name = init_data['name']
#             public_key = init_data.get('public_key')  # Only for RSA
            
#             self.clients[client_socket] = {
#                 'name': name,
#                 'address': address,
#                 'public_key': public_key
#             }
            
#             print(f"\n{name} joined the chat from {address}")
#             self.broadcast(f"{name} joined the chat!", client_socket)
            
#             while True:
#                 try:
#                     message = client_socket.recv(1024).decode()
#                     if not message:
#                         raise Exception("Client disconnected")
                    
#                     # If message is encrypted, it will be handled by the broadcast function
#                     print(f"\nMessage from {name}: {message}")
#                     self.broadcast(f"{name}: {message}", client_socket)
                    
#                 except Exception as e:
#                     print(f"\nError with client {name}: {str(e)}")
#                     break
                    
#         except Exception as e:
#             print(f"\nError handling client {address}: {str(e)}")
        
#         finally:
#             # Clean up on disconnect
#             if client_socket in self.clients:
#                 name = self.clients[client_socket]['name']
#                 del self.clients[client_socket]
#                 client_socket.close()
#                 print(f"\n{name} left the chat")
#                 self.broadcast(f"{name} left the chat!", None)
    
#     def broadcast(self, message, sender_socket):
#         """Broadcast message to all clients except sender"""
#         for client in self.clients:
#             if client != sender_socket:
#                 try:
#                     # In real implementation, message would be encrypted here
#                     # based on the encryption method and client's keys
#                     client.send(message.encode())
#                 except Exception as e:
#                     print(f"\nError broadcasting to {self.clients[client]['name']}: {str(e)}")
    
#     def run(self):
#         try:
#             self.select_encryption()
#             self.start_server()
#         except KeyboardInterrupt:
#             print("\nServer shutting down...")
#         except Exception as e:
#             print(f"\nServer error: {str(e)}")
#         finally:
#             # Clean up
#             for client in list(self.clients.keys()):
#                 client.close()
#             self.server.close()
#             print("Server stopped")

# if __name__ == "__main__":
#     server = ChatServer()
#     server.run()


import socket
import threading
import json
from rsa import RSA
from sdes import SDES

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5555
        self.clients = {}  # {client_socket: {'name': name, 'public_key': key}}
        self.encryption_method = None
        self.sdes_key = "1010101010"  # Default SDES key (10 bits)

    def select_encryption(self):
        while True:
            print("\n=== Chat Server Configuration ===")
            print("Select encryption method:")
            print("1. RSA")
            print("2. SDES")
            choice = input("Enter your choice (1/2): ").strip()

            if choice == "1":
                self.encryption_method = "RSA"
                print("\nSelected RSA encryption")
                break
            elif choice == "2":
                self.encryption_method = "SDES"
                print("\nSelected SDES encryption")
                # Allow custom SDES key
                custom_key = input("Enter 10-bit key for SDES (press Enter for default key): ").strip()
                if custom_key and len(custom_key) == 10 and all(bit in '01' for bit in custom_key):
                    self.sdes_key = custom_key
                print(f"Using SDES key: {self.sdes_key}")
                break
            else:
                print("Invalid choice. Please select 1 or 2.")

    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"\nServer is running on {self.host}:{self.port}")
        print(f"Encryption method: {self.encryption_method}")
        print("Waiting for connections...\n")

        while True:
            client_socket, address = self.server.accept()
            print(f"New connection from {address}")
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def handle_client(self, client_socket, address):
        try:
            # Send encryption method to client
            encryption_data = {
                'method': self.encryption_method,
                'sdes_key': self.sdes_key if self.encryption_method == "SDES" else None
            }
            client_socket.send(json.dumps(encryption_data).encode())

            # Receive client's initial data
            init_data = json.loads(client_socket.recv(1024).decode())
            name = init_data['name']
            public_key = init_data.get('public_key')  # Only for RSA

            self.clients[client_socket] = {
                'name': name,
                'address': address,
                'public_key': public_key
            }

            print(f"\n{name} joined the chat from {address}")
            self.broadcast(f"{name} joined the chat!", client_socket)

            while True:
                try:
                    message = client_socket.recv(1024).decode()
                    if not message:
                        raise Exception("Client disconnected")

                    print(f"\nMessage from {name}: {message}")
                    self.broadcast(f"{name}: {message}", client_socket)

                except Exception as e:
                    print(f"\nError with client {name}: {str(e)}")
                    break

        except Exception as e:
            print(f"\nError handling client {address}: {str(e)}")

        finally:
            # Clean up on disconnect
            if client_socket in self.clients:
                name = self.clients[client_socket]['name']
                del self.clients[client_socket]
                client_socket.close()
                print(f"\n{name} left the chat")
                self.broadcast(f"{name} left the chat!", None)

    def broadcast(self, message, sender_socket):
        """Broadcast message to all clients except sender"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"\nError broadcasting to {self.clients[client]['name']}: {str(e)}")

    def run(self):
        try:
            self.select_encryption()
            self.start_server()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            for client in list(self.clients.keys()):
                client.close()
            self.server.close()
            print("Server stopped")


if __name__ == "__main__":
    server = ChatServer()
    server.run()
