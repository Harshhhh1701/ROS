#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
from math import pi

def square_movement_node():
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	rospy.init_node('tbsim_driver',anonymous=True)
	rate = rospy.Rate(1)

	# forward at 0.2 m/s
	move_cmd = Twist()
	move_cmd.linear.x = 0.1
	move_cmd.angular.z = 0;

	#turn at 45 deg/s
	turn_cmd = Twist()
	turn_cmd.linear.x = 0
	turn_cmd.angular.z = pi*2/4; #45 deg/s in radians/s
	
	while not rospy.is_shutdown():
		
		for x in range(0,10):
			pub.publish(move_cmd)
			rate.sleep()
			
		pub.publish(turn_cmd)
		rate.sleep()            
		

		
if __name__ == '__main__':
	try:
		square_movement_node()
	except rospy.ROSInterruptException:
		pass
