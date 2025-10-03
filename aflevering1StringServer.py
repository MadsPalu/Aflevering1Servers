from socket import *
import threading
import random

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print('Server is ready to listen')


def do_add(a, b):
    return a + b

def do_subtract(a, b):
    return a - b

def do_random(a, b):
    return random.randint(a, b)


def handleClient(connectionSocket, address):
    print(f"[{address}] connected")

    while True:
        data = connectionSocket.recv(1024)
        if not data:
            break

        op = data.decode().strip().lower()

        connectionSocket.sendall(b"Input numbers \"a b\"\n")

        nums = connectionSocket.recv(1024).decode().strip()
        parts = nums.split()

        a = int(parts[0])
        b = int(parts[1])

        if op == "add":
            res = do_add(a, b)
        if op == "subtract":
            res = do_subtract(a, b)
        if op == "random":
            res = do_random(a, b)

        connectionSocket.sendall(f"{res}\n".encode())

    connectionSocket.close()
    print(f"[{address}] disconnected")


while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket, addr)).start()
