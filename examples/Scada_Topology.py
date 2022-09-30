#!/usr/bin/env python3
# -*- coding: utf8 -*-
#相關參考: https://blog.csdn.net/m0_45406092/article/details/118497597

 
"""

執行拓樸方法: sudo python3 Scada_Topology.py

"""
import re
from mininet.net import Containernet
from mininet.node import RemoteController, OVSSwitch,Docker,OVSBridge,UserSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
from mininet.link import Intf
from mininet.util import quietRun
def checkIntf( intf ): #檢查網卡是否被使用
    "Make sure intf exists and is not configured."
    config = quietRun( 'ifconfig %s 2>/dev/null' % intf, shell=True )
    if not config:
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', config )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
                'and is probably in use!\n' )
        exit( 1 )

class SCADA_Topo(Topo):
  def build(self):  
    #Add Switches
    OvS3=self.addSwitch('OvS3', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone') # standalone 為 沒有controller時會變成一般的switch
    OvS4=self.addSwitch('OvS4', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone')
    OvS5=self.addSwitch('OvS5', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone') 
    # OvS3=self.addSwitch('OvS3', switch=UserSwitch,failMode='standalone') # standalone 為 沒有controller時會變成一般的switch
    # OvS4=self.addSwitch('OvS4', switch=UserSwitch,failMode='standalone')
    # OvS5=self.addSwitch('OvS5', switch=UserSwitch,failMode='standalone') 
    #Add Links
    self.addLink(OvS3,OvS4)
    self.addLink(OvS4,OvS5)

def Scada_Network_Topology():
    topology= SCADA_Topo()
    #Add Controller
    net = Containernet(topo=topology,controller=None)
    c1=RemoteController('c1',ip='192.168.20.134',port=6653)
    net.addController(c1)
    #Add Docker
    d1 = net.addDocker('d1',ip="192.168.3.11/24",defaultRoute="via 192.168.3.254",dimage="softplc2.plc.student:latest")
    d2 = net.addDocker('d2',ip="192.168.3.12/24",defaultRoute="via 192.168.3.254",dimage="softplc2.plc.student")
    # d2 = net.addDocker('d2',ip="192.168.3.12/24",defaultRoute="via 192.168.3.254",dimage="ubuntu:trusty")
    #取得OvS
    OvS3=net.get('OvS3')
    OvS4=net.get('OvS4')
    OvS5=net.get('OvS5')
    #Add Links
    net.addLink(OvS3,d1)
    net.addLink(OvS4,d2)
    interface_OvS3='enp7s0f0'
    checkIntf( interface_OvS3 )
    #將實體接口接到OvS上
    _intf=Intf(interface_OvS3,node=OvS3)
    #將網卡設為 混和模式
    OvS3.cmd('ip link set ' + interface_OvS3 + ' promisc on')
    interface_OvS5='enp8s0f1'
    checkIntf( interface_OvS5 )
    #將實體接口接到OvS上
    _intf=Intf(interface_OvS5,node=OvS5)
    d1.cmd("ifconfig d1-eth0 192.168.3.11/24") #將介面設定ip
    d1.cmd("route add default gw 192.168.3.254") #將介面設定ip
    d1.cmd("ifconfig eth0 down") #關閉預設網卡
    d2.cmd("ifconfig d2-eth0 192.168.3.12/24")
    d2.cmd("route add default gw 192.168.3.254")
    d2.cmd("ifconfig eth0 down") #關閉預設網卡
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    Scada_Network_Topology()