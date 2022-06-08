# Import socket module
import socket
from time import sleep


def Main():
    # connection is lost or not.
    # defined host local.
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 8081

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    s.connect((host, port))
    print('socket port is', s.getsockname())

    # message you send to server
    message = "hello this is client 1 speaking."
    while True:
        connected = True
        try:
            # message sent to server
            s.send(message.encode('ascii'))

            # message received from server
            data = s.recv(1024)

            # print the received message
            # here it would be a reverse of sent message
            print('Received from the server :', str(data.decode('ascii')))

            # ask the client whether he wants to continue
            ans = input('\nDo you want to continue(y/n) :')
            if ans == 'y':
                continue
            else:
                break
        # server failure exception.
        except socket.error:
            connected = False
            print("connection lost... reconnecting")
            while not connected:
                # attempt to reconnect, otherwise sleep for 2 seconds
                try:
                    # create socket and try to connect the socket until it success.
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, port))
                    connected = True
                    print("re-connection successful")
                except socket.error:
                    sleep(2)
    s.close()


if __name__ == '__main__':
    Main()
