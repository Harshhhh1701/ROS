#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from random import randint

class RandomTurtle:
    def __init__(self, name):
        self.name = name
        rospy.init_node(name)
        rospy.Subscriber('/' + name + '/pose', Pose, self.update_pose)
        self.velocity_publisher = rospy.Publisher('/' + name + '/cmd_vel', Twist, queue_size=10)
        self.pose = Pose()
    
    def update_pose(self, data):
        self.pose = data
    
    def move_randomly(self):
        move_cmd = Twist()
        move_cmd.linear.x = randint(1,5)
        move_cmd.angular.z = randint(-3,3)
        self.velocity_publisher.publish(move_cmd)
        
    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.move_randomly()
            rate.sleep()
            
if __name__ == '__main__':
    dogobot = RandomTurtle('dogobot')
    catobot = RandomTurtle('catobot')
    try:
        dogobot.run()
        catobot.run()
    except rospy.ROSInterruptException:
        pass
