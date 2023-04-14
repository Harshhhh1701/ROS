#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def packet_publisher_node():
	rospy.init_node("packet_publisher", anonymous=True)
	pub = rospy.Publisher("packet_name", String, queue_size=10)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		packet_name = "VITCC " 
		rospy.loginfo(packet_name)
		pub.publish(packet_name)
		rate.sleep()


if __name__ == '__main__':
	try: 
		packet_publisher_node()
	except rospy.ROSInterruptException:
		pass
		
