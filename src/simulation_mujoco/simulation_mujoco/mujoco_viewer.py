import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import mujoco
import mujoco.viewer
from ament_index_python.packages import get_package_share_directory

class JointStateSubscriber(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.JointStateCallback,
            10
        )
        model_path = get_package_share_directory('so_arm101_description')
        self.model = mujoco.MjModel.from_xml_path(model_path + '/mjcf/scene.xml')
        self.data = mujoco.MjData(self.model)
        self.handle_mujoco = mujoco.viewer.launch_passive(self.model, self.data)

        self.timer = self.create_timer(
            0.01,  # 100ms周期
            self.TimerCallback
        )

    def TimerCallback(self):
        if not hasattr(self, "positions"):
            return
        self.data.qpos[:6] = self.positions
        mujoco.mj_step(self.model, self.data)
        self.handle_mujoco.sync()

    # 处理接收到的关机位置信息
    def JointStateCallback(self, msg: JointState):
        JOINT_ORDER = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
        name_to_pos = dict(zip(msg.name, msg.position))
        self.positions = [name_to_pos[name] for name in JOINT_ORDER]

    #节点结束，清理mujoco窗口
    def cleanup(self):
        self.handle_mujoco.close()

def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber("mujoco_simulation")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("CTRL+C received")
    finally:
        node.cleanup()
        rclpy.shutdown()

if __name__ == "__main__":
    main()