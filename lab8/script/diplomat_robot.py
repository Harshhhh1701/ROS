#!/usr/bin/python3
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from numpy import inf
from math import pi
class IrritationRobot:
   def __init__(self):
       rospy.Subscriber("/scan", LaserScan, self.laserData_cb)
       self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
       self.robot_velocity = Twist()
   def laserData_cb(self, data):
       laser_data = np.array(data.ranges)
       laser_data[laser_data == inf] = -1000
       laser_data=max(laser_data)
       rospy.loginfo(laser_data)
       if(laser_data < 1 and laser_data >0):
           self.irritated()
       else:
           self.move_forward()
   def irritated(self):
       rospy.loginfo("I am irritated")
       self.robot_velocity.linear.x = 0.0
       self.robot_velocity.angular.z = 0.5
       self.pub.publish(self.robot_velocity)
       rospy.sleep(3)
       self.robot_velocity.linear.x = 0.5
       self.robot_velocity.angular.z = 0.0
       self.pub.publish(self.robot_velocity)
       rospy.sleep(3)
   def move_forward(self):
       rospy.loginfo("CHARGEEEEEE!!!")
       self.robot_velocity.linear.x = 0.5
       self.robot_velocity.angular.z = 0.0
       self.pub.publish(self.robot_velocity)
if __name__=="__main__":
   rospy.init_node("object_irritation_robot")
   IrritationRobot()
   rospy.spin()
