from socket import *
import threading
import json
import random

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print('Server is ready to listen')


def do_add(values):
    a, b = values
    return a + b

def do_subtract(values):
    a, b = values
    return a - b

def do_random(values):
    a, b = values
    if a > b:
        raise ValueError("For Random, first value must be <= second value")
    return random.randint(a, b)


def handleClient(connectionSocket, address):
    print(f"[{address}] connected")
    connectionSocket.sendall("please use JSON format like this: {\"funktion\": \"Random\", \"values\": [1, 10]}".encode())
    
    try:
        #breaks if connections lost
        while True:
            data = connectionSocket.recv(1024)
            if not data:
                break

            #checks for valid JSON, example: {"funktion": "Random", "values": [1, 10]}
            try:
                jsonInput = json.loads(data.decode())
            except json.JSONDecodeError:
                print("Invalid JSON received")
                connectionSocket.sendall("Invalid JSON\n".encode())
                continue
            
            #checks if json input contains the 2 ints to complete the functions
            values = jsonInput.get("values")
            if (
                not isinstance(values, list)
                or len(values) != 2
                or not all(isinstance(v, int) for v in values)
            ):
                connectionSocket.sendall("Values must be a list of two integers\n".encode())
                continue

            fn = jsonInput.get("funktion")

            if fn == "Add":
                connectionSocket.sendall(str(do_add(jsonInput["values"])).encode())
            elif fn == "Subtract":
                connectionSocket.sendall(str(do_subtract(jsonInput["values"])).encode())
            elif fn == "Random":
                connectionSocket.sendall(str(do_random(jsonInput["values"])).encode())
            else:
                connectionSocket.sendall(b"Unknown funktion")

    finally:
        connectionSocket.close()
        print(f"[{address}] disconnected")


while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket, addr)).start()