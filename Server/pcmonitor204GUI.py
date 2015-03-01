
""" This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import sys,glob,psutil,serial,time,threading
from gi.repository import Gtk
def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM' + str(i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		ports = glob.glob('/dev/tty[A-Za-z]*')
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result
portszeregowy = "no"
run = True


def proces():

	ser = serial.Serial(portszeregowy, 9600)
	while(run==True):

		ileproc = 0
		cpu = ['101', '101', '101', '101']
		cpu_text = ['BRAK', 'BRAK', 'BRAK', 'BRAK']
		if psutil.cpu_count()==1:
			cpu_text[0]=str(int(psutil.cpu_percent()))
		else:
			for cpus in range(0,psutil.cpu_count()):
				cpu[cpus]=str(int(psutil.cpu_percent(percpu=True)[cpus]))
				#cpu[cpus]=str(int(20))
				if (int(cpu[cpus])<10):
					cpu_text[cpus]="  "+cpu[cpus]+"%"
				elif int(cpu[cpus])==100:
					cpu_text[cpus]=cpu[cpus]+"%"
				else:
					cpu_text[cpus]=" "+cpu[cpus]+"%"
		for proc in psutil.process_iter():
			try:
				pinfo = proc.as_dict(attrs=['pid', 'name'])
			except psutil.NoSuchProcess:
				pass
			else:
				ileproc = ileproc+1
		anam = "Wolny Ram "+str(int(psutil.virtual_memory().available/1000000))+"Mb"
		anam = anam.encode()
		cpu = cpu_text[0]+"|"+cpu_text[1]+"||"+cpu_text[2]+"|"+cpu_text[3]
		cpu=cpu.encode()
		date =time.strftime("%X") +" || "+time.strftime("%x")
		ileproc = str(ileproc)
		ileproc +=" procesow"
		date=date.encode()
		ileproc =ileproc.encode()


		ser.write(b'%')
		time.sleep(0.01)
		ser.write(b'!')
		time.sleep(0.01)
		ser.write(date)
		time.sleep(0.01)
		ser.write(b'@')
		time.sleep(0.01)
		ser.write(anam)
		time.sleep(0.01)
		ser.write(b'#')
		time.sleep(0.01)
		ser.write(ileproc)
		time.sleep(0.01)
		ser.write(b'$')
		time.sleep(0.01)
		ser.write(cpu)
		time.sleep(0.5)
	else:
		ser.write(b'%')
		ser.write(b'Usluga Zamknieta')
		ser.close()

class OknoStart(Gtk.Window):

	def __init__(self):
		self.port = "no"
		self.running = False
		Gtk.Window.__init__(self, title="PCMonitor Server")
		self.set_border_width(5)
		self.text1 = Gtk.Label("Na jakim porcie jest arduino?")
		self.text2 = Gtk.Label("Usluga nieaktywna")
		self.przycisk = Gtk.Button("Wystartuj Usluge")
		self.przyciskstop = Gtk.Button("Wylacz Usluge")
		self.porty = Gtk.ListStore(str)
		for s in serial_ports():
			self.porty.append([s])

		self.vbox = Gtk.VBox(spacing=5)

		self.portcombo = Gtk.ComboBox.new_with_model(self.porty)
		self.portcombo.connect("changed", self.ustaw_port)
		self.przycisk.connect("clicked", self.start)
		self.przyciskstop.connect("clicked", self.stop)
		self.vbox.pack_start(self.text1, False, False, 0)
		self.rtext = Gtk.CellRendererText()
		self.portcombo.pack_start(self.rtext, True)
		self.portcombo.add_attribute(self.rtext, "text", 0)
		self.vbox.pack_start(self.portcombo, False, False, 0)
		self.vbox.pack_start(self.przycisk, False, False, 0)
		self.vbox.pack_start(self.przyciskstop, False, False, 0)
		self.vbox.pack_start(self.text2, False, False, 0)

		self.add(self.vbox)

	def ustaw_port(self, combo):
		global portszeregowy
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			portszeregowy = model[tree_iter][0]
	def start(self, widget):
		global run
		if portszeregowy=="no":
			self.text2.set_text("Nie podano portu")
		else:
			run = True
			self.text2.set_text("Usluga Aktywna")
			global t
			t = threading.Thread(target=proces)
			t.deamon = False
			t.start()

	def stop(self, widget):
		self.text2.set_text("Usluga nieaktywna")
		global run
		run = False

def quit(self, widget):
	global run
	Gtk.main_quit()
	run = False
win = OknoStart()
win.connect("delete-event", quit)
win.show_all()
Gtk.main()
