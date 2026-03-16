#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from my_robot_interfaces.action import MoveTurtle


class MoveTurtleClient(Node):

    def __init__(self):

        super().__init__("move_turtle_client")

        self.client = ActionClient(self, MoveTurtle, "/turtle1/move_turtle")

    def send_goal(self, x, y):

        goal = MoveTurtle.Goal()
        goal.x = x
        goal.y = y

        self.client.wait_for_server()

        self.future = self.client.send_goal_async(
            goal, feedback_callback=self.feedback_callback
        )

        self.future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return

        self.get_logger().info("Goal accepted")

        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):

        result = future.result().result
        self.get_logger().info(f"Result: {result.success}")

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(f"Remaining distance: {feedback.distance_remaining:.2f}")


def main():

    rclpy.init()

    node = MoveTurtleClient()

    node.send_goal(8.0, 8.0)

    rclpy.spin(node)


if __name__ == "__main__":
    main()
