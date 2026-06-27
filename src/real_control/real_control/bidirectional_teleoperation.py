import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from hardware import FeetechMotor as FM
import math
import threading
from enum import Enum

class ControlMode(Enum):
    SIM2REAL = 0
    REAL2SIM = 1

class BiTeleoperation(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.motor = FM.FeetechMotor(1,"/dev/ttyACM0")
        self.motor.connect()
        self.positions_rad = [0.0,0.0,0.0,0.0,0.0,0.0]
        
        self.mode = ControlMode.SIM2REAL
        self.mode_lock = threading.Lock()
        self.motor_lock = threading.Lock()

        self.keyboard_thread = threading.Thread(
            target=self.keyboard_loop,
            daemon=True
        )
        self.keyboard_thread.start()
        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.JointStateCallback,
            10
        )
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
            self.TimerCallback
        )

    def TimerCallback(self):
        with self.mode_lock:
            mode  = self.mode

        if mode == ControlMode.SIM2REAL:
            self.sim2real()
        else:
            self.real2sim()

    
    def sim2real(self):
        if not hasattr(self, "positions_deg"):
            return
        with self.motor_lock:
            for i in range(1, 7):
                self.motor.setMotorId(i)
                self.motor.setSpeed(2000)  
                self.motor.printFlag(False) 
                if i == 1 or i == 2:
                    self.motor.setPID(16, 16, 0)
                else:   
                    self.motor.setPID(32, 32, 0)  
                self.motor.setPosition(self.positions_deg[i - 1])

    def real2sim(self):
        with self.motor_lock:
            for i in range(1,7):
                    self.motor.setMotorId(i)
                    self.motor.setTorqueEnable(0)
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


    def JointStateCallback(self, msg: JointState):
        JOINT_ORDER = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
        name_to_pos = dict(zip(msg.name, msg.position))
        self.positions_deg = [math.degrees(name_to_pos[name]) for name in JOINT_ORDER]


    def keyboard_loop(self):

        while rclpy.ok():

            key = input()

            if key.lower() == 'q':

                with self.mode_lock:

                    if self.mode == ControlMode.SIM2REAL:
                        self.mode = ControlMode.REAL2SIM
                    else:
                        self.mode = ControlMode.SIM2REAL

                    print(f"Current mode: {self.mode}")


    def cleanup(self):
        for i in range(1,7):
            self.motor.setMotorId(i)
            self.motor.setTorqueEnable(0)
        self.motor.disconnect()

def main():
    rclpy.init()
    node = BiTeleoperation("BiTeleoperation")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("CTRL+C received")
    finally:
        node.cleanup()
        rclpy.shutdown()

if __name__ == "__main__":
    main()







