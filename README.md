# Course
针对第四届兵棋推演想定，做简要规则和学习BOT，供大家参考。

#Rule
Rule文件夹下my_test文件夹代码为基于规则的BOT，将my_test文件夹整体拷入官方提供的代码的./test目录下即可，并将官方中的main函数引用修改为 from test.my_test import main

#想定导入linux
1. 将/Scenarios下的final_scenario.xml，拷贝至linux系统下
2. 打开想定文件的目录文件，并右击-在此打开终端，输入
    sudo docker cp final_scenario.xml ba704ff982a9:/home/LinuxServer/Scenarios
    ba704ff982a9为docker ID，每个人的不一致。
3. 可在docker目录下的/home/LinuxServer/Scenarios目录下查看
