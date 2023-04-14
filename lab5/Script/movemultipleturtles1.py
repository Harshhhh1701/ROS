#!/usr/bin/env python3
import rospy
import random
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
 
def create_dogobot():
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    dogobot_x = 1
    dogobot_y = 1
    dogobot_theta = 0
    dogobot_name = "dogobot"
    spawner(dogobot_x, dogobot_y, dogobot_theta, dogobot_name)
 
def create_catobot():
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    catobot_x = 9
    catobot_y = 9
    catobot_theta = 0
    catobot_name = "catobot"
    spawner(catobot_x, catobot_y, catobot_theta, catobot_name)
 
def move_dogobot():
    pub = rospy.Publisher('/dogobot/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    twist = Twist()
    twist.linear.x = 2 + random.uniform(-1, 1)
    twist.angular.z = 2 + random.uniform(-1, 1)
    pub.publish(twist)
    rate.sleep()
 
def move_catobot():
    pub = rospy.Publisher('/catobot/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    twist = Twist()
    twist.linear.x = -2 + random.uniform(-1, 1)
    twist.angular.z = -2 + random.uniform(-1, 1)
        
    pub.publish(twist)
    rate.sleep()
 
if __name__== '__main__':
    try:
        rospy.init_node('turtle_spawner')
        create_dogobot()
        create_catobot()
        while not rospy.is_shutdown():
            move_dogobot()
            move_catobot()
    except rospy.ROSInterruptException:
        pass
