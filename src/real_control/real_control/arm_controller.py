import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from hardware import FeetechMotor as FM
import math

class JointStateSubscriber(Node):
    def __init__(self,node_name):
        super().__init__(node_name)

        self.motor = FM.FeetechMotor(1,"/dev/ttyACM0")
        self.motor.connect()
        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.JointStateCallback,
            10
        )
        self.timer = self.create_timer(
            0.01, 
            self.send_command
        )

    def send_command(self):
        if not hasattr(self, "positions_deg"):
            return
        for i in range(1, 7):
            self.motor.setMotorId(i)
            self.motor.setSpeed(2000)  # 设置目标速度为1000步/秒
            self.motor.printFlag(False)  # 打开打印
            if i == 1 or i == 2:
                self.motor.setPID(16, 16, 0)
            else:   
                self.motor.setPID(32, 32, 0)  # 设置PID参数
            self.motor.setPosition(self.positions_deg[i - 1])

    def JointStateCallback(self, msg: JointState):
        JOINT_ORDER = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
        name_to_pos = dict(zip(msg.name, msg.position))
        self.positions_deg = [math.degrees(name_to_pos[name]) for name in JOINT_ORDER]


    def cleanup(self):
        for i in range(1,7):
            self.motor.setMotorId(i)
            self.motor.setTorqueEnable(0)
        self.motor.disconnect()

def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber("arm_controller")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("CTRL+C received")
    finally:
        node.cleanup()
        rclpy.shutdown()

if __name__ == "__main__":
    main()