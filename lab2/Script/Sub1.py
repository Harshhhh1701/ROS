#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def this_course(data: str):
	rospy.loginfo("I took %s", data.data)

def listener():
	rospy.init_node('subscriber_node',anonymous=True)
	rospy.Subscriber('CSE3102', String, this_course)
	rospy.spin()
		
		

if __name__ == '__main__':
	listener()
