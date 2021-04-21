import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import designlib as des
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import stepper

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x60)
pca.frequency = 1600
powerChannel = [0]
stepChannel_1 = [1]
stepChannel_2 = [2]
pca.channels[powerChannel] = 0xFFFF
stepperMotor  = stepper.StepperMotor(pca.channel[stepChannel_1],pca.channel[stepChannel_2])

def X_Stepper(msg):
    step = des.Conv_Steps_XY(msg)
    if step > 0:
        stepMain = step.floor()
        stepMicro = ((((stepMain - step)*100)/2)).floor() 
        for i in range(step):
            stepperMotor.onestep()
            time.sleep(0.01)
        stepperMotor.onestep(microsteps = stepMicro)
    if step < 0:
        step = step * -1
        stepMain = step.floor()
        stepMicro = ((((stepMain - step)*100)/2)).floor() 
        for i in range(step):
            stepperMotor.onestep(direction = stepper.BACKWARD)
            time.sleep(0.01)
        stepperMotor.onestep(direction = stepper.BACKWARD, microsteps = stepMicro)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('R_Subscriber')
        self.subscription = self.create_subscription(
            String,
            'R_Code',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        self.publisher = self.create_publisher(String,'Check',10)
 
    def check_callback(self):
        msg = String()
        msg.data = 'R'
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)   

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        x_Stepper(msg)
        self.check_callback()
        

def main(args=None):
    rclpy.init(args=args)
    
    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    #checkpub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
