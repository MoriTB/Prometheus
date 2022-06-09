import socket
from _thread import *
import threading
from prometheus_client import *
import json

print_lock = threading.Lock()


# c = Counter('network_bytes_send', 'Description of counter')
# print(c)

# thread function
def threaded(c, i):
    # defining the metrics with the metric type pre-defined in prometheus.
    """""
    network_byte_received = Counter('network_byte_received', 'network bytes received.', ['thread', 'endpoint'])
    network_byte_send = Counter('network_byte_send', 'network bytes send.', ['thread', 'endpoint'])
    g = Gauge('cpu_usage', 'shows cpu usage', ['thread', 'endpoint'])
    g1 = Gauge('ram_usage', 'shows ram usage', ['thread', 'endpoint'])
    g2 = Gauge('disk_used', 'shows disk percentage', ['thread', 'endpoint'])
    g3 = Gauge('boot_time', 'shows disk percentage', ['thread', 'endpoint'])
    """
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break
        if data:
            received = data.decode("utf-8")
            json_received = json.loads(received)
            # counter metrics (network bytes send/receive)
            # network_byte_received = Counter('network_byte_received', 'network bytes received.')
            #network_byte_received.inc(json_received["network_receive_byte"])
            converted_num = str(i)
            client_increase = 'client '+converted_num
            network_byte_received.labels(client_increase, '/').inc(json_received["network_receive_byte"])
            print(network_byte_received)
            # network_byte_send = Counter('network_byte_send', 'network bytes send.')
            #network_byte_send.inc(json_received["network_send_byte"])
            network_byte_send.labels(client_increase, '/').inc(json_received["network_send_byte"])
            print(network_byte_send)
            # gauge metrics( cpu,ram,disk usage and booting)
            # g = Gauge('cpu_usage', 'shows cpu usage')
            #g.set(json_received["cpu_usage"])
            g.labels(client_increase, '/').set(json_received["cpu_usage"])
            # Set to a given value
            # g1 = Gauge('ram_usage', 'shows ram usage')
            #g1.set(json_received["ram_usage"])
            g1.labels(client_increase, '/').set(json_received["ram_usage"])
            # g2 = Gauge('disk_used', 'shows disk percentage')
            #g2.set(json_received["disk_used"])
            g2.labels(client_increase, '/').set(json_received["disk_used"])
            # g3 = Gauge('boot_time', 'shows disk percentage')
            #g3.set(json_received["boot_time"])
            g3.labels(client_increase, '/').set(json_received["boot_time"])
            print(g1)
            print(g2)
            print(g3)
            print(g)
            # affirmation on receiving.
        c.send(bytes("data has been received by the server.", encoding="utf-8"))
    # connection closed
    """""
    registry = CollectorRegistry()
    g = Gauge('raid_status', '1 if raid array is okay', registry=registry)
    g.set(1)
    write_to_textfile('/configured/textfile/path/raid.prom', registry)
    """
    c.close()


def MainS():
    # any address that machine happens to have.
    host = ""
    port = 8103
    # making basic socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server socket visible within the machine.
    s.bind((host, port))
    print("socket binded to port", port)
    # server listing mode (queue up as 5 connect requests before refusing anymore).
    s.listen(5)
    print("socket is listening")
    i = 0
    # a forever loop until client wants to exit
    start_http_server(8000)
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # i is used to declare what client is using the data.
        i = i + 1
        print(i)
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c, i))
    s.close()


if __name__ == '__main__':
    # defined metric type accepted in prometheus.
    network_byte_received = Counter('network_byte_received', 'network bytes received.', ['thread', 'endpoint'])
    network_byte_send = Counter('network_byte_send', 'network bytes send.', ['thread', 'endpoint'])
    g = Gauge('cpu_usage', 'shows cpu usage', ['thread', 'endpoint'])
    g1 = Gauge('ram_usage', 'shows ram usage', ['thread', 'endpoint'])
    g2 = Gauge('disk_used', 'shows disk percentage', ['thread', 'endpoint'])
    g3 = Gauge('boot_time', 'shows disk percentage', ['thread', 'endpoint'])
    MainS()
