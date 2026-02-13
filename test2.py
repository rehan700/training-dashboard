import socket

try:
    socket.create_connection(("smtp.gmail.com", 587), timeout=5)
    print("Port is OPEN")
except Exception as e:
    print("Port BLOCKED:", e)
