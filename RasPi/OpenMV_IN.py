import serial
import json
import time
import threading
import queue

class Reciever:

	def __init__(self):
		self._openMVIn = serial.Serial('/dev/openmv', baudrate = 115200, timeout = 0)
		#self._openMVIn = serial.Serial('/dev/ttyACM0', baudrate = 115200, timeout = 0)
		self._buffer = u''
		#self.decode_queue = queue.Queue(10000) #yes this is a MASSIVE queue
		self.messages = queue.Queue(100)

		#self.decoder_thread = threading.Thread( target = self.decode_loop )
		#self.decoder_thread.daemon = True
		#self.decoder_thread.start()

	def in_loop(self):
		while True:
			input = self._openMVIn.read(1024)
			self._buffer += input.decode("utf-8", "ignore")
			
			while u'\n' in self._buffer:
				idx = self._buffer.find(u'\n')
				message = self._buffer[:idx]
				self._buffer = self._buffer[idx + 1:]
				if self.messages.full():
					self.messages.get(2)
				self.messages.put(message) 

	def get_message(self):
		if(self.messages.empty()):
			pass
		else:
			return self.messages.get(2)
