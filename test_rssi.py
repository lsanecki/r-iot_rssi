from subprocess import Popen, PIPE, STDOUT
from time import sleep
from multiprocessing import Process


def task():
    path = "show_mac.exe"
    log_file = "recv_mac2"
    rssi = "-35"
    print("tesk")
    sub_proc = Popen([path], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    input_data = "{}.log\n {}\n".format(log_file, rssi)
    stdout_data = sub_proc.communicate(input=input_data.encode())


process = Process(target=task)
process.start()
print("rozpoczynam task")
# sleep(5)
# process.kill()
print("Koniec")