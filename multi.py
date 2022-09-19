# example of killing a process
from time import sleep
from multiprocessing import Process
from subprocess import Popen, PIPE, STDOUT


# custom task function
def task():
    path = "show_mac.exe"
    log_file = "recv_mac3"
    rssi = "-75"
    sub_proc = Popen([path], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    input_data = "{}.log\n {}\n".format(log_file, rssi)
    sub_proc.communicate(input=input_data.encode())
    print('Worker process running...', flush=True)



# entry point
if __name__ == '__main__':
    # create a process
    process = Process(target=task)
    # run the process
    process.start()
    # wait for a moment
    sleep(5)
    # kill the process
    if process.is_alive():
        process.kill()
    # continue on...
    print('Parent is continuing on...')