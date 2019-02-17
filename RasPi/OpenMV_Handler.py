import queue
import threading
import time
import json
from Handlers import OrangeBallHandler
from Handlers import StripHandler
from Handlers import RoboHandler

class Handler:
	
	def __init__(self):
		self.data = queue.Queue(100)
		self.orange_ball_key = "BALL"
		self.RTS_key = "RTS"
		self.RTR_key = "RTR"
		self.orange_ball = OrangeBallHandler.OrangeBall_Handler(100)
		self.RTS = StripHandler.Strip_Handler(100)
		self.RTR = RoboHandler.Robo_Handler(100)
		self.init_threads()

	def loop(self):
		while True:
			if(not self.data.empty()):
				d = self.data.get(2)
				if d is not None and d != "":
					try:
						#print("Data: " + d)
						foo = json.loads(d)
						if foo["KEY"] == self.orange_ball_key:
							#print("KEY FOUND!")
							self.orange_ball.put(foo)
							time.sleep(0.0001)
						elif foo["KEY"] == self.RTS_key:
							self.RTS.put(foo)
							time.sleep(0.0001)
						elif foo["KEY"] == self.RTR_key:
							self.RTR.put(foo)
							time.sleep(0.0001)
						else:
							time.sleep(0.0003)
					except:
						time.sleep(0.0001)
				else:
					time.sleep(0.0001)
			else:
				time.sleep(0.0003)

	def put_data(self, d):
		if(self.data.full()):
			self.data.get(2)
			self.data.put(d, 2)
		else:
			self.data.put(d, 2)

	def get_ball_info(self):
		return self.orange_ball.get()

	def get_RTR_info(self):
		return self.RTR.get()

	def get_RTS_info(self):
		return self.RTS.get()

	def init_threads(self):
		#define all threads
		orange_ball_thread = threading.Thread( target = self.orange_ball.loop )
		RTS_thread = threading.Thread( target = self.RTS.loop )
		RTR_thread = threading.Thread( target = self.RTR.loop )

		#the threads MUST close on progam close
		orange_ball_thread.daemon = True
		RTS_thread.daemon = True
		RTR_thread.daemon = True 

		orange_ball_thread.start()
		RTS_thread.start()
		RTR_thread.start()
