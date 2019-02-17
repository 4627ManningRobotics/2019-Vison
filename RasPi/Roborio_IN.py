import serial
import time
import queue
import json

class Roborio:

	#recognized calls
	RTS = "RTS"
	RTR = "RTR"
	BALL = "BALL"
	MOUSE = "MOUSE"
	
	def __init__(self):
		self._rob = serial.Serial('/dev/roborio', baudrate = 115200, timeout = 0, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
		self._buffer = u''
		self.messages = queue.Queue(20)
		
	def in_loop(self):
		message = ""
		while True:
			input = self._rob.read(1024)
			self._buffer += input.decode("utf-8", "ignore")

			while u'\n' in self._buffer:
				idx = self._buffer.find(u'\n')
				message = self._buffer[:idx]
				self._buffer = self._buffer[idx + 1:]
				if self.messages.full():
					self.messages.get(2)
				print(message)
				self.messages.put(message)
			time.sleep(0.0001)

	def filter_loop(self, funcList):
		send = ""
		while True:
			for key in iter(self.messages.get, None):
				if key == Roborio.RTS:
					send = funcList[0]()
				elif key == Roborio.RTR:
					send = funcList[1]()
				elif key == Roborio.BALL:
					send = funcList[2]()
				elif key == Roborio.MOUSE:
					send = funcList[3]()

				if send != None:
					print(send)
					self._rob.write( bytes( json.dumps( send ) + "\n", "UTF-8"))
				send = ""
				time.sleep(0.0001)
