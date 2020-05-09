#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2020-01-07 03:28
# Modified date : 2020-01-09 19:31
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import torch
import os

app_abspath = os.path.dirname(__file__)
USE_CUDA = False
device = torch.device("cuda" if USE_CUDA else "cpu")

#######################
#我们可以看到，这里是定义了一些参数，，这前四个是比较重要的。
SERVER_IP = "192.168.142.128" #是连接linux的ip
SERVER_PORT = "6260"          #是学习端口
SCENARIO_NAME = "final_scenario"  # 想定是本次大赛的想定，
simulate_compression = 4 #推演时间步长档位（0：1 秒，1：2 秒，2：5 秒，3：15 秒，4：30 秒，5：1 分钟，6：5 分钟，7：15 分钟，8：30 分钟）
DURATION_INTERVAL = 30
target_radius = 3700.0
control_noise = True
#######################
MAX_EPISODES = 5000
MAX_BUFFER = 1000000
MAX_STEPS = 30
#######################

#######################
TMP_PATH = "%s/%s/tmp" % (app_abspath, SCENARIO_NAME)
OUTPUT_PATH = "%s/%s/output" % (app_abspath, SCENARIO_NAME)

CMD_LUA = "%s/cmd_lua" % TMP_PATH
PATH_CSV = "%s/path_csv" % OUTPUT_PATH
MODELS_PATH = "%s/Models/" % OUTPUT_PATH
EPOCH_FILE = "%s/epochs.txt" % (OUTPUT_PATH)
#######################

TRANS_DATA = True
