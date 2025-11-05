import message_filters
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import CameraInfo, CompressedImage

import rerun as rr
from cv_bridge import CvBridge
# import cv2


class ImageLogger(Node):
    def __init__(self):
        super().__init__("image_logger")
        self.cv_bridge = CvBridge()
        self._spawn_rerun()

        image_sub = message_filters.Subscriber(
            self, CompressedImage, "/image_rect/compressed"
        )

        info_sub = message_filters.Subscriber(self, CameraInfo, "/camera_info")

        # synchronize camera info and image
        synchronized = message_filters.ApproximateTimeSynchronizer(
            [image_sub, info_sub], queue_size=10, slop=0.2
        )
        synchronized.registerCallback(self.image_callback)

    def _spawn_rerun(self):
        rr.init("test_subscriber", spawn=True)

    def image_callback(self, image: CompressedImage, info: CameraInfo):
        cv_image = self.cv_bridge.compressed_imgmsg_to_cv2(
            image, desired_encoding="rgb8"
        )

        rr.log("/image", rr.Image(cv_image))


def main():
    try:
        rclpy.init(args=None)
        node = ImageLogger()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
