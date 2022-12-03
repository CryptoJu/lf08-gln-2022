import psutil                                                                                     
import platform                                                                                    
import socket

class Computer():
    powerSupply= '12v'                                 

    def __init__(self, cpu, cpuSpeed, ram, os, ip):
        self._cpu = cpu
        self._cpuSpeed = cpuSpeed
        self._ram = ram
        self._os = os
        self._ip = ip
   
    def getInfo(self):
        self._cpu = platform.uname().processor
        self._cpuSpeed = float(psutil.cpu_freq().max/1024)                                          # Cpu_freq returns float bzw. double already, but just for safety convert again
        self._ram = int(round(psutil.virtual_memory().total/ (1024**3), 0))                         # same here with int. Divide 3 times by 1024 to get GiB instead of bytes
        self._os = platform.platform()                                                              # can also use sys.platform but it returns 'win32' for windows. Plaform.platform() output is prettier 
        host = socket.gethostname()                                                                 
        self._ip = socket.gethostbyname(str(host))

        print(f'\n\tCPU: {self._cpu}\n\tcpuSpeed: {psutil.cpu_count(logical=False)}x {self._cpuSpeed:.2f} GhZ\n\tRAM: {self._ram} GB\n\tOS: {self._os}\n\tIP: {self._ip}')                                            
        # .2f rounds float to two decimal places which is prettier in output




