#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def talker():
	rospy.init_node('publisher_node',anonymous=True)
	pub = rospy.Publisher('lec1', String, queue_size=10)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		_string = "ROS Knowledge"
		rospy.loginfo(_string)
		pub.publish(_string)
		rate.sleep()

if __name__ == '__main__':
	try: 
		talker()
	except rospy.ROSInterruptException:
		pass
		
