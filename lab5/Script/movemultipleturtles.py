#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import sys
from math import pi

def create_turtle1():
	rospy.wait_for_service('spawn')
	spawner = rospy.ServiceProxy('spawn', Spawn)
	turtle1_x = 1
	turtle1_y = 1
	turtle1_theta = 0
	turtle1_name = "turtle2"
	spawner(turtle1_x, turtle1_y, turtle1_theta, turtle1_name)

def create_turtle2():
	rospy.wait_for_service('spawn')
	spawner = rospy.ServiceProxy('spawn', Spawn)
	turtle2_x = 9
	turtle2_y = 9
	turtle2_theta = 0
	turtle2_name = "turtle3"
	spawner(turtle2_x, turtle2_y, turtle2_theta, turtle2_name)

def circular_movement_node_1():
	pub = rospy.Publisher('/turtle2/cmd_vel',Twist,queue_size=10)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		robot_velocity=Twist()
		robot_velocity.linear.x=2.0
		robot_velocity.angular.z=0.8
		pub.publish(robot_velocity)
		rate.sleep()

def circular_movement_node_2():
	pub = rospy.Publisher('/turtle3/cmd_vel',Twist,queue_size=10)
	rate = rospy.Rate(1)
	robot_velocity=Twist()
	robot_velocity.linear.x=2.0
	robot_velocity.angular.z=0.8
	pub.publish(robot_velocity)
	rate = rospy.Rate(1)
		


if __name__ == '__main__':
    try:
        rospy.init_node('turtle_spawner')
        create_turtle1()
        create_turtle2()
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
        	circular_movement_node_2()
        	rate.sleep()
    except rospy.ROSInterruptException:
        pass

