# import socket
# import threading
# import json
# import tkinter as tk
# from tkinter import ttk, scrolledtext
# from datetime import datetime
# from rsa import RSA
# from sdes import SDES
# import tkinter.font as tkFont

# class ChatClient:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.host = 'localhost'
#         self.port = 5555
#         self.encryption_method = None
#         self.rsa = None
#         self.sdes = None
#         self.username = None
#         self.setup_gui()
        
#     def setup_gui(self):
#         self.window = tk.Tk()
#         self.window.title("Secure Chat Client")
#         self.window.geometry("800x600")
        
#         # Define color scheme
#         self.colors = {
#             'bg_main': '#E8EAF6',  # Light blue-grey background
#             'bg_chat': '#FFFFFF',   # White chat background
#             'primary': '#3F51B5',   # Indigo primary color
#             'secondary': '#7986CB', # Lighter indigo
#             'text': '#1A237E',      # Dark indigo text
#             'system_msg': '#78909C' # Blue-grey for system messages
#         }
        
#         self.window.configure(bg=self.colors['bg_main'])
        
#         # Custom fonts
#         self.title_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
#         self.normal_font = tkFont.Font(family="Helvetica", size=11)
#         self.message_font = tkFont.Font(family="Helvetica", size=11)
        
#         # Configure styles
#         style = ttk.Style()
#         style.configure('Custom.TFrame', background=self.colors['bg_main'])
#         style.configure('Custom.TLabel', 
#                        background=self.colors['bg_main'], 
#                        foreground=self.colors['text'])
#         style.configure('Custom.TButton',
#                        background=self.colors['primary'],
#                        foreground='white',
#                        padding=(10, 5))
#         style.configure('Send.TButton',
#                        background=self.colors['secondary'],
#                        padding=(15, 5))
        
#         # Main container
#         main_container = ttk.Frame(self.window, style='Custom.TFrame')
#         main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Login frame
#         self.login_frame = ttk.Frame(main_container, style='Custom.TFrame')
#         self.login_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Create a decorative header
#         header_frame = tk.Frame(self.login_frame, bg=self.colors['primary'])
#         header_frame.pack(fill=tk.X, pady=(0, 20))
#         header_frame.pack_propagate(False)
#         header_frame.configure(height=60)
        
#         title_label = tk.Label(
#             header_frame, 
#             text="Secure Chat",
#             font=self.title_font,
#             bg=self.colors['primary'],
#             fg='white'
#         )
#         title_label.pack(pady=15)
        
#         # Login container with white background
#         login_container = tk.Frame(self.login_frame, bg='white', padx=40, pady=40)
#         login_container.pack(padx=50, pady=(0, 50))
        
#         # Name entry with label
#         name_frame = tk.Frame(login_container, bg='white')
#         name_frame.pack(pady=10)
#         tk.Label(
#             name_frame, 
#             text="Username:",
#             font=self.normal_font,
#             bg='white',
#             fg=self.colors['text']
#         ).pack(side=tk.LEFT, padx=5)
        
#         self.name_entry = tk.Entry(
#             name_frame,
#             width=30,
#             font=self.normal_font,
#             bg='#F5F5F5',
#             relief='flat',
#             highlightthickness=1,
#             highlightcolor=self.colors['primary']
#         )
#         self.name_entry.pack(side=tk.LEFT, padx=5)
        
#         # Connect button
#         self.connect_btn = tk.Button(
#             login_container,
#             text="Connect",
#             command=self.connect_to_server,
#             font=self.normal_font,
#             bg=self.colors['primary'],
#             fg='white',
#             relief='flat',
#             padx=20,
#             pady=10,
#             cursor='hand2'
#         )
#         self.connect_btn.pack(pady=20)
        
#         # Chat frame (initially hidden)
#         self.chat_frame = ttk.Frame(main_container, style='Custom.TFrame')
        
#         # Chat display
#         self.chat_display = scrolledtext.ScrolledText(
#             self.chat_frame,
#             wrap=tk.WORD,
#             font=self.message_font,
#             height=20,
#             bg=self.colors['bg_chat'],
#             relief='flat',
#             padx=10,
#             pady=10
#         )
#         self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
#         # Configure chat display tags
#         self.chat_display.tag_configure('timestamp', foreground='#9E9E9E')
#         self.chat_display.tag_configure('username', foreground=self.colors['primary'], font=self.message_font)
#         self.chat_display.tag_configure('message', font=self.message_font)
#         self.chat_display.tag_configure('system', foreground=self.colors['system_msg'])
        
#         # Message input frame
#         input_frame = tk.Frame(self.chat_frame, bg=self.colors['bg_main'])
#         input_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Message entry
#         self.message_entry = tk.Entry(
#             input_frame,
#             font=self.message_font,
#             bg='white',
#             relief='flat',
#             highlightthickness=1,
#             highlightcolor=self.colors['primary']
#         )
#         self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
#         self.message_entry.bind('<Return>', lambda e: self.send_message())
        
#         # Send button
#         self.send_btn = tk.Button(
#             input_frame,
#             text="Send",
#             command=self.send_message,
#             font=self.normal_font,
#             bg=self.colors['secondary'],
#             fg='white',
#             relief='flat',
#             padx=20,
#             pady=5,
#             cursor='hand2'
#         )
#         self.send_btn.pack(side=tk.RIGHT)
        
#         self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
#     # Rest of the methods remain the same
#     def connect_to_server(self):
#         if not self.name_entry.get():
#             self.display_system_message("Please enter a username!")
#             return
            
#         try:
#             self.username = self.name_entry.get()
#             self.client.connect((self.host, self.port))
            
#             encryption_data = json.loads(self.client.recv(1024).decode())
#             self.encryption_method = encryption_data['method']
            
#             if self.encryption_method == "RSA":
#                 self.rsa = RSA()
#                 init_data = {'name': self.username, 'public_key': self.rsa.public_key}
#             else:
#                 self.sdes = SDES()
#                 init_data = {'name': self.username, 'public_key': None}
            
#             self.client.send(json.dumps(init_data).encode())
            
#             self.login_frame.pack_forget()
#             self.chat_frame.pack(fill=tk.BOTH, expand=True)
            
#             self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
#             self.receive_thread.start()
            
#             self.display_system_message(f"Connected using {self.encryption_method} encryption!")
            
#         except Exception as e:
#             self.display_system_message(f"Connection failed: {str(e)}")
    
#     def display_system_message(self, message):
#         timestamp = datetime.now().strftime("%H:%M")
#         self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
#         self.chat_display.insert(tk.END, f"{message}\n", 'system')
#         self.chat_display.see(tk.END)
    
#     def display_message(self, username, message):
#         timestamp = datetime.now().strftime("%H:%M")
#         self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
#         self.chat_display.insert(tk.END, f"{username}: ", 'username')
#         self.chat_display.insert(tk.END, f"{message}\n", 'message')
#         self.chat_display.see(tk.END)
    
#     def receive_messages(self):
#         while True:
#             try:
#                 message = self.client.recv(1024).decode()
#                 if not message:
#                     break
                
#                 if ": " in message:
#                     username, content = message.split(": ", 1)
#                     self.display_message(username, content)
#                 else:
#                     self.display_system_message(message)
                    
#             except:
#                 self.display_system_message("Disconnected from server")
#                 break
    
#     def send_message(self):
#         message = self.message_entry.get().strip()
#         if message:
#             try:
#                 self.client.send(message.encode())
#                 self.display_message(self.username, message)
#                 self.message_entry.delete(0, tk.END)
#             except:
#                 self.display_system_message("Failed to send message")
    
#     def on_closing(self):
#         try:
#             self.client.close()
#         except:
#             pass
#         self.window.destroy()

#     def run(self):
#         self.window.mainloop()

# if __name__ == "__main__":
#     client = ChatClient()
#     client.run()

import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5555
        self.encryption_method = None
        self.username = None
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Secure Chat Client")
        self.window.geometry("600x500")

        self.login_frame = tk.Frame(self.window)
        self.chat_frame = tk.Frame(self.window)

        # Login frame
        tk.Label(self.login_frame, text="Enter your username:").pack(pady=10)
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.pack(pady=10)
        tk.Button(self.login_frame, text="Connect", command=self.connect_to_server).pack(pady=10)

        # Chat frame
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD)
        self.chat_display.pack(pady=10, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.pack(fill=tk.X, padx=10, pady=5)
        self.message_entry.bind('<Return>', lambda event: self.send_message())

        tk.Button(self.chat_frame, text="Send", command=self.send_message).pack(pady=5)

        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def connect_to_server(self):
        try:
            self.username = self.name_entry.get()
            if not self.username:
                self.display_system_message("Enter a username!")
                return

            self.client.connect((self.host, self.port))
            encryption_data = json.loads(self.client.recv(1024).decode())
            self.encryption_method = encryption_data['method']

            init_data = {'name': self.username}
            self.client.send(json.dumps(init_data).encode())

            self.login_frame.pack_forget()
            self.chat_frame.pack(fill=tk.BOTH, expand=True)

            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.display_system_message(f"Connected with {self.encryption_method} encryption!")
        except Exception as e:
            self.display_system_message(f"Connection failed: {str(e)}")

    def display_system_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"System: {message}\n")
        self.chat_display.configure(state='disabled')

    def display_message(self, username, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{username}: {message}\n")
        self.chat_display.configure(state='disabled')

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if ": " in message:
                    username, msg = message.split(": ", 1)
                    self.display_message(username, msg)
                else:
                    self.display_system_message(message)
            except Exception as e:
                self.display_system_message("Disconnected from server")
                break

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client.send(message.encode())
                self.display_message("You", message)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_system_message("Failed to send message")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    client = ChatClient()
    client.run()
