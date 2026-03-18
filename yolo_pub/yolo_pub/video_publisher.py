import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class VideoPublisher(Node):

    def __init__(self):
        super().__init__("video_publisher")
        self.publisher = self.create_publisher(Image, "video_frames", 10)

        self.cap = cv2.VideoCapture("video.mp4")

        if not self.cap.isOpened():
            self.get_logger().error("Failed to open video file")

        self.bridge = CvBridge()

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30.0

        self.timer = self.create_timer(1.0 / fps, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()

        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "camera"

            self.publisher.publish(msg)
        else:
            self.get_logger().info("Video finished")
            self.cap.release()
            raise SystemExit  # 가장 깔끔한 종료


def main(args=None):
    rclpy.init(args=args)
    node = VideoPublisher()

    try:
        rclpy.spin(node)
    except SystemExit:
        pass

    node.destroy_node()
    rclpy.shutdown()
