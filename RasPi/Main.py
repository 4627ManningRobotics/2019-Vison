#!/usr/bin/python3 
import threading
import queue
import getopt
import time 
import struct 
import sys 
import OpenMV_IN 
import OpenMV_Handler
import Roborio_IN
import Mouse

if __name__ == '__main__':
	#opts, args = getopt.getopt(sys.argv[1:], 'l:r:m:', ['left=', 'right=', 'mouse='])
	robot = Roborio_IN.Roborio()
	camera = OpenMV_IN.Reciever()
	handler = OpenMV_Handler.Handler()
	mouse = Mouse.Mouse("/dev/input/event0")
	
	time.sleep(0.01) #let the camera decoding start up before the in thread

	a = [ handler.get_RTS_info, handler.get_RTR_info, handler.get_ball_info, mouse.get_robot_out ]

	robot_in_thread = threading.Thread(target = robot.in_loop)
	robot_out_thread = threading.Thread(target = robot.filter_loop, args = [a] )
	camera_thread = threading.Thread(target = camera.in_loop)
	handler_thread = threading.Thread(target = handler.loop)
	mouse_thread = threading.Thread(target = mouse.loop)

	robot_in_thread.daemon = True #ensure the threads close when oo.py is stopped
	robot_out_thread.daemon = True
	camera_thread.daemon = True
	handler_thread.daemon = True
	mouse_thread.daemon = True

	robot_in_thread.start()
	robot_out_thread.start()
	camera_thread.start()
	handler_thread.start()
	mouse_thread.start()
	time.sleep(0.01) #wait for the thread to completely start up

	while camera.get_message() is None:
		#print('none')
		time.sleep(0.0001)

	while True:
		handler.put_data(camera.get_message())
		#ball_info = handler.get_ball_info()
		#if ball_info is not None:
			#print("Ball: {0}".format(ball_info))
		time.sleep(0.0001)
