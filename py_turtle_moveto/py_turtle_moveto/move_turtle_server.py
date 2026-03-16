#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from my_robot_interfaces.action import MoveTurtle

import math


class MoveTurtleServer(Node):

    def __init__(self):

        super().__init__("move_turtle_server")

        self.pose = None

        self.pose_sub = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )

        self.cmd_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.action_server = ActionServer(
            self, MoveTurtle, "/turtle1/move_turtle", self.execute_callback
        )

    def pose_callback(self, msg):
        self.pose = msg

    def execute_callback(self, goal_handle):

        target_x = goal_handle.request.x
        target_y = goal_handle.request.y

        self.get_logger().info(f"Move to ({target_x}, {target_y})")

        feedback = MoveTurtle.Feedback()

        twist = Twist()

        while rclpy.ok():

            if self.pose is None:
                continue

            dx = target_x - self.pose.x
            dy = target_y - self.pose.y

            distance = math.sqrt(dx**2 + dy**2)

            feedback.distance_remaining = distance
            goal_handle.publish_feedback(feedback)

            if distance < 0.1:
                break

            angle = math.atan2(dy, dx)
            angle_error = angle - self.pose.theta

            twist.linear.x = 1.5 * distance
            twist.angular.z = 4.0 * angle_error

            self.cmd_pub.publish(twist)

        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

        goal_handle.succeed()

        result = MoveTurtle.Result()
        result.success = True

        return result


def main():

    rclpy.init()

    node = MoveTurtleServer()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
