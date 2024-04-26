#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2023, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
"""
import sys
import math
import time
import datetime
import random
import traceback    
import threading

"""
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
# git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
# cd xArm-Python-SDK
# python setup.py install
"""
try:
    from xarm.tools import utils
except:
    pass
from xarm import version
from xarm.wrapper import XArmAPI

def pprint(*args, **kwargs):
    try:
        stack_tuple = traceback.extract_stack(limit=2)[0]
        print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
    except:
        print(*args, **kwargs)

pprint('xArm-Python-SDK Version:{}'.format(version.__version__))

arm = XArmAPI('192.168.1.210')
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)
time.sleep(1)

variables = {}
params = {'speed': 100, 'acc': 2000, 'angle_speed': 20, 'angle_acc': 500, 'events': {}, 'variables': variables, 'callback_in_thread': True, 'quit': False}


# Register error/warn changed callback
def error_warn_change_callback(data):
    if data and data['error_code'] != 0:
        params['quit'] = True
        pprint('err={}, quit'.format(data['error_code']))
        arm.release_error_warn_changed_callback(error_warn_change_callback)
arm.register_error_warn_changed_callback(error_warn_change_callback)


# Register state changed callback
def state_changed_callback(data):
    if data and data['state'] == 4:
        if arm.version_number[0] >= 1 and arm.version_number[1] >= 1 and arm.version_number[2] > 0:
            params['quit'] = True
            pprint('state=4, quit')
            arm.release_state_changed_callback(state_changed_callback)
arm.register_state_changed_callback(state_changed_callback)


# Register counter value changed callback
if hasattr(arm, 'register_count_changed_callback'):
    def count_changed_callback(data):
        if not params['quit']:
            pprint('counter val: {}'.format(data['count']))
    arm.register_count_changed_callback(count_changed_callback)


# Register connect changed callback
def connect_changed_callback(data):
    if data and not data['connected']:
        params['quit'] = True
        pprint('disconnect, connected={}, reported={}, quit'.format(data['connected'], data['reported']))
        arm.release_connect_changed_callback(error_warn_change_callback)
arm.register_connect_changed_callback(connect_changed_callback)



# Define Mydef class
class Mydef(object):
    def __init__(self, *args, **kwargs):
        pass

        @classmethod
        def function_1(cls):
            """
            Init arm: move above whiteboard then close gripper
            """
            # Initial Position
            if arm.error_code == 0 and not params['quit']:
                code = arm.set_position(x=157, y=8.4, z=272.4, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
                if code != 0:
                    params['quit'] = True
                    pprint('set_position, code={}'.format(code))
            if arm.error_code == 0 and not params['quit']:
                code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
                if code != 0:
                    params['quit'] = True
                    pprint('set_gripper_position, code={}'.format(code))

# release all event
if hasattr(arm, 'release_count_changed_callback'):
    arm.release_count_changed_callback(count_changed_callback)
arm.release_error_warn_changed_callback(state_changed_callback)
arm.release_state_changed_callback(state_changed_callback)
arm.release_connect_changed_callback(error_warn_change_callback)

# Settings
if not params['quit']:
    params['speed'] = 200
if not params['quit']:
    params['acc'] = 5000
# Initial Position
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=157, y=8.4, z=272.4, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
# Grab Pen
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(300, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=230, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=330, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Moving to the whiteboard
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=190, y=-89, z=300, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Descent the pen to whiteboard
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=190, y=-89, z=230, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Draw a horizontal line
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=190, y=80, z=230, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Lift the pen 
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=190, y=80, z=300, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Place back the pen
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=230, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(300, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
# Lift the Robotic Arm
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=170, y=217, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Back to Initial Position
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=157, y=8.4, z=272.4, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))

# Start the Erasing 

# Initial Position
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=157, y=8.4, z=272.4, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
# Grab Duster
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=173, y=330, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(700, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=173, y=330, z=169, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=173, y=330, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Moving to Whiteboard
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=-120, z=257, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=-120, z=180, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Release and Regrab
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(530, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=-120, z=185, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(460, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Start Cleaning
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=115, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=180, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=220, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=220, y=115, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=220, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=255, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=255, y=115, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=255, y=-120, z=174, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
# Place back the Duster
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=255, y=-120, z=257, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=173, y=330, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=173, y=330, z=169, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(700, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
# Go Back to Initial Postion
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=183, y=296, z=332, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_position(x=157, y=8.4, z=272.4, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))
if arm.error_code == 0 and not params['quit']:
    code = arm.set_gripper_position(0, wait=True, speed=5000, auto_enable=True)
    if code != 0:
        params['quit'] = True
        pprint('set_gripper_position, code={}'.format(code))


# release all event
if hasattr(arm, 'release_count_changed_callback'):
    arm.release_count_changed_callback(count_changed_callback)
arm.release_error_warn_changed_callback(state_changed_callback)
arm.release_state_changed_callback(state_changed_callback)
arm.release_connect_changed_callback(error_warn_change_callback)






