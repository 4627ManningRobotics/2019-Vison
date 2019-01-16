import serial
import json
import time
import threading
import queue

class Reciever:

	def __init__(self):
		self.openMVIn = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout = 0)
		self.message = ""
		self.decode_queue = queue.Queue(10000) #yes this is a MASSIVE queue
		self.messages = queue.Queue(100)

		self.decoder_thread = threading.Thread( target = self.decode_loop )
		self.decoder_thread.daemon = True
		self.decoder_thread.start()

	def in_loop(self):
		while True:
			input = self.openMVIn.read(1)
			self.decode_queue.put_nowait(input)

	def decode_loop(self):
		while True:
			c = self.decode_queue.get(2)
			if c == b'\n':
				if self.messages.full():
					self.messages.get(2) #waste least recent
				self.messages.put(self.message, 2)
				self.message = ""
			else:
				self.message += c.decode("utf-8", "ignore")

	def get_message(self):
		if(self.messages.empty()):
			pass
		else:
			return self.messages.get(2)
