#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def this_course(data: str):
    rospy.loginfo("I took: %s", data.data)

def listener():
    rospy.init_node('subscriber_node_final', anonymous = True)
    rospy.Subscriber("P1", String, this_course)
    rospy.Subscriber("P2", String, this_course)
    rospy.Subscriber("P3", String, this_course)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass