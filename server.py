import socket
from _thread import *
import threading

print_lock = threading.Lock()


# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break
        if data:
            print("data received.")
            print("data: ", data)

        # handling input (in this case Json)
        ####
        ####
        c.send(data)
    # connection closed
    c.close()


def MainS():
    # any address that machine happens to have.
    host = ""
    port = 8081
    # making basic socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server socket visible within the machine.
    s.bind((host, port))
    print("socket binded to port", port)
    # server listing mode (queue up as 5 connect requests before refusing anymore).
    s.listen(5)
    print("socket is listening")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    MainS()
