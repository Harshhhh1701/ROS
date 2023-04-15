#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from cryptography.fernet import Fernet

rospy.init_node('publisher_node_2_and_subscriber_node_mediate', anonymous = True)

def cipher_ceaser(txt, n):
    s = ""
    txt = txt.lower()
    for x in txt:
        s += chr((ord(x) + n - 97) % 26 + 97)
    return s

def talker(text):

    pub = rospy.Publisher('P2', String, queue_size=10)
    rate = rospy.Rate(1)

    _string = cipher_ceaser(text, 3)
    rospy.loginfo(_string)
    pub.publish(_string)
    rate.sleep()

def receiver(data: str):
    while not rospy.is_shutdown():
        rospy.loginfo("I took %s", data.data)
        text = data.data
        try:
            talker(text)
        except rospy.ROSInterruptException:
            pass

def listener():
    rospy.Subscriber("P1", String, receiver)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass