#  ROS2 Turtlesim Geometry Drawer

![ROS2](https://img.shields.io/badge/ROS2-Humble%20%7C%20Iron-blue?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

> A ROS2-powered Python node that commands the **Turtlesim** robot to draw geometric shapes — interactively, from the terminal. Supports six shapes: circle, square, triangle, spiral, star, and infinity loop.

---

##  About the Project

**ROS2 Turtlesim Geometry Drawer** is a hands-on ROS2 learning project that demonstrates how to publish velocity commands to a simulated robot (Turtlesim) to make it draw precise geometric shapes. The user selects a shape from an interactive terminal menu, and the ROS2 node takes over — publishing timed `Twist` messages to `/turtle1/cmd_vel` to trace the path.

Each shape run clears the canvas automatically using the `/clear` service before drawing begins, giving a clean slate every time.

This project is ideal for anyone learning ROS2 fundamentals such as publishers, services, timers, and node lifecycle management in a visual, satisfying way.

---

##  Features

- **6 drawable shapes** — circle, square, triangle, spiral, star, and infinity loop
- **Interactive terminal menu** — select a shape each run without restarting the node
- **Auto canvas clear** — calls the `/clear` service before every new drawing
- **Timer-based motion control** — uses ROS2 timers to drive smooth, step-based movement
- **Graceful stop** — cancels the timer and publishes a zero-velocity command when drawing is complete
- **Polygon abstraction** — square, triangle, and star all reuse a unified `draw_polygon()` helper
- **Clean shutdown** — handles node destruction and `rclpy` shutdown properly

---

##  Tech Stack

| Technology | Purpose |
|---|---|
| **ROS2 (Humble / Iron)** | Robot middleware framework |
| **Python 3.10+** | Primary programming language |
| **rclpy** | Python client library for ROS2 |
| **geometry_msgs/Twist** | Velocity command message type |
| **std_srvs/Empty** | ROS2 service type for `/clear` |
| **Turtlesim** | Built-in ROS2 simulator for visualizing turtle movement |

---

##  Concepts Used

- **ROS2 Publisher** — publishing `Twist` messages to `/turtle1/cmd_vel`
- **ROS2 Service Client** — calling the `/clear` service using `std_srvs/Empty`
- **ROS2 Timer** — periodic callbacks using `create_timer()` for step-by-step motion
- **Node Lifecycle** — creating, spinning, and destroying nodes cleanly
- **`spin_once()` vs `spin()`** — using `spin_once()` for fine-grained control in a loop
- **`spin_until_future_complete()`** — waiting for async service responses
- **Twist Message** — setting linear and angular velocity for 2D motion control
- **Parametric motion** — using time increments and phase-based state machines

---

##  Project Structure

```
ros2-turtlesim-geometry-drawer/
│
├── geometry_drawer/              # Main ROS2 Python package
│   ├── __init__.py
│   └── geometry_drawer_node.py   # Core node — all shape-drawing logic
│
├── resource/                     # ROS2 package resource marker
│   └── geometry_drawer
│
├── test/                         # Unit/linting tests
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
│
├── .gitignore
├── package.xml                   # ROS2 package metadata and dependencies
├── setup.cfg                     # Entry point and package config
├── setup.py                      # Python package setup
└── README.md
```

---

##  Prerequisites

Before running this project, ensure you have:

- **Ubuntu 22.04** (recommended) or compatible Linux distro
- **ROS2 Humble or Iron** installed — [Installation Guide](https://docs.ros.org/en/humble/Installation.html)
- **Turtlesim** package installed
- A properly sourced ROS2 workspace

---

##  Installation

### 1. Source your ROS2 installation

```bash
source /opt/ros/humble/setup.bash
```

### 2. Create or navigate to your ROS2 workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### 3. Clone the repository

```bash
git clone https://github.com/b-suhas/ros2-turtlesim-geometry-drawer.git
```

### 4. Navigate to the workspace root and build

```bash
cd ~/ros2_ws
colcon build --packages-select geometry_drawer
```

### 5. Source the workspace overlay

```bash
source install/setup.bash
```

---

##  How to Run

You will need **two terminal windows**.

### Terminal 1 — Launch Turtlesim

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

### Terminal 2 — Run the Geometry Drawer Node

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run geometry_drawer geometry_drawer
```

---

##  Usage Instructions

Once the node starts, you'll see an interactive menu in the terminal:

```
Available shapes:
circle
square
triangle
spiral
star
infinity
quit

Enter shape:
```

1. Type the name of any shape and press **Enter**
2. Watch the turtle draw the shape in the Turtlesim window
3. The canvas clears automatically before each new drawing
4. Type `quit` to exit the program

---

##  Available Shapes

| Shape | Motion Type | Description |
|---|---|---|
| `circle` | Constant linear + angular velocity | Draws a full circle using uniform `Twist` values |
| `square` | Phase-based (move → turn × 4) | Moves forward, turns 90°, repeats 4 times |
| `triangle` | Phase-based (move → turn × 3) | Moves forward, turns 120°, repeats 3 times |
| `star` | Phase-based (move → turn × 5) | Moves forward, turns 144°, repeats 5 times (5-pointed star) |
| `spiral` | Increasing linear speed | Gradually accelerates linear velocity while maintaining angular velocity |
| `infinity` | Split-phase circular arcs | Draws two opposing circular arcs to form a figure-8 / ∞ shape |

---

##  ROS2 Commands Reference

Useful commands for debugging and inspecting the node at runtime:

```bash
# List all active topics
ros2 topic list

# Echo velocity commands being published
ros2 topic echo /turtle1/cmd_vel

# Inspect the topic message type
ros2 topic info /turtle1/cmd_vel

# List available services
ros2 service list

# Manually call the clear service
ros2 service call /clear std_srvs/srv/Empty

# List running nodes
ros2 node list

# Inspect the geometry_drawer node
ros2 node info /geometry_drawer
```

---

##  Example Workflow

```
$ ros2 run geometry_drawer geometry_drawer

Available shapes:
circle
square
triangle
spiral
star
infinity
quit

Enter shape: circle
[INFO] [geometry_drawer]: Circle completed!

Available shapes:
...

Enter shape: spiral
[INFO] [geometry_drawer]: Spiral completed!

Enter shape: quit
Exiting Geometry Drawer...
```

---

##  Key Learning Outcomes

By building and studying this project, you will understand:

- How to structure a proper **ROS2 Python package** with `setup.py`, `setup.cfg`, and `package.xml`
- How to **publish velocity commands** to control a robot's motion
- How to **call ROS2 services** asynchronously and wait for their completion
- How **timer callbacks** can implement step-by-step state machines for motion control
- The difference between `rclpy.spin()` and `rclpy.spin_once()` and when to use each
- How to **cleanly destroy nodes** and shut down `rclpy` after task completion
- Practical use of **`geometry_msgs/Twist`** for 2D planar motion

---

##  Future Improvements

- [ ] Add a **pentagon** and **hexagon** using the existing `draw_polygon()` helper
- [ ] Accept shape input as a **ROS2 launch argument** instead of terminal input
- [ ] Publish shape-drawing **status** on a custom ROS2 topic
- [ ] Add a **ROS2 action server** to support cancellation and progress feedback mid-draw
- [ ] Support **custom shape sizes** via user input or ROS2 parameters
- [ ] Write proper **unit tests** for motion logic in the `test/` folder
- [ ] Package as a **ROS2 launch file** to start both Turtlesim and the drawer together

---

##  Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add: your feature description"`
4. Push the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [PEP8](https://peps.python.org/pep-0008/) style guidelines and keep ROS2 best practices in mind.

---

## 👤 Author

**B Suhas**

[![GitHub](https://img.shields.io/badge/GitHub-b--suhas-black?logo=github)](https://github.com/b-suhas)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-B%20Suhas-blue?logo=linkedin)](https://linkedin.com/in/b-suhas)

---

> _Built with curiosity and a love for robotics. If this project helped you learn ROS2, give it a ⭐!_
> 
