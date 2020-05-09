#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-01-09 19:22
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

import numpy as np
import gc
from test.my_test.env import Environment
from test.my_test import etc
from test.my_test.ship_agent import CAgent



        
def run(env):
    #start()函数不动
    env.start()
    while True:
        
        env.reset()
        i=0
        while True:
            condition = env.step()
            
            print(i,env.blueside.iTotalScore)
            i+=1
            





def main():
    env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)

    run(env)



main()
