#!/usr/bin/python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from my_robot_interfaces.srv import SetDegree
from functools import partial

class Client(Node):
    def __init__(self):
        super().__init__("client_node")

        self.declare_parameter("degrees",10)
        self.parameter_ = self.get_parameter("degrees").get_parameter_value().integer_value

        self.get_logger().info("Client about to ask: " + str(self.parameter_))

        self.service_call()

        
    def service_call(self):

        self.client_ = self.create_client(SetDegree,"/set_degree")

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server...")

        self.request_ = SetDegree.Request()

        self.request_.degree = self.parameter_

        future = self.client_.call_async(self.request_)
        
        future.add_done_callback(partial(self.on_service_response,data=self.request_.degree))

    def on_service_response(self,future,data):

        try:
            response = future.result()

            self.get_logger().info("Request: " + str(data) + " - Response: Todo OK")

            image = CvBridge().imgmsg_to_cv2(response.response_attr_name)

            cv2.imshow("Display WIndow name",image)
            cv2.waitKey(0)
            cv2.destroyAllWindows(0)

        except Exception as e:
            self.get_logger().error("Something went wrong: %r" % (e,))



def main():

    rclpy.init()
    my_server = Client()
    
    try:
        rclpy.spin(my_server)
    except KeyboardInterrupt:
        my_server.destroy_node()
        rclpy.shutdown()
    

if __name__ == "__main__":
    main() 