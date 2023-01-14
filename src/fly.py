# https://clover.coex.tech/en/simple_offboard.html

import rospy
from clover import srv
from std_srvs.srv import Trigger
from std_msgs.msg import Int32

class fly:
    def __init__(self):
        rospy.init_node('fly') 

        self.get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy('navigate', srv.Navigate)
        self.navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
        self.set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
        self.set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
        self.set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
        self.set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
        self.land = rospy.ServiceProxy('land', Trigger)

        rospy.Subscriber('/move',
                         Int32, self.linear_z) 

        rospy.Subscriber('/start_end',
                    Int32, self.start_end)

    def linear_z(self, data):
        tel = self.get_telemetry
        
        if data.data = 1:
            if   < 2 and data.data > 1:
                self.navigate(x=0, y=0, z=(data.data + 0.1), speed=0.5, frame_id='body')
        else:
            if data.data < 2 and data.data > 1:
                self.navigate(x=0, y=0, z=(data.data + 0.1), speed=0.5, frame_id='body')

    def start_end(self, data):
        if data.data == 0:
            self.land()
        else:
            self.navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)


if __name__ == '__main__':
    fly()