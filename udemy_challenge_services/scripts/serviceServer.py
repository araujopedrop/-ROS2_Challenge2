#!/usr/bin/python3

import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from my_robot_interfaces.srv import SetDegree

class Server(Node):
    def __init__(self):
        super().__init__("server_node")

        self.service_ = self.create_service(SetDegree,"/set_degree",self.callback_service)
        
        #Here use your own path
        self.file_location_ = "/home/.../img/"
        self.full_file_location_ = ""
        self.get_logger().info("Service iniciado")

        image_ = CvBridge()


    def callback_service(self,request,response):
        try:
            
            self.get_logger().info("Servicio llamado")

            val = request.degree

            self.full_file_location_ = self.file_location_ + str(val) + ".jpg"

            image = cv2.imread(self.full_file_location_)

            #Convert ros image msg to a opencv data type
            image_msg = CvBridge().cv2_to_imgmsg(image)

            response.response_attr_name = image_msg 
            return response

        except:
            self.get_logger().error("Servicio en falla")
            response.response_attr_name = image_msg

            return response
    


def main():

    rclpy.init()
    my_server = Server()
    
    try:
        rclpy.spin(my_server)
    except KeyboardInterrupt:
        my_server.destroy_node()
        rclpy.shutdown()
    

if __name__ == "__main__":
    main() 
