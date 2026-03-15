#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from my_robot_interfaces.action import MoveTurtle  # 생성한 액션 인터페이스 import

class MoveTurtleActionServer(Node):

    def __init__(self):
        super().__init__('move_turtle_action_server')
        self._action_server = ActionServer(
            self,
            MoveTurtle,
            '/turtle1/move_turtle',
            self.execute_callback)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.current_pose = Pose()

    def pose_callback(self, msg):
        self.current_pose = msg

    async def execute_callback(self, goal_handle):
        self.get_logger().info(f'Goal received: x={goal_handle.request.x}, y={goal_handle.request.y}')
        feedback_msg = MoveTurtle.Feedback()
        goal_x = goal_handle.request.x
        goal_y = goal_handle.request.y

        rate = self.create_rate(10)
        success = False

        while rclpy.ok():
            dx = goal_x - self.current_pose.x
            dy = goal_y - self.current_pose.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 0.1:
                success = True
                break

            # 방향 제어
            angle_to_goal = math.atan2(dy, dx)
            twist = Twist()
            twist.linear.x = 1.5 * distance
            twist.angular.z = 4.0 * (angle_to_goal - self.current_pose.theta)
            self.cmd_pub.publish(twist)

            feedback_msg.distance_remaining = distance
            goal_handle.publish_feedback(feedback_msg)
            await rate.sleep()

        twist = Twist()
        self.cmd_pub.publish(twist)

        goal_handle.succeed()
        result = MoveTurtle.Result()
        result.success = success
        self.get_logger().info('Goal completed!')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtleActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
