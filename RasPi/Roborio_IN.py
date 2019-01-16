import serial
import time
import queue
import json

class Roborio:

	#recognized calls
	STRIP = "STRIP"
	BALL = "BALL"
	
	def __init__(self):
		self._rob = serial.Serial('dev/roborio', baudrate = 9600)
		self._buffer = u''
		self.messages = queue.Queue(20)
		self.out_queue = queue.Queue(100)
		
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
				self.messages.put(message)

	def filter_loop(self, funcList):
		send = ""
		for key in iter(self.messages.get, None):
			if key == Roborio.STRIP:
				send = funcList[0]()
			elif key == Roborio.BALL:
				send = funcList[1]()

			if not send == "":
				self.rob.write( bytes( json.dumps( send )))
			time.sleep(0.01)
