#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from RRTStar import RRTStar
from math import sqrt, atan2
from time import time

# Mapping function for converting coordinate from domain of serach algorithm to gazebo
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


# Initiate object
r = RRTStar( [150,500], [240, 95],512, 512, 1000, 10)
start = time()
# Solve
path = r.solve()
# Print Time taken
print(time()-start)
solution = []
done = False

# Get output path
for point in path:
    solution.append(point)
for point in solution:
    print(translate(point.env[0], 0, 512, -55, 65),  -translate(point.env[1], 0, 512, -60, 60))

# Wait for user input as user has to start the simulation
temp = raw_input("Done")
index = 0

# Map Theta from gazebo value to search algorithm value
def turnTheta(theta, offset):
    theta += offset
    if abs(theta) > 3.142:
        if theta > 0:
            theta = -3.142+(theta - 3.142)
        elif theta < 0:
            theta = 3.142+(theta + 3.142)
    return theta
    
# Callback function for subscriber
def callback(data):
    # Access global variables
    global cmd_vel
    global solution
    global index
    global done
    # If path is not compeleted
    if not done:
        # Get coordinated of next desired step in the computed path
        desiredX = translate(solution[index].env[0], 0, 512, -55, 65) + 5
        desiredY =  -translate(solution[index].env[1], 0, 512, -60, 60)
        # Get rovers coordinate
        x = data.pose[1].position.x
        y = data.pose[1].position.y
        theta = euler_from_quaternion(quaternion=(data.pose[1].orientation.x, data.pose[1].orientation.y, data.pose[1].orientation.z, data.pose[1].orientation.w))[2]
        print(theta, atan2(desiredY -y, desiredX-x))
        # Compute expected theta of rover
        theta = turnTheta(theta, -atan2(desiredY -y, desiredX-x)-1.57)
        print(theta)
        print([x, y], [desiredX, desiredY])
        # Check if robot has readed next desired step
        if sqrt((x - desiredX)**2 + (y - desiredY)**2) < 5:
            # increment till path is present
            index += 1
            if len(solution)-1 == index:
                done = True
        # Create command and set value
        move_cmd = Twist()
        move_cmd.linear.x = 10
        if theta < 0:
            move_cmd.angular.z = 1
        elif theta > 0:
            move_cmd.angular.z = -1
        else:
            move_cmd.angular.z = 0
        # Publish command
        cmd_vel.publish(move_cmd)
    # If path gets completed
    else:
        # Stop rover
        cmd_vel.publish(Twist())

# Initiate ROS node
rospy.init_node('command_publisher')
# Create publisher to publish commands to the rover
cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
# Get rover state
rospy.Subscriber("/gazebo/model_states", ModelStates, callback)
# Keep script in loop till ROS is running
rospy.spin()
