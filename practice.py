import socket
import keyboard
import time
import fmpy

host, port = "127.0.0.1", 25001
data_arr = [0, 0, 0]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((host, port))

    while True:
        if keyboard.is_pressed(80):
            data_arr[1] -= 0.1
            time.sleep(0.001)
        
        if keyboard.is_pressed(72):
            data_arr[1] += 0.1
            time.sleep(0.001)

        data = "".join(str(data_arr))
        data = data.strip('[')
        data = data.strip(']')

        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")

        print(response)

finally:
    sock.close()