#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from MoziService.mozi_service import MoziService
from MoziService.entitys.scenario import CScenario
import pylog
import time
import json
from websocket import create_connection
from test.my_test.geo import*
from MoziService.entitys.args import*
#from test.my_test.ship_agent import CAgent


class Environment():
    '''
    环境
    '''
    def __init__(self, IP, AIPort, scenario_name, simulate_compression):
        self.server_ip = IP
        self.aiPort = AIPort
        self.scenario_name = scenario_name
        self.websocker_conn = None
        self.mozi_server = None
        self.scenario = None
        self.connect_mode = 1
        self.num = 1
        self.simulate_compression = simulate_compression
        #self.agent = CAgent()
    
    def step(self):
        '''
        步长
        主要用途：
        单步决策的方法
        根据环境态势数据改变战场环境
        '''
        time.sleep(1/3)
        self.mozi_server.suspend_simulate()
        self.mozi_server.update_situation(self.scenario)#数据更新
        self.redside.static_update()#数据组合
        self.blueside.static_update()
        #写了一个my_step函数，用来执行动作
        self.my_step(self.blueside)
        self.mozi_server.run_simulate()
        return self.scenario
    
    def reset(self):
        '''
        重置函数
        主要用途：
        加载想定，
        '''
        self.mozi_server.suspend_simulate() 
        self.mozi_server.load_scenario("linux")
        self.create_scenario() 
        self.mozi_server.init_situation(self.scenario)
        self.redside = self.scenario.get_side_by_name('红方')# 获得红方的主对象
        self.redside.static_construct() # 结构化平台返回数据，存入相应的实体属性中,
        self.blueside = self.scenario.get_side_by_name('蓝方')# 获得蓝方的主对象
        self.blueside.static_construct()
        self.mozi_server.run_simulate()
        self.mozi_server.set_simulate_compression(4) #设定推演步长
        
        
        #为了便于区分，定义了一个新的函数my_prepeo,以实例化的推演方对象作为参数输入，对推演前的任务进行设置

        self.my_prepro(self.blueside)


    def create_scenario(self):
        '''
        建立一个想定对象
        '''
        self.scenario = CScenario(self.mozi_server)

    def connect_mozi_server(self, websocket_Ip, websocket_port):
        """
        连接墨子服务器
        param ：
        websocket_server 要连接的服务器的ip
        websocket_port 要连接的服务器的端口
        :return:
        """
        pylog.info("connect_mozi_server")
        if self.connect_mode == 1:
            self.mozi_server = MoziService(self.server_ip ,self.aiPort,self.scenario_name)
            return True
        # server_address = r"ws://%s:%d/websocket" % ('60.205.207.206', 9998)
        server_address = r"ws://%s:%d/websocket" % (websocket_Ip, websocket_port)
        pylog.info(server_address)
        for i in range(10):
            try:
                self.websocket_connect = create_connection(server_address)
                break
            except:
                pylog.info("can not connect to %s." % server_address)
                time.sleep(2)
                self.websocket_connect = None
        #
        if self.websocket_connect is None:
            pylog.warning("Interrupted, can not connect to %s." % server_address)
            return False
        #
        self.websocket_connect.send("{\"RequestType\":\"StartServer\"}")
        result = self.websocket_connect.recv()
        print("connect server result:%s" % result)
        jsons = json.loads(result)
        self.ai_server = jsons['IP']
        self.ai_port = jsons['AIPort']
        self.mozi_task = MoziService(self.server_ip ,self.aiPort,self.scenario_name)
        return True

    def start(self):
        '''
        开始函数
        主要用途：
        1.连接服务器端
        2.设置决策时间
        3.设置智能体决策想定是否暂停
        '''
        self.connect_mozi_server(self.server_ip,self.aiPort)
        self.mozi_server.set_run_mode()
        self.mozi_server.one_time_stop(10)
        
    def my_prepro(self,side):
        '''
        设置预先设定的任务
        '''
        #清空原本的想定任务
        mission_keys=list(self.blueside.missions.keys())
        for k in mission_keys:
            self.blueside.delete_mission(k)
        
        
        #记录信息，这部分是用来做条件判断
        self.enm_miss=[]
        
        
        #设置推演方条令，对水面自由开火，对空自由开火，电磁管控开
        doctrine=side.get_doctrine()
        doctrine.set_weapon_control_status_surface(0)
        doctrine.set_weapon_control_status_air(0)
        doctrine.set_em_control_status('Radar','Active')
        
        #设置武器打击距离
        #51
        doctrine.set_weapon_release_authority(weapon_dbid='51',target_type='1999', quantity_salvo='1', shooter_salvo='1',firing_range='45')
        doctrine.set_weapon_release_authority(weapon_dbid='51',target_type='2000', quantity_salvo='1', shooter_salvo='1',firing_range='45')
        doctrine.set_weapon_release_authority(weapon_dbid='51',target_type='2001', quantity_salvo='1', shooter_salvo='1',firing_range='45')
        
        #15
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='2200', quantity_salvo='1', shooter_salvo='1',firing_range='25')
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='2201', quantity_salvo='1', shooter_salvo='1',firing_range='25')
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='2202', quantity_salvo='1', shooter_salvo='1',firing_range='25')        
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='2203', quantity_salvo='1', shooter_salvo='1',firing_range='25')
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='2204', quantity_salvo='1', shooter_salvo='1',firing_range='25')        
        doctrine.set_weapon_release_authority(weapon_dbid='15',target_type='1999', quantity_salvo='1', shooter_salvo='1',firing_range='20')
        

        #第一个是空战巡逻任务，主要是执行对空作战的歼击机，进行空中巡逻。第二个是空战等待任务，
        #创建空战任务飞机的巡逻区（以驱逐舰为中心的八边形，内径长80km）
        a=0
        ship=side.ships['6d829dba-2092-4b9d-a824-05ae1cb74c9b']
        point_list='{type="AAW",Zone={'
        for i in range(8):
            temp=get_geopoint_from_distance(geo_point=(ship.dLatitude,ship.dLongitude), azimuth=22.5+i*45, distance_m=80*1000)
            side.addReferencePoint('AAW_Attack'+str(i),temp[0],temp[1])
            if i!=7:
                point_list+=('"AAW_Attack'+str(i)+'",')
            else:
                point_list+=('"AAW_Attack'+str(i)+'"}}')
        print(point_list)
        side.add_mission('空战巡逻','Patrol',point_list)
        
        
        #创建突击任务飞机的巡逻区（以驱逐舰为中心的八边形，内径长30km）
        a=0
        point_list='{type="AAW",Zone={'
        for i in range(8):
            temp=get_geopoint_from_distance(geo_point=(ship.dLatitude,ship.dLongitude), azimuth=22.5+i*45, distance_m=30*1000)
            side.addReferencePoint('AAW_Wait'+str(i),temp[0],temp[1])
            if i!=7:
                point_list+=('"AAW_Wait'+str(i)+'",')
            else:
                point_list+=('"AAW_Wait'+str(i)+'"}}')
        
        side.add_mission('空战等待','Patrol',point_list)
        
        #创建突击任务
        side.add_mission('对水攻击','STRIKE',"{type='LAND'}")
        
        #对每类飞机设置标签，记录当前信息。
        self.AAW_Attack={}
        self.AAW_Wait={}
        
        for k,v in side.aircrafts.items():
            temp=v.strName.split('#')
            if int(temp[1])>8:
                self.AAW_Attack[k]={'空战巡逻':True}
            else:
                self.AAW_Wait[k]={'空战等待':True, '对水攻击':False}
        
        #最后一行代码，是用来标记任务是否进行了设置，在step中会用到。
        self.mission_setting=False    
        
    def get_enmInfo(self, side):
        '''
        获取探测信息
        '''
        #print(side.contacts)
        airs=dict()
        air_missiles=dict()
        ship_missiles=dict()
        defense_missiles=dict()
        ships=dict()
        for k,v in side.contacts.items():
            
            temp=v.get_contact_info()
            if temp['typed']==2:
                ships[k]={'name':temp['name'],'fg':temp['fg'],'longitude':temp['longitude'],'latitude':temp['latitude'],
                          'alt':temp['altitude'],'heading':temp['heading'],'speed':temp['speed']}
            if temp['typed']==1 and '导弹' in temp['name']:
                air_missiles[k]={'name':temp['name'],'fg':temp['fg'],'longitude':temp['longitude'],'latitude':temp['latitude'],
                          'alt':temp['altitude'],'heading':temp['heading'],'speed':temp['speed']}
            if temp['typed']==0:
                airs[k]={'name':temp['name'],'fg':temp['fg'],'longitude':temp['longitude'],'latitude':temp['latitude'],
                          'alt':temp['altitude'],'heading':temp['heading'],'speed':temp['speed']}
            if temp['typed']==1 and ('VAMPIRE' in temp['name'] or 'GuidedWeapon' in temp['name']):
                ship_missiles[k]={'name':temp['name'],'fg':temp['fg'],'longitude':temp['longitude'],'latitude':temp['latitude'],
                          'alt':temp['altitude'],'heading':temp['heading'],'speed':temp['speed']}
            if temp['typed']==1 and '防空' in temp['name'] :
                defense_missiles[k]={'name':temp['name'],'fg':temp['fg'],'longitude':temp['longitude'],'latitude':temp['latitude'],
                          'alt':temp['altitude'],'heading':temp['heading'],'speed':temp['speed']}
        #敌方飞机，舰船，空空弹，空地弹，地空弹    
        return  airs,ships,air_missiles,ship_missiles,defense_missiles     
    
    def my_step(self,side):
        '''
        实现自身的规则设计
        '''
        #获得己方任务对象，根据我们之前定义的名字，拿到被对象化的任务实例
        for k,v in side.missions.items():
            if '巡逻' in v.strName:
                AAW_Attack=v
            elif '等待' in v.strName:
                AAW_Wait=v
            else:
                LAND_Attack=v
        
        #获取敌方实体信息，接下来是我自己写的一个函数，用来对敌方的信息进行抽取，我将其分为飞机、舰船，空空弹，反舰弹，防空弹五类。
        airs,ships,air_missiles,ship_missiles,defense_missiles=self.get_enmInfo(side)
        
        #记录敌方发射的空空弹
        for k,v in air_missiles.items():
            if k not in self.enm_miss:
                self.enm_miss.append(k)
        
        #获取敌方驱逐舰信息，我这里获取敌方的舰船guid，这个值是要传给打击任务的。
        ship_target=None
        for k,v in ships.items():
            if '驱逐舰' in v['name']:
                ship_target=k
        
        #首次进入对任务的规则进行设置
        if not self.mission_setting:
            #巡逻任务：关闭三分之一，关闭防区外探测，设置单机编队，设置出航、阵位、攻击速度；设置高度。
            AAW_Attack.set_one_third_rule('false')
            AAW_Attack.set_OPA_check(False)
            AAW_Attack.set_flight_size(FlightSize.One)
            AAW_Attack.set_throttle_transit(Throttle.Cruise)
            AAW_Attack.set_throttle_station(Throttle.Loiter)
            AAW_Attack.set_throttle_attack(Throttle.Loiter)
            AAW_Attack.set_transit_altitude(8000)
            AAW_Attack.set_station_altitude(8000)
            AAW_Attack.set_attack_altitude(8000)
            
            AAW_Wait.set_one_third_rule('false')
            AAW_Wait.set_OPA_check(False)
            AAW_Wait.set_flight_size(FlightSize.One)
            AAW_Wait.set_throttle_transit(Throttle.Cruise)
            AAW_Wait.set_throttle_station(Throttle.Loiter)
            AAW_Wait.set_throttle_attack(Throttle.Loiter)
            AAW_Wait.set_transit_altitude(8000)
            AAW_Wait.set_station_altitude(8000)
            AAW_Wait.set_attack_altitude(8000)            
            
            #打击任务：设置单机编队,设置预先规划，添加打击目标，设置最小打击半径,设置多扇面攻击
            LAND_Attack.set_flight_size(FlightSize.One)
            LAND_Attack.set_preplan(True)
            LAND_Attack.add_target([k])
            LAND_Attack.set_min_strike_radius(30)
            LAND_Attack.set_auto_planner(True)

            self.mission_setting=True
        
                
        #规则实现，根据敌方的空中防御力量，判断是否发起对水攻击任务

        if len(self.enm_miss)>60 or len(airs)<3:
            for k,v in self.AAW_Wait.items():
                self.AAW_Wait[k]['对水攻击']=True
                self.AAW_Wait[k]['空战等待']=False
        else:
            for k,v in self.AAW_Wait.items():
                self.AAW_Wait[k]['对水攻击']=False
                self.AAW_Wait[k]['空战等待']=True
        

        #获取任务的分配单元
        AAW_Attack_list=AAW_Attack.get_assigned_mission()
        AAW_Wait_list=AAW_Wait.get_assigned_mission()
        LAND_Attack_target=LAND_Attack.get_targets()
        LAND_Attack_list=LAND_Attack.get_assigned_mission()

        #根据存储标识，将飞机分向指定任务
        for k,v in self.AAW_Attack.items():
            if k not in AAW_Attack_list and self.AAW_Attack[k]['空战巡逻']:
                #先清空出之前的任务
                if k  in LAND_Attack_list:
                    LAND_Attack.scenEdit_unAssignUnitFromMission(k)
                #在分配至新任务
                AAW_Attack.assignUnitToMission(k)
                
        
        for k,v in self.AAW_Wait.items():
            if k not in AAW_Wait_list and self.AAW_Wait[k]['空战等待']:
                side.aircrafts[k].delete_coursed_point(clear=True)
                #先清空出之前的任务
                if k  in LAND_Attack_list:
                    LAND_Attack.scenEdit_unAssignUnitFromMission(k)
                
                AAW_Wait.assignUnitToMission(k)
                
            if k not in LAND_Attack_list and self.AAW_Wait[k]['对水攻击']:
                #先清空出之前的任务
                if k  in AAW_Wait_list:
                    AAW_Wait.scenEdit_unAssignUnitFromMission(k)
                
                LAND_Attack.assignUnitToMission(k)
                
        
    def get_mysideInfo(self, side):
        '''
        传入推演方
        输出：
        {
         'ships':{guid:{}},
         'airs':{guid:{}},
         'ship_missiles':{guid:{}},
         'air_missiles': {guid:{}}
         }
        '''
        ships=dict()
        airs=dict()
        missiles=dict()
    
        
        for k,v in side.ships.items():
            ships[k]={'latitude':v.dLatitude,'longitude':v.dLongitude,'name':v.strName}
    
                
        for k,v in side.aircrafts.items():
            airs[k]={'latitude':v.dLatitude,'longitude':v.dLongitude,'alt':v.fCurrentAlt,
                      'speed':v.fDesiredSpeed,'name':v.strName}
            
            
        for k,v in side.weapons.items():
            missiles[k]={'latitude':v.dLatitude,'longitude':v.dLongitude,'alt':v.fCurrentAlt,
                      'speed':v.fDesiredSpeed,'target':v.m_PrimaryTargetGuid,'from':v.m_FiringUnitGuid,'name':v.strName}
    
        return ships,airs, missiles