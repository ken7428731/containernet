#!/usr/bin/env python
# -*- coding: utf8 -*-
#相關參考: https://blog.csdn.net/m0_45406092/article/details/118497597

 
"""
2022.07.18
3 host 3 switch, topo is link
拓樸可查看 /mininet/Everyday_set_log/20220718/Mininet_Topology.png
            c1
          /  |     \
        /    |       \
      /      |        \
    s3------s4-------s5
     |        |       |
     h1       h2      h3



執行拓樸方法: sudo python Scada_Topology.py

"""
import re
from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
from mininet.net import Mininet
from mininet.link import Intf
from mininet.node import RemoteController, OVSSwitch
from mininet.topo import Topo
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
      #Add host
      h1=self.addHost('h1',ip="192.168.3.11/24",mac="00:00:00:00:00:01",defaultRoute="via 192.168.3.254")
      h2=self.addHost('h2',ip="192.168.3.12/24",mac="00:00:00:00:00:02",defaultRoute="via 192.168.3.254")
      h3=self.addHost('h3',ip="192.168.3.14/24",mac="00:00:00:00:00:03",defaultRoute="via 192.168.3.254")

      #Add Switches
      # OvS3=self.addSwitch('OvS3', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone')
      OvS3=self.addSwitch('OvS3', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone') # standalone 為 沒有controller時會變成一般的switch
      OvS4=self.addSwitch('OvS4', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone')
      OvS5=self.addSwitch('OvS5', switch=OVSSwitch, protocols='OpenFlow15',failMode='standalone') 

      #Add Controller
      # c0=self.addController(name='c1',controller=RemoteController,ip='192.168.20.134',port=6653)

      #Add Links
      self.addLink(OvS3,h1)
      self.addLink(OvS4,h2)
      self.addLink(OvS5,h3)

      self.addLink(OvS3,OvS4)
      self.addLink(OvS4,OvS5)

        

def Scada_Network_Topology():
   topology= SCADA_Topo()
   #Add Controller
   c1=RemoteController('c1',ip='192.168.20.134',port=6653)
   net = Mininet(topo=topology,controller=c1)
   #取得OvS
   OvS3=net.get('OvS3')
   interface_OvS3='ens39'
   checkIntf( interface_OvS3 )
   #將實體接口接到OvS上
   _intf=Intf(interface_OvS3,node=OvS3)
   #將網卡設為 混和模式
   OvS3.cmd('ip link set ' + interface_OvS3 + ' promisc on')

   OvS5=net.get('OvS5')
   interface_OvS5='ens40'
   checkIntf( interface_OvS5 )
   #將實體接口接到OvS上
   _intf=Intf(interface_OvS5,node=OvS5)
   #將網卡設為 混和模式
   # OvS5.cmd('ip link set ' + interface_OvS5 + ' promisc on') #為什麼不用是因為 interface_OvS5 為接PLC的部分(為設備)，所以不用使用混和模式

  #  #-----連接 labtainer 網路----
  #  #取得OvS
  #  OvS3=net.get('OvS3')
  #  interface_OvS3_labtainer_hmi='ens41'
  #  checkIntf( interface_OvS3_labtainer_hmi )
  #  #將實體接口接到OvS上
  #  _intf=Intf(interface_OvS3_labtainer_hmi,node=OvS3)
  #  OvS3.cmd('ip link set ' + interface_OvS3_labtainer_hmi + ' promisc on')

  #   #取得OvS
  #  OvS5=net.get('OvS5')
  #  interface_OvS5_labtainer_plc='ens42'
  #  checkIntf( interface_OvS5_labtainer_plc )
  #  #將實體接口接到OvS上
  #  _intf=Intf(interface_OvS5_labtainer_plc,node=OvS5)
  #  OvS5.cmd('ip link set ' + interface_OvS5_labtainer_plc + ' promisc on')

   #-------------------------------


   net.start()
   CLI(net)
   net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    Scada_Network_Topology()
