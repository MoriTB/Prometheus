import os
import psutil
import datetime


# cpu usage calculator with 3 different mode.
def cpu_Usage_cal(mode):
    load1, load5, load15 = psutil.getloadavg()
    # cpu usage measurement for the last 1 minute.
    if mode == 1:
        final = load1
    # cpu usage measurement for the last 5 minutes.
    if mode == 2:
        final = load5
    # cpu usage measurement for the last 15 minutes.
    else:
        final = load15
    cpu_usage = (final / os.cpu_count()) * 100
    return cpu_usage


# ram usage percent atm.
def ram_usage():
    # print('RAM memory % used:', psutil.virtual_memory()[2])
    return psutil.virtual_memory()[2]


# storage used space percent atm.
def disk_used():
    disk_use = psutil.disk_usage('/')[3]
    return disk_use


# network
# network send bytes.
def network_send():
    byte_send = (psutil.net_io_counters())[0]
    return byte_send


# network received bytes.
def network_receive():
    byte_receive = (psutil.net_io_counters())[1]
    return byte_receive


# network packet send.
def network_pack_send():
    packet_send = (psutil.net_io_counters())[3]
    return packet_send


# network packet received.
def network_pack_receive():
    packet_receive = (psutil.net_io_counters())[4]
    return packet_receive


# other info about system
# boot time in seconds.
def boot_time():
    boot_timer = psutil.boot_time()
    boot_timer
    return boot_timer


if __name__ == '__main__':

    data = {"cpu_usage": cpu_Usage_cal(1),
            "ram_usage": ram_usage(),
            "disk_used":disk_used(),
            "network_send_byte":network_send(),
            "network_receive_byte":network_receive(),
            "boot_time":boot_time()} # a real dict
    print(data)