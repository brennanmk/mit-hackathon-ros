import rospy
from geometry_msgs.msg import Twist

from std_msg.msg import Float32

from math import pi

# This package is used to control the arm
from interbotix_xs_modules.locobot import InterbotixLocobotCreate3XS as InterbotixLocobotXS

class Teleop:
    def __init__(self):
        rospy.init_node('teleop')

        self.rate = rospy.Rate(60)

        self.lin_x_multiplier = 0.5 # 0.5 m/s
        self.ang_z_multiplier = pi # pi rad/s

        self.dead_zone = 5 # 5 degree deadzone
        self.max = 35 

        self.normalize = 45

        self.cmd_vel_pub = rospy.Publisher('/mobile_base/cmd_vel', Twist, queue_size=3)
        rospy.Subscriber('/joy', Float32, self.control_base)

    def control_base(self, x, yaw):
        '''Function to control base, takes x linear and yaw as inputs. 
            Base moves as a velocity in m/s for the duration specified, 
            there is a similair function in https://github.com/Interbotix/interbotix_ros_toolboxes/blob/main/interbotix_xs_toolbox/interbotix_xs_modules/src/interbotix_xs_modules/locobot.py, 
            this function was written to gain a better understanding of how the geometry/Twist message type works.'''

        msg = Twist()
        msg.angular.y = 0.0
        msg.angular.y = 0.0
        if self.dead_zone < yaw  < self.max:
            msg.angular.z = (yaw / self.normalize) * self.ang_z_multiplier
        elif self.dead_zone >= yaw:
            msg.angular.z = 0
        else:
            msg.angular.z = 1
        
        if self.dead_zone < x <= self.max:
            msg.linear.x = (x / self.normalize) * self.lin_x_multiplier
        elif self.dead_zone >= x:
            msg.linear.x = 0
        else:
            msg.linear.x = 1
    
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        self.cmd_vel_pub.publish(msg)
        self.rate.sleep()
            