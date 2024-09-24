import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from hewo_bot_module_display.display.main_window import MainWindow

class MainWindowNode(Node, MainWindow):
    def __init__(self):
        Node.__init__(self, 'main_window_node')
        MainWindow.__init__(self)
        self.subscription = self.create_subscription(
            String,
            'window_state',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Recibido: "{msg.data}"')


    def run_node(self):
        while rclpy.ok():
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            rclpy.spin_once(self, timeout_sec=0.01)

if __name__ == '__main__':
    rclpy.init()
    node = MainWindowNode()
    node.run_node()
