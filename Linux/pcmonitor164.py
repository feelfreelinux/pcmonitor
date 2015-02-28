import serial, psutil, time, sys
for arg in sys.argv:
    arg = str(arg) 
ser = serial.Serial(arg, 9600)
while True:
    ser.write(b'linia0')
    cpu1 = str(psutil.cpu_percent(interval=1))
    anam = "Wolny Ram "+str(int(psutil.virtual_memory().available/1000000))+"Mb"
    ser.write(b'czysc')
    ser.write(anam.encode())
    
    cpu = "CPU: "+cpu1+"%"
    time.sleep(0.1)
    ser.write(b'linia1')
    ser.write(cpu.encode())
    time.sleep(1)
