#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from my_robot_interfaces.action import MoveTurtle

import math
import time


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
            rclpy.spin_once(self, timeout_sec=0.1)

            if self.pose is None:
                continue

            # 거리 계산
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.sqrt(dx**2 + dy**2)

            # 피드백 전송
            feedback.distance_remaining = distance
            goal_handle.publish_feedback(feedback)

            # 목표 위치 도착하면 종료
            if distance < 0.1:
                break

            # 목표 각도 계산
            angle_to_target = math.atan2(dy, dx)
            angle_error = angle_to_target - self.pose.theta

            # 각도를 -pi ~ pi 범위로 제한
            angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

            # 속도 제어
            K_linear = 1.0
            K_angular = 4.0

            twist.linear.x = K_linear * distance if abs(angle_error) < 0.1 else 0.0
            twist.angular.z = K_angular * angle_error

            self.cmd_pub.publish(twist)

            time.sleep(0.05)

        # 정지
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