## Steps

```
1. mkdir myws and cd myws
2. mkdir src
3. catkin_make
4. source in .bashrc
5. cd src
6. catkin_create_pkg mypkg roscpp rospy std_msgs
7. catkin_make in myws level
8. mkdir scripts inside package dir
9. touch mynode.py
10. chmod +x mynode.py
```

## ROS Commands

```
1. rosnode list
2. rosrun mypkg mynode.py
3. rosnode info
4. rosnode kill
5. rosnode ping <name>
6. rosrun rqt_graph rqt_graph
```

## Turtle sim

### To install
```
sudo apt-get install ros-noetic-turtlesim
rosrun turtlesim turtlesim_node
rosrun turtle_teleop_key
* Add dependency pkg gemometry_msgs
```

### Code 1

```py
#!/usr/bin/env python3
import rospy
import sys
from geometry_msgs.msg import Twist

def circleFn(radius):
  rospy.init_node('circle')
  publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
  rate = rospy.Rate(10)
  twist = Twist()
  while not rospy.is_shutdown():
    twist.linear.x = radius
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 1
    rospy.loginfo("Radius = %f", radius)
    publisher.publish(twist)
    rate.sleep()

if __name__ == '__main__':
circleFn(3)
```

### Code 2

```py
#!/usr/bin/env python3
import rospy
import sys
from geometry_msgs.msg import Twist
speed = 3
angular_speed = 2
PI = 3.1415926535897

def move_in_line(side_length,twist,pub):
  twist.linear.x = speed
  twist.linear.y = 0
  twist.linear.z = 0
  twist.angular.x = 0
  twist.angular.y = 0
  twist.angular.z = 0
  t0 = rospy.Time.now().to_sec()
  distance_travelled = 0
  
  while distance_travelled < side_length:
    pub.publish(twist)
    t1 = rospy.Time.now().to_sec()
    distance_travelled = speed*(t1-t0)
    
  twist.linear.x = 0
  pub.publish(twist)

def rotate(twist,pub):
  twist.angular.z = angular_speed
  t0 = rospy.Time.now().to_sec()
  angle_travelled = 0
  
  while ( angle_travelled < PI/2.0 ):
    pub.publish(twist)
    t1 = rospy.Time.now().to_sec()
    angle_travelled = angular_speed*(t1-t0)
  
  twist.angular.z = 0
  pub.publish(twist)

def quadFn(side, rotations):
  rospy.init_node('quad')
  publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)twist = Twist()
  current_rotation = 0
  
  while current_rotation < rotations:
    move_in_line(side, twist, publisher)
    rotate(twist, publisher)
    current_rotation += 0.25
    
if __name__ == '__main__':
  quadFn(2, 1.25)
```

## Publisher and Subscriber

### Code 1 - Subscriber
```py
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback_receive_radio_data(msg):
  rospy.loginfo("Message received:")
  rospy.loginfo(msg)
if __name__ == '__main__':
  rospy.init_node('subscriber')
  sub = rospy.Subscriber("/my_publisher", String, callback_receive_radio_data)
  rospy.spin()
```

### Code 1 - Publisher
```py
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
#from std_msgs.msg import Int8

if __name__ == '__main__':
  rospy.init_node('publisher')
  pub = rospy.Publisher("my_publisher",String, queue_size=10)
  rate = rospy.Rate(2)
  
  while not rospy.is_shutdown():
    msg = String()
    msg.data = "Hi i am publishing"
    pub.publish(msg)
    rate.sleep()
    
  rospy.loginfo("Publisher Node stopped")
```

### Code 2 - Publisher
```py
#!/usr/bin/env python3
import rospy as rp
from std_msgs.msg import String

if __name__=='__main__':
  rp.init_node('publisher')
  publisher = rp.Publisher('/raw_text', String, queue_size=15)
  
  while not rp.is_shutdown():
    text = String()
    text.data = 'chandramauli'
    publisher.publish(text)
    rp.loginfo('Published: ' + text.data)
    rp.sleep(3)
    
  rospy.loginfo("Publisher node stopped")
```
### Code 2 - Middleman 1
```py
#!/usr/bin/env python3
import rospy as rp
import string as s
from std_msgs.msg import String

cipherText: String = String()
def caesar_cipher(text):
  alphabet = s.ascii_lowercase
  shifted_alphabet = alphabet[3:] + alphabet[:3]
  table = str.maketrans(alphabet, shifted_alphabet)
  cipherText.data = text.data.translate(table)
  
  rp.loginfo('Got: ' + text.data)
  rp.loginfo('Changed: ' + cipherText.data)
  rp.loginfo('-------------------------------')

if __name__=='__main__':
  rp.init_node('middleman')
  subscriber = rp.Subscriber('/raw_text', String, caesar_cipher)
  publisher = rp.Publisher('/cipher_text', String, queue_size = 15)
  
  while not rp.is_shutdown():
    publisher.publish(cipherText)
    rp.loginfo('Published: ' + cipherText.data)
    rp.loginfo('-------------------------------')
    rp.sleep(3)
```
### Code 2 - Middleman 2
```py
#!/usr/bin/env python3
import rospy as rp
import string as s
from std_msgs.msg import String

text: String = String()
def de_cipher(coded_text):
  alphabet = s.ascii_lowercase
  shifted_alphabet = alphabet[3:] + alphabet[:3]
  table = str.maketrans(shifted_alphabet, alphabet)
  text.data = coded_text.data.translate(table)
  rp.loginfo('Got: ' + coded_text.data)
  rp.loginfo('Changed: ' + text.data)
  rp.loginfo('-------------------------------')

if __name__=='__main__':
  rp.init_node('middleman2')
  subscriber = rp.Subscriber('/cipher_text', String, de_cipher)
  publisher = rp.Publisher('/text', String, queue_size = 15)
  
  while not rp.is_shutdown():
    publisher.publish(text)
    rp.loginfo('Published: ' + text.data)
    rp.loginfo('-------------------------------')
    rp.sleep(3)
```

## Services

### Code 1 - Server
```py
#!/usr/bin/env python3
import rospy
from rospy_tutorials.srv import AddTwoInts

def handle_add_two_ints(req):
  result = req.a+req.b
  rospy.loginfo("Sum of " +str(req.a)+ " and " +str(req.b) + " is " + str(result))
  return result

if __name__ == '__main__':
  rospy.init_node("server")
  rospy.loginfo("Add two ints server node created")
  service = rospy.Service("/add_two_ints", AddTwoInts, handle_add_two_ints)
  rospy.loginfo("Service server has been started")
  rospy.spin()
```

### Code 1 - Client
```py
#!/usr/bin/env python3
import rospy
from rospy_tutorials.srv import AddTwoInts

if __name__ == '__main__':
  rospy.init_node("client")
  rospy.wait_for_service("/add_two_ints")
  try:
    add_two_ints = rospy.ServiceProxy("/add_two_ints", AddTwoInts)
    response = add_two_ints(2,6)
    rospy.loginfo("Client sum (2+6) is :" +str(response.sum))
  except rospy.ServiceException as e:
    rospy.logwarn("Service failed:" +str(e))
```

### Code 2 - Server
```py
#!/usr/bin/env python3
import rospy
from service_pkg.srv import IsPalindrome

def check(req):
  txt = req.text
  isTrue = True
  for i in range(len(txt)):if(txt[i] != txt[len(txt) -1 -i]):
    isTrue = False
    break
  return isTrue

if __name__ == '__main__':
  rospy.init_node("server")
  rospy.loginfo("Palindrome Check Server Created")
  service = rospy.Service("/check_palindrome", IsPalindrome, check)
  rospy.loginfo("Service server has been started")
  rospy.spin()
```

### Code 2 - Client
```py
#!/usr/bin/env python3
import rospy
from service_pkg.srv import IsPalindrome

if __name__ == '__main__':
  rospy.init_node("client")
  rospy.wait_for_service("/check_palindrome")
  try:
    is_palindrome = rospy.ServiceProxy("/check_palindrome", IsPalindrome)
    response = is_palindrome("Chandramauli")
    rospy.loginfo("Text: " + str(response.output))
  except rospy.ServiceException as e:
    rospy.logwarn("Service failed:" + str(e))
```

### Code 2 - IsPalindrome.srv
```srv
string text
---
bool output
```

### Code 2 - CmakeList.txt
```cmake
find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  std_msgs
)
add_service_files(
  FILES
  IsPalindrome.srv
)
catkin_install_python(PROGRAMS
  scripts/server.py scripts/client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

generate_messages(
  DEPENDENCIES
  std_msgs
)
```
### Code 2 - package.xml
```xml
<exec_depend>message_runtime</exec_depend>
<build_depend>message_generation</build_depend>
```

## Custom Messages in ROS

### Setup
```
1. Create a package - catkin_create_pkg my_robot_msgs roscpp rospy std_msgs
2. Remove include and src folder

<exec_depend>message_runtime</exec_depend>
<build_depend>message_generation</build_depend>

find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  std_msgs
)

add_message_files(
  FILES
  HardwareInfo.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES custom_msgs_pkg
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs
#  DEPENDS system_lib
)

4. Create msg directory in package folder
5. Put HardwareInfo.msg in msg folder.

catkin_make

6. In some other package

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  custom_msgs_pkg
)

<depend>custom_msgs_pkg</depend> - use only if error comes

```

## Code 1 - HardwareInfo.msg
```
int64 temp
bool isMotorUp
string debugMsg
```

## Code 1 - Publisher
```py
#!/usr/bin/env python3
import rospy
from custom_msgs_pkg.msg import HardwareInfo

if __name__ == '__main__':
  rospy.init_node('pub')
  pub = rospy.Publisher('/motors/hardwareinfo', HardwareInfo, queue_size=10)
  rate = rospy.Rate(5)
  while not rospy.is_shutdown():
    msg = HardwareInfo()
    msg.temp = 45
    msg.isMotorUp = True
    msg.debugMsg = 'No Error'
    pub.publish(msg)
    rate.sleep()
```

## Code 1 - Subscriber
```py
#!/usr/bin/env python3
import rospy
from custom_msgs_pkg.msg import HardwareInfo

def print_info(info):
  print('temp:', info.temp)
  print('isMotorUp:', info.isMotorUp)
  print('debugMsg:', info.debugMsg)
  print('----------------------------')

if __name__ == '__main__':
  rospy.init_node('sub')
  sub = rospy.Subscriber('/motors/hardwareinfo', HardwareInfo, print_info)
  rospy.spin()
```

## URDF and SLAM and RVIZ

### Steps
```
1. Copy the slam_ws folder and delete the build and devel folder
2. Navigate inside slam_ws and do a catkin_make and add to source
3. Comment all inertia, collision tags and all gazebo tags
4. roslaunch explorer_bot rviz_explorer_bot.launch
5. Open another terminal and type rosrun rviz rviz if needed
6. Change fixed frame to base_link in the application
7. Add robot model in the application
```

### URDF
```urdf
<?xml version="1.0"?>
<robot name="custom_bot">

    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.6 0.3 0.1"/>
            </geometry>
            <material name="red">
                <color rgba="1 0.0 0.0 1"/>
            </material>
        </visual>
    </link>

    <link name="front_caster_of_wheel">
        <visual>
            <geometry>
                <box size="0.1 0.1 0.1"/>
            </geometry>
            <material name="green">
                <color rgba="0.0 0.1 0.0 1"/>   
            </material>
        </visual>
    </link>
    
    <joint name="front_caster_of_wheel_joint" type="continuous">
       <axis xyz="0.0 0.0 1"/> 
       <parent link="base_link"/>
       <child link="front_caster_of_wheel"/>
       <origin xyz="0.3 0.0 0.0" rpy="0.0 0.0 0.0"/>
    </joint>

    <link name="front_wheel">
        <visual>
            <geometry>
                <cylinder radius="0.035" length="0.05"/>
            </geometry>
            <material name="black">
            </material>
        </visual>
    </link>

    <joint name="front_wheel_joint" type="continuous">
        <axis xyz="0.0 0.0 1"/>
        <parent link="front_caster_of_wheel"/>
        <child link="front_wheel"/>
        <origin xyz="0.05 0.0 -0.05" rpy="-1.5708 0.0 0.0"/>
    </joint>

    <link name="right_wheel">
        <visual>
            <geometry>
                <cylinder radius="0.035" length="0.05"/>
            </geometry>
            <material name="black">
                <color rgba="0.0 0.0 0.0 1"/>
            </material>
        </visual>
    </link>

    <joint name="right_wheel_joint" type="continuous">
        <axis xyz="0.0 0.0 1"/>
        <parent link="base_link"/>
        <child link="right_wheel"/>
        <origin xyz="-0.2825 -0.125 -0.05" rpy="-1.5708 0.0 0.0"/>
    </joint>
    
    <link name="left_wheel">
        <visual>
            <geometry>
                <cylinder radius="0.035" length="0.05"/>
            </geometry>
            <material name="black">
                <color rgba="0.0 0.0 0.0 1"/>
            </material>
        </visual>
    </link>

    <joint name="left_wheel_joint" type="continuous">
        <axis xyz="0.0 0.0 1"/>
        <parent link="base_link"/>
        <child link="left_wheel"/>
        <origin xyz="-0.2825 0.125 -0.05" rpy="-1.5708 0.0 0.0"/>
    </joint>

    <link name="laser_scanner">
        <visual>
            <geometry>
                <box size="0.1 0.1 0.1"/>
            </geometry>
        </visual>
    </link>

    <joint name="laser_scanner_joint" type="fixed">
        <axis xyz="0.0 1 0.0"/>
        <parent link="base_link"/>
        <child link="laser_scanner"/>
        <origin xyz="0.0 0.0 0.08" rpy="0.0 0.0 0.0"/>
    </joint>

</robot> 
```
