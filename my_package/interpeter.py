import pandas
import math
import rclpy
import time
from rclpy.node import Node

from std_msgs.msg import String

xCheck = False
yCheck = True
zCheck = True
lCheck = True
rCheck = True
Gcode = open("probegcode.gcode", "r+")

def send(Gcode,node):
    i = Gcode.readline()
    if i[4] == 'X':
        i = i.strip("G01 ")
        i = i.strip("\n")
        X,Y = i.split(" ")
        X = X.strip("X")
        Y = Y.strip("Y")
        node.callback_X(X)
        node.callback_Y(Y)
    elif i[4] == 'Z':
        trash, Z = i.split('Z')
        node.callback_Z(Z)
    elif i[4] == 'R':
        i = i.strip("G01 ")
        i = i.strip("\n")
        R = i.strip("R")
        node.callback_R(R)
    elif i[4] == 'L':
        i = i.strip("G01 ")
        i = i.strip("\n")
        L = i.strip("L")
        node.callback_L(L)


class GcodePublisher(Node):

    def __init__(self):
        super().__init__('Gcode_publisher')
        self.publisher_X = self.create_publisher(String, 'X_Code', 10)
        self.publisher_Y = self.create_publisher(String, 'Y_Code', 10)
        self.publisher_Z = self.create_publisher(String, 'Z_Code', 10)
        self.publisher_R = self.create_publisher(String, 'R_Code', 10)
        self.publisher_L = self.create_publisher(String, 'L_Code', 10)
        self.subscription = self.create_subscription(String,'Check',self.listener_callback, 10)

    def listener_callback(self,msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        if msg.data == 'X':
            send(Gcode,self)
        elif msg.data == 'Y':
            send(Gcode,self)
        elif msg.data == 'Z':
            send(Gcode,self)
        elif msg.data == 'R':
            send(Gcode,self)
        elif msg.data == 'L':
            send(Gcode,self)

    def callback_X(self,tempstring):
        msg = String()
        msg.data = tempstring
        self.publisher_X.publish(msg)
        self.get_logger().info('Publishing - X: "%s"' % msg.data)

    def callback_Y(self,tempstring):
        msg = String()
        msg.data = tempstring
        self.publisher_Y.publish(msg)
        self.get_logger().info('Publishing - Y: "%s"' % msg.data)

    def callback_Z(self,tempstring):
        msg = String()
        msg.data = tempstring
        self.publisher_Z.publish(msg)
        self.get_logger().info('Publishing - Z: "%s"' % msg.data)

    def callback_R(self,tempstring):
        msg = String()
        msg.data = tempstring
        self.publisher_R.publish(msg)
        self.get_logger().info('Publishing - R: "%s"' % msg.data)

    def callback_L(self,tempstring):
        msg = String()
        msg.data = tempstring
        self.publisher_L.publish(msg)
        self.get_logger().info('Publishing - L: "%s"' % msg.data)

def read(filename):
    Gcode = []
    for i in filename:
        i = i.strip("\n")
        Gcode.append(i)
    return Gcode

def main(args=None):
    rclpy.init(args=args)
    #file = open("probegcode.gcode", "r+")
    #Gcode = read(file)
    Gcode_Publisher = GcodePublisher()
    #Checker = CheckSubscriber()
    send(Gcode, Gcode_Publisher)
    rclpy.spin(Gcode_Publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Gcode_Publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


