#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from Dijkstra import Dijkstra
from math import sqrt, atan2

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)



r = Dijkstra( [150,500,0], [240, 95],5, 40)
path, _ = r.solve()
solution = []
done = False

for point in path:
    solution.append(point)
for point in solution:
    print(translate(point.env[0], 0, 512, -55, 65),  -translate(point.env[1], 0, 512, -60, 60))

temp = raw_input("Done")
index = 0

def turnTheta(theta, offset):
    theta += offset
    if abs(theta) > 3.142:
        if theta > 0:
            theta = -3.142+(theta - 3.142)
        elif theta < 0:
            theta = 3.142+(theta + 3.142)
    return theta
    
def callback(data):
    global cmd_vel
    global solution
    global index
    global done
    if not done:
        desiredX = translate(solution[index].env[0], 0, 512, -55, 65) 
        desiredY =  -translate(solution[index].env[1], 0, 512, -60, 60)+5
        
        x = data.pose[1].position.x
        y = data.pose[1].position.y
        theta = euler_from_quaternion(quaternion=(data.pose[1].orientation.x, data.pose[1].orientation.y, data.pose[1].orientation.z, data.pose[1].orientation.w))[2]
        print(theta, atan2(desiredY -y, desiredX-x))
        theta = turnTheta(theta, -atan2(desiredY -y, desiredX-x)-1.57)
        print(theta)
        print([x, y], [desiredX, desiredY])
        if sqrt((x - desiredX)**2 + (y - desiredY)**2) < 5:
            index += 1
            if len(solution)-1 == index:
                
                done = True
        move_cmd = Twist()
        move_cmd.linear.x = 10
        if theta < 0:
            move_cmd.angular.z = 1
        elif theta > 0:
            move_cmd.angular.z = -1
        else:
            move_cmd.angular.z = 0
        cmd_vel.publish(move_cmd)
    else:
        cmd_vel.publish(Twist())

rospy.init_node('command_publisher')
cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
rospy.Subscriber("/gazebo/model_states", ModelStates, callback)
rospy.spin()
