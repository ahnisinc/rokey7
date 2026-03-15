#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_robot_interfaces.action import MoveTurtle

class MoveTurtleActionClient(Node):

    def __init__(self):
        super().__init__('move_turtle_action_client')
        self._action_client = ActionClient(self, MoveTurtle, '/turtle1/move_turtle')

    def send_goal(self, x, y):
        goal_msg = MoveTurtle.Goal()
        goal_msg.x = x
        goal_msg.y = y

        self._action_client.wait_for_server()
        self.get_logger().info(f'Sending goal: ({x}, {y})')
        return self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Distance remaining: {feedback.distance_remaining:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtleActionClient()

    future = node.send_goal(5.0, 5.0)  # 원하는 좌표로 수정
    rclpy.spin_until_future_complete(node, future)
    result = future.result().result
    node.get_logger().info(f'Goal result: success={result.success}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
