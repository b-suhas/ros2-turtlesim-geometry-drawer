#!/usr/bin/env pyton3

# Importing necessary libraries and modules
from geometry_msgs import msg
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
import math
import time

# Defining the GeometryDrawerNode 
class GeometryDrawerNode(Node):

    # Initializing the node and setting up the publisher and timer
    def __init__(self, shape):
        
        super().__init__('geometry_drawer')
        # Publisher
        self.cmd_vel_pub_ = self.create_publisher(Twist ,"/turtle1/cmd_vel",10)

        # Selected shape
        self.shape = shape

        # Common variables
        self.timer_ = None
        self.step = 0
        self.phase = "move"
        self.counter = 0

        # Spiral variables
        self.linear_speed = 0.0
        self.angular_speed = 1.15
        self.linear_increment = 0.01
        self.max_linear_speed = 6.0

        # Infinity / heart counters
        self.t = 0.0

        # Shape selection
        if self.shape == "circle":
            self.timer_ = self.create_timer(0.1, self.draw_circle)

        elif self.shape == "square":
            self.timer_ = self.create_timer(0.1, self.draw_square)

        elif self.shape == "triangle":
            self.timer_ = self.create_timer(0.1, self.draw_triangle)

        elif self.shape == "spiral":
            self.timer_ = self.create_timer(0.1, self.draw_spiral)

        elif self.shape == "star":
            self.timer_ = self.create_timer(0.1, self.draw_star)

        elif self.shape == "infinity":
            self.timer_ = self.create_timer(0.1, self.draw_infinity)

            

    # Method to draw a circle
    def draw_circle(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0

        self.cmd_vel_pub_.publish(msg)
        
        self.t += 0.1
        if self.t > 6.3:
            self.stop_turtle()

    # Method to draw a spiral
    def draw_spiral(self):
        msg = Twist()

        msg.linear.x = self.linear_speed
        msg.angular.z = self.angular_speed

        self.cmd_vel_pub_.publish(msg)

        self.linear_speed += self.linear_increment

        if self.linear_speed > self.max_linear_speed:
            self.stop_turtle()

    
    # Method to draw a square
    def draw_square(self):
        self.draw_polygon(sides=4,
        move_steps=15,          
        turn_steps=10,
        turn_angle=math.pi / 2)

    # Method to draw a triangle
    def draw_triangle(self):
        self.draw_polygon(sides=3,
        move_steps=18,
        turn_steps=12,
        turn_angle=(2 * math.pi / 3))

    # Method to draw a star
    def draw_star(self):
        self.draw_polygon(sides=5,
        move_steps=12,
        turn_steps=10,
        turn_angle=(4 * math.pi / 5)
        )
    
    # Common method to draw polygons (square, triangle, star)
    def draw_polygon(self, sides, move_steps, turn_steps, turn_angle):

        if self.step >= sides:
            self.stop_turtle()
            return

        msg = Twist()

        # Move straight
        if self.phase == "move":
            msg.linear.x = 1.8   # slower for accuracy
            self.counter += 1

            if self.counter >= move_steps:
                self.phase = "turn"
                self.counter = 0

        # Rotate gradually
        elif self.phase == "turn":
            msg.angular.z = turn_angle / (turn_steps * 0.1)
            self.counter += 1

            if self.counter >= turn_steps:
                self.phase = "move"
                self.counter = 0
                self.step += 1

        self.cmd_vel_pub_.publish(msg)


    # Method to draw an infinity symbol
    def draw_infinity(self):
        msg = Twist()

        # First loop
        if self.t < 6.3:
            msg.linear.x = 1.5
            msg.angular.z = 1.5

        # Second loop (reverse direction)
        elif self.t < 12.6:
            msg.linear.x = 1.5
            msg.angular.z = -1.5

        else:
            self.stop_turtle()
            return

        self.cmd_vel_pub_.publish(msg)

        self.t += 0.1
    
    
    # Method to stop the turtle
    def stop_turtle(self):
        self.cmd_vel_pub_.publish(Twist())
        self.get_logger().info(
            f"{self.shape.capitalize()} completed!"
        )

        if self.timer_:
            self.timer_.cancel()

# Clear screen
def clear_turtle():
    temp_node = rclpy.create_node("clear_screen_client")

    clear_client = temp_node.create_client(
        Empty,
        "/clear"
    )

    while not clear_client.wait_for_service(timeout_sec=1.0):
        pass

    request = Empty.Request()
    future = clear_client.call_async(request)

    rclpy.spin_until_future_complete(
        temp_node,
        future
    )

    temp_node.destroy_node()
        
            
# Main function to initialize the ROS2 node and start spinning
def main(args=None):
    # Initializing ROS2
    rclpy.init(args=args)

    while True:

        # Clear previous drawing
        clear_turtle()
        
        print("\nAvailable shapes:")
        print("circle")
        print("square")
        print("triangle")
        print("spiral")
        print("star")
        print("infinity")
        print("quit")

        shape = input(
            "\nEnter shape: "
        ).lower()

        if shape == "quit":
            print("Exiting Geometry Drawer...")
            break
        
        valid_shapes = [
            "circle",
            "square",
            "triangle",
            "spiral",
            "star",
            "infinity"
        ]

        if shape not in valid_shapes:
            print("Invalid shape!")
            continue

        # Creating an instance of the GeometryDrawerNode        
        node = GeometryDrawerNode(shape)

        # Keep spinning only until shape completes
        while rclpy.ok() and not node.timer_.is_canceled():
            rclpy.spin_once(node)

        # Clean up after shape finishes
        node.destroy_node()

        # Small pause before menu returns
        time.sleep(1)
        
    # Shutdown ROS2 when done
    rclpy.shutdown()

# Entry point of the program
if __name__ == '__main__':
    main()
    
