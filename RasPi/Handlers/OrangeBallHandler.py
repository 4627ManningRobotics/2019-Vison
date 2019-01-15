import queue
import threading
import time
import json

class OrangeBall_Handler:

	def __init__(self, queue_size):
		#using a queue to store unfiltered data
		self.ball_queue = queue.Queue(queue_size)
		self.ball_data = queue.Queue(queue_size)

	def put(self, message):
		if(self.ball_queue.full()):
			self.ball_queue.get(2)
			self.ball_queue.put(message, 2)
		else:
			self.ball_queue.put(message, 2)

	def get(self):
		if(self.ball_queue.empty()):
			pass
		else:
			return self.ball_data.get(2)

	def loop(self):
		while True:
			if(self.ball_queue.empty()):
				time.sleep(0.1)
			else:
				m = self.ball_queue.get(2)
				#print( m )
				self.ball_data.put(m) 
				time.sleep(0.02)
