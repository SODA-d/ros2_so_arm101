import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from hardware import FeetechMotor as FM
import math

class JointStateSubscriber(Node):
    def __init__(self,node_name):
        super().__init__(node_name)

        self.motor = FM.FeetechMotor(1,"/dev/ttyACM0")
        self.motor.connect()
        self.arm_controller_pub = self.create_publisher(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            10
        )
        self.hand_controller_pub = self.create_publisher(
            JointTrajectory,
            "/hand_controller/joint_trajectory",
            10
        )
        self.timer = self.create_timer(
            0.01, 
            self.send_command
        )
        self.positions_rad = [0,0,0,0,0,0]
    def TimerCallback(self):
        for i in range(1, 7):
            self.motor.setMotorId(i)
            self.positions_rad[i-1] = math.radians(self.motor.getPosition())

    def send_command(self):
        for i in range(1, 7):
            self.motor.setMotorId(i)
            self.positions_rad[i-1] = math.radians(self.motor.getPosition())

        arm_msg = JointTrajectory()
        hand_msg = JointTrajectory()
        print(self.positions_rad)
        arm_msg.joint_names = [
            "shoulder_pan",
            "shoulder_lift",
            "elbow_flex",
            "wrist_flex",
            "wrist_roll"
        ]
        hand_msg.joint_names = ["gripper"]

        arm_point = JointTrajectoryPoint()
        hand_point = JointTrajectoryPoint()

        arm_point.positions = self.positions_rad[:5]
        arm_point.time_from_start.sec = 2
        hand_point.positions = self.positions_rad[-1:]
        hand_point.time_from_start.sec = 2


        arm_msg.points.append(arm_point)
        self.arm_controller_pub.publish(arm_msg)
        hand_msg.points.append(hand_point)
        self.hand_controller_pub.publish(hand_msg)


    def cleanup(self):
        self.motor.disconnect()

def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber("real2sim_controller")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("CTRL+C received")
    finally:
        node.cleanup()
        rclpy.shutdown()

if __name__ == "__main__":
    main()