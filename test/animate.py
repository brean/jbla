# -*- coding: utf-8 -*-
# install jbla and run this script inside blender e.g.
#  "C:\Program Files\Blender Foundation\Blender\blender.exe" data\test.blend --python animate.py
#
import os
import json
from jbla import BlenderAnimation

def test_animate(ani_path):
    ani = BlenderAnimation()
    ani.load(ani_path)
    ani.animate()

if __name__ == '__main__':
    test_animate('data/block_test.json')
