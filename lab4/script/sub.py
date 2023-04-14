#!/usr/bin/env python3
import rospy
import message_filters
from std_msgs.msg import String
from std_msgs.msg import Int32


def int_callback(data):
    
    num_packets = data.data
    print("Received number of packets:", num_packets)

def subscriber_node():
	rospy.init_node("subscriber", anonymous=True)
	# Subscribing to the packet name topic
	rospy.Subscriber("num_packets", Int32, int_callback)
	rospy.spin()

if __name__ == '__main__':
	subscriber_node()
