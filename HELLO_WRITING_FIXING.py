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
import re

def convert_ngc_to_2d_array(file_path):
    array_2d = []
    patterns = {
        'G00': r'G00\s+(?:X(-?\d+(?:\.\d+)?))?\s*(?:Y(-?\d+(?:\.\d+)?))?\s*(?:Z(-?\d+(?:\.\d+)?))?',
        'G01': r'G01\s+(?:X(-?\d+(?:\.\d+)?))?\s*(?:Y(-?\d+(?:\.\d+)?))?\s*(?:Z(-?\d+(?:\.\d+)?))?',
        'G02': r'G02\s+X(-?\d+(?:\.\d+)?)\s+Y(-?\d+(?:\.\d+)?)\s+Z(-?\d+(?:\.\d+)?)',
        'G03': r'G03\s+X(-?\d+(?:\.\d+)?)\s+Y(-?\d+(?:\.\d+)?)\s+Z(-?\d+(?:\.\d+)?)'
    }

    with open(file_path, 'r') as file:
        for line in file:
            for gcode, pattern in patterns.items():
                if gcode in line:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        values = [float(value) if value else 0.0 for value in match]
                        values[0] *= 0.5589997037  # Multiply x by 0.5589997037
                        values[1] = values[1] * 0.5589997037 + 200.0  # Multiply y by 0.5589997037 and add 200.0
                        values[2] += 217.0  # Add 189.0 to z
                        array_2d.append(values)
                    break

    return array_2d

# Dictionary to map letters to file names.
LETTER_TO_FILE = {
    'H': "H_Inverted_output_0001.ngc",
    'E': "E_Inverted_output_0001.ngc",
    'L': "L_Inverted_output_0001.ngc",
    'O': "O_Inverted_output_0002.ngc"
}

# List to store the 2D arrays for each letter.
ARRAYS = []

# Define a function to convert the .ngc files to 2D arrays and scale the arrays.
def convert_letters_to_arrays(letters):
    global ARRAYS
    ARRAYS = []
    for letter in letters:
        file_path = LETTER_TO_FILE[letter]
        array = convert_ngc_to_2d_array(file_path)
        ARRAYS.append(array)

# User input
letters = input("Enter a string (e.g. HELLO): ").upper()
convert_letters_to_arrays(letters)

# Print the array of different Y array offsets for different counters.
offsets = [-100, -50, 0, 50, 100]
for i, array in enumerate(ARRAYS):
    print(f"Letter {chr(ord('A') + i)}:")
    for j, point in enumerate(array):
        print(f"  Point {j}: {point[0]}, {point[1] + offsets[i]}, {point[2]}")

# Define a new function called raise_arm that moves the arm to a higher z-position:
def raise_arm(arm, z_offset=20):
    code, position = arm.get_position()
    new_z = position[2] + z_offset
    code = arm.set_position(x=position[0], y=position[1], z=new_z, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('raise_arm, code={}'.format(code))

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

# Settings
if not params['quit']:
    params['speed'] = 200
if not params['quit']:
    params['acc'] = 5000

# Define a function to raise the Z coordinate of the arm
def raise_z(arm, z_offset=50):
    code, position = arm.get_position()
    new_z = position[2] + z_offset
    code = arm.set_position(x=position[0], y=position[1], z=new_z, roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
    if code != 0:
        params['quit'] = True
        pprint('set_position, code={}'.format(code))

# Write the letters with a pause and Z raise between each letter
for i, array in enumerate(ARRAYS):
    print(f"Letter {letters[i]}:")
    for count, point in enumerate(array):
        if len(point) == 3:
            if point[0] == 0:
                pass
            else:
                if arm.error_code == 0 and not params['quit']:
                    print(f"  Point {count}: {point[1]}")
                    code = arm.set_position(x=point[1], y=point[0] + offsets[i], z=point[2], roll=-3.14, pitch=0, yaw=-0.76, is_radian=True)
                    if code != 0:
                        params['quit'] = True
                        pprint('set_position, code={}'.format(code))
    time.sleep(1)  # pause for 1 second between letters
    raise_z(arm)  # raise the Z coordinate before writing the next letter

# release all event
if hasattr(arm, 'release_count_changed_callback'):
    arm.release_count_changed_callback(count_changed_callback)
arm.release_error_warn_changed_callback(state_changed_callback)
arm.release_state_changed_callback(state_changed_callback)
arm.release_connect_changed_callback(error_warn_change_callback)