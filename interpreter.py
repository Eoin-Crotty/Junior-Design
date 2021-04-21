import pandas
import math
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class GcodePublisher(Node):

    def __init__(self):
        super().__init__('Gcode_publisher')
        self.publisher_X = self.create_publisher(String, 'X_Code', 10)
        self.publisher_Y = self.create_publisher(String, 'Y_Code', 10)
        self.publisher_Z = self.create_publisher(String, 'Z_Code', 10)
        self.publisher_R = self.create_publisher(String, 'R_Code', 10)
        self.publisher_L = self.create_publisher(String, 'L_Code', 10)

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

def send(Gcode,node):
    for i in Gcode:
        if i[4] == 'X':
            i = i.strip("G01 ")
            i = i.strip("\n")
            X,Y = i.split(" ")
            X = X.strip("X")
            Y = Y.strip("Y")
            node.callback_X(X)
            node.Callback_Y(Y)
        if i[4] == 'Z':
            i = i.strip("G01 ")
            i = i.strip("\n")
            Z = i.strip("Z")
            node.callback_Z(Z)
        if i[4] == 'R':
            i = i.strip("G01 ")
            i = i.strip("\n")
            Z = i.strip("R")
            node.callback_R(R)
        if i[4] == 'L':
            i = i.strip("G01 ")
            i = i.strip("\n")
            L = i.strip("L")
            node.callback_L(L)

def main(args=None):
    rclpy.init(args=args)
    file = open("probegcode.gcode", "r+")
    Gcode = read(file)
    Gcode_Publisher = GcodePublisher()
    send(Gcode, Gcode_Publisher)
    rclpy.spin(Gcode_Publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Gcode_Publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


