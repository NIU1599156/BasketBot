<img src="https://www.safbonwater.com/wp-content/uploads/2017/09/image-placeholder.jpg" align="right" width="300" alt="header picture"/>

# Basket-Bot
# Table of Contents
* [Description](#description)
* [Requirements](#requirements)
    * [Software](#software)
    * [Hardware](#hardware)
* [How to use](#how-to-use)
* [Authors](#authors)

# Description
This robot will consist of a rotating base with a camera, a barrier that can be raised and lowered with a servo, and two wheels attached to motors that will move at the desired speed.

When the robot is turned on, all the electronic components will be set to their initial positions and a barrier will be placed for the ball, which we will place on the initial downward ramp, to keep it in an initial position. Simultaneously, the robot will start rotating and taking photos with the camera. Using computer vision, we will be able to process and identify the target, estimating the actual distance to the point where we should shoot the ball.

Once the target is centered, the necessary calculations will be made to determine the speed at which the motors should move, so that when the barrier is unlocked, the ball will be launched towards an upward slope, following a trajectory that will make it score into the target. The position of the target can be changed within a certain range so the robot must be able to detect it and still score the ball.

# Requirements
## Software
- [Python 3.10.x or greater](https://www.python.org/)
- [gpiozero](https://pypi.org/project/gpiozero/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- Future software requirements...

## Hardware
- Raspberry PI 3 B
- Camera Module for Raspberry Pi
- 2 Servos
- 2 Electric Motors
- Servo Controller
- Electric Motor Controller
- Power Supply for Raspberry Pi
- Battery Holder

# How to use
TODO: Here goes the description of usage...

# Authors
- Oriol Camps Isus
- Martí Bruix Fernández
- Gabriel Chirinos Sulcany
- Iván Peñarando Martínez