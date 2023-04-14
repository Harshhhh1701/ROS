#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
from math import pi

def square_movement_node():
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	rospy.init_node('tbsim_driver',anonymous=True)
	rate = rospy.Rate(1)

	move_cmd1 = Twist()
	move_cmd1.linear.x = 0.1
	move_cmd1.angular.z = 0;
	
	
	turn_cmd = Twist()
	turn_cmd.linear.x = 0
	turn_cmd.angular.z = pi/2; 
	
	
	while not rospy.is_shutdown():
		
		for x in range(0,20):
			pub.publish(move_cmd1)
			rate.sleep()
			
		pub.publish(turn_cmd)
		rate.sleep() 
		
		for x in range(0,9):
			pub.publish(move_cmd1)
			rate.sleep()
			
			
		pub.publish(turn_cmd)
		rate.sleep()            
		

		
if __name__ == '__main__':
	try:
		square_movement_node()
	except rospy.ROSInterruptException:
		pass
