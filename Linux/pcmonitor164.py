""" 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details. 

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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

