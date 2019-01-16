import threading
import queue
import getopt
import time 
import struct 
import sys 
import OpenMV_IN 
import OpenMV_Handler
import Roborio_IN

if __name__ == '__main__':
	#opts, args = getopt.getopt(sys.argv[1:], 'l:r:m:', ['left=', 'right=', 'mouse='])
	robot = Roborio_IN.Roborio()
	camera = OpenMV_IN.Reciever()
	handler = OpenMV_Handler.Handler()
	
	time.sleep(0.01) #let the camera decoding start up before the in thread

	robot_in_thread = threading.thread(target = robot.in_loop)
	robot_out_thread = threading.thread(target = robot.filter_loop, args = ( handler.get_ball_info, handler.get_ball_info ))
	camera_thread = threading.Thread(target = camera.in_loop)
	handler_thread = threading.Thread(target = handler.loop)

	robot_in_thread.daemon = True #ensure the threads close when oo.py is stopped
	robot_out_thread.daemon = True
	camera_thread.daemon = True
	handler_thread.daemon = True

	robot_in_thread.start()
	robot_out_thread.start()
	camera_thread.start()
	handler_thread.start()
	time.sleep(0.01) #wait for the thread to completely start up

	while camera.get_message() is None:
		#print('none')
		time.sleep(0.001)

	while True:
		handler.put_data(camera.get_message())
		ball_info = handler.get_ball_info()
		if ball_info is not None:
			print("Ball: {0}".format(ball_info))
		time.sleep(0.001)
