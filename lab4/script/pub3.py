#!/usr/bin/env python3
import rospy
from std_msgs.msg import String,Int32



def security_callback(data):
	print("Received encrypted packet:", data.data)
	pub = rospy.Publisher("num_packets", Int32, queue_size=10)
	rate = rospy.Rate(1)
	count = len(data)
	while not rospy.is_shutdown():
		
		rospy.loginfo(count)
		pub.publish(count)
		rate.sleep()



def subscriber_node():
	rospy.init_node("subscriber", anonymous=True)
	# Subscribing to the packet name topic
	rospy.Subscriber("security", String, security_callback)
	rospy.spin()

if __name__ == '__main__':
	subscriber_node()
