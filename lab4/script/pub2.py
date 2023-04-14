#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def encrypt(text,s):
	result = " "
	# transverse the plain text
	for i in range(len(text)):
		char = text[i]
		# Encrypt uppercase characters in plain text

		if (char.isupper()):
		 result += chr((ord(char) + s-65) % 26 + 65)
		# Encrypt lowercase characters in plain text
		else:
		 result += chr((ord(char) + s - 97) % 26 + 97)
	return result


def packet_name_callback(data: str):
	encrypted_packet = encrypt(data,3)
	# Increment the number of packets
	print("Received packet name:", data.data)
	pub = rospy.Publisher("security", String, queue_size=10)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown(): 
		rospy.loginfo(encrypted_packet)
		pub.publish(encrypted_packet)
		rate.sleep()
		

		
def subscriber_node():
	rospy.init_node("subscriber", anonymous=True)
	# Subscribing to the packet name topic
	rospy.Subscriber("packet_name", String, packet_name_callback)
	rospy.spin()

if __name__ == '__main__':
	
	subscriber_node()
	
		
