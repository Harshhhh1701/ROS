#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

count = 0

def talker():
    global count
    pub = rospy.Publisher('P3', String, queue_size=10)
    rate = rospy.Rate(1)
    count = count + 1
    _string = "Number of packets received and encrypted: " + str(count) + "."
    rospy.loginfo(_string)
    pub.publish(_string)
    rate.sleep()

def receiver(data: str):
    rospy.loginfo("I took %s", data.data)
    text = data.data
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

def listener():
    rospy.init_node('subscriber_node', anonymous = True)
    rospy.Subscriber("P2", String, receiver)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass