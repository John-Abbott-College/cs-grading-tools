# Assignment 3: Saving Turtles
import math
import random
import turtle

"""
This is helper code for creating screenshots of the turtle code at various stages.
"""

# ======================================================================
# Constants
# ======================================================================
LOOP_CONSTANT = 100000

EARTH_GRAVITY: float = 9.807  # Earth  (m/s^2)

# turtle land dimensions
(X_MIN, Y_MIN, X_MAX, Y_MAX) = -400, -400, 400, 400
GROUND_LEVEL = -100  # the y value of the ground level
OCEAN_X1 = 50
OCEAN_Y1 = 0
OCEAN_X2 = 250
OCEAN_Y2 = GROUND_LEVEL

# turtle initial position
X_START: int = X_MIN + 50
Y_START: int = GROUND_LEVEL

# wall position
X_WALL_MIN = 0
X_WALL_MAX = 10
Y_WALL_MIN = GROUND_LEVEL
Y_WALL_MAX = 100

# set up some turtle defaults
turtle.speed(0)  # this is the fastest
turtle.resizemode('user')
turtle.hideturtle()
turtle.bgcolor("lightblue")

# ======================================================================
# create our turtle
# ======================================================================
baby_turtle = turtle.Turtle()
baby_turtle.shape("turtle")
baby_turtle.color("orange", "green")  # Michealangelo
baby_turtle.shapesize(2.5, 2.5, 3)
baby_turtle.pensize(3)
baby_turtle.speed(0)

# ======================================================================
# set up text turtle
# ======================================================================
text_turtle = turtle.Turtle()
text_turtle.teleport(X_MIN+50, Y_MAX - 50)
font = ('Arial', 20, 'bold')
text_turtle.hideturtle()

# ======================================================================
# Your code goes here
# ======================================================================
text_turtle_font = ('Arial', 32, 'italic')

# set turtle back to original spot
baby_turtle.teleport(X_MIN, GROUND_LEVEL)

# motion diagram triangle
angle=36.87
turtle.begin_fill()
turtle.teleport(X_MIN,GROUND_LEVEL)

vx=turtle.clone()
vx.showturtle()
vx.shape("arrow")
vy=vx.clone()
v=vx.clone()

# vx
vx.color("red")
vx.pensize(3)
vx.shape("arrow")
vx.setheading(0)
vx.forward(200)
vx.stamp()
vx.hideturtle()
vx.write("Vx", font=text_turtle_font)
vx.forward(200)

# vy
vy.color("blue")
vy.pensize(3)
vy.shape("arrow")
vy.teleport(X_MIN+400,GROUND_LEVEL)
vy.setheading(90)
vy.forward(125)
vy.write(" Vy", font=text_turtle_font)
vy.forward(25)
vy.stamp()
vy.hideturtle()
vy.forward(150)

# v
v.color("purple")
v.pensize(6)
v.shape("arrow")
v.setheading(angle)
v.forward(225)
v.write("""V
""", font=text_turtle_font)
v.forward(275)

# reset
turtle.end_fill()
turtle.setheading(0)

text_turtle.teleport(X_MIN+75, GROUND_LEVEL)
text_turtle.write("Θ", font=text_turtle_font)
text_turtle.teleport(X_MIN+50, Y_MAX - 50)

turtle.exitonclick()

# draw the wall, the ground, and the ocean
# wall
# turtle.color("red")
# turtle.begin_fill()
# turtle.teleport(X_WALL_MIN,Y_WALL_MIN)
# for _ in range(2):
#     turtle.forward(X_WALL_MAX-X_WALL_MIN)
#     turtle.left(90)
#     turtle.forward(Y_WALL_MAX-Y_WALL_MIN)
#     turtle.left(90)
# turtle.end_fill()

# ground
# turtle.begin_fill()
# turtle.teleport(X_MIN, Y_MIN)
# turtle.color("green")
# turtle.showturtle()
# for _ in range(2):
#     turtle.forward(X_MAX-X_MIN)
#     turtle.left(90)
#     turtle.forward(GROUND_LEVEL-Y_MIN)
#     turtle.left(90)
# turtle.end_fill()

# ocean
# turtle.begin_fill()
# turtle.teleport(OCEAN_X1, Y_MIN)
# turtle.color("blue")
# for _ in range(2):
#     turtle.forward(OCEAN_X2-OCEAN_X1)
#     turtle.left(90)
#     turtle.forward(GROUND_LEVEL-Y_MIN)
#     turtle.left(90)
# turtle.end_fill()

# sun
# sun_x = X_MAX - 75
# sun_y = Y_MAX - 100
# turtle.teleport(sun_x,sun_y)
# turtle.fillcolor("yellow")
# turtle.color("yellow")
# turtle.begin_fill()
# radius = 40
# turtle.circle(radius)
# turtle.end_fill()
# turtle.pensize(3)
# num_rays = 20
# for _ in range(num_rays):
#     turtle.goto(sun_x, sun_y+radius)
#     turtle.forward(1.5*radius)
#     turtle.right(360/num_rays)
# turtle.hideturtle()

# ======================================================================
# Set the random wind
# ======================================================================
# wind_direction = 0
# wind_speed = 0

# wind_direction = random.randint(0, 360)
# wind_speed = random.randint(1, 20)
# wind_icon = turtle.Turtle()
# wind_icon.color("black")
# wind_icon.shape("arrow")
# wind_icon.left(wind_direction)
# wind_icon.teleport(X_MIN+20, Y_MAX-10)
# wind_speed = 0
# wind_icon.shapesize(stretch_len=0.5*wind_speed + 1)

# Inputs
x = X_START
y = Y_START
theta: float = turtle.numinput("Initial Conditions", "enter θ")
v: float = turtle.numinput("Initial Conditions", "enter initial velocity")

# find vector components
theta_r = math.radians(theta)
vx = math.cos(theta_r) * v
vy = math.sin(theta_r) * v

# got to the starting position
baby_turtle.teleport(x, y)

# set the turtle looking forward
angle = theta_r
baby_turtle.setheading(math.degrees(angle))
baby_turtle.speed(1)

# GO!
# purposely set this to something really small so that the animation is slow
# enough to let the students see the turtle heading changes as the turtle moves
dt = .2

# wind speed components
wind_x = wind_speed * math.cos(wind_direction * math.pi / 180.)
wind_y = wind_speed * math.sin(wind_direction * math.pi / 180.)


x_old = x
y_old = y
for i in range(LOOP_CONSTANT):
    x = x + (vx + wind_x) * dt
    vy = vy - EARTH_GRAVITY * dt
    y = y + (vy + wind_y) * dt - (1 / 2) * EARTH_GRAVITY * dt * dt

    baby_turtle.goto(x, y)

    angle = math.atan( (vy + wind_y) / (vx + wind_x))
    baby_turtle.seth(math.degrees(angle))

    # hit the wall
    if x_old <= X_WALL_MIN <= x and y < Y_WALL_MAX:
        text_turtle.write("Pride goeth before a fall: another turtle has hit the wall.", font=font)
        break

    # hit the ocean
    if y <= GROUND_LEVEL and OCEAN_X1 <= x <= OCEAN_X2:
        text_turtle.write("Yay: you have saved the day!!", font=font)
        break

    # hit the ground
    if y < GROUND_LEVEL:
        text_turtle.write("Too bad: your turtle is sad.", font=font)
        break

    x_old = x
    y_old = y


# IMPORTANT: don't change the code below this point:
#            AND, this needs to be at the bottom of the file
turtle.exitonclick()
