from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    package_ = "udemy_challenge_services"

    client_server_node = Node(
        package=package_,
        executable="serviceClient.py",
        name="service_client",
        parameters=[
            {"degrees": 20}
        ]
    )

    service_server_node = Node(
        package=package_,
        executable="serviceServer.py",
        name="service_service",
        parameters=[
        ]
    )

    ld.add_action(client_server_node)
    ld.add_action(service_server_node)


    return ld


