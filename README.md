基於軟體定義網路技術之工業控制場域防護系統-Factory Simulator
=====

環境設定資訊(Environmental Setting Information):
===========
- Python3 Version: 3.8.1  
- OS version: Ubuntu 20.04.4
- Ansible
- 會需要兩張實體網卡(Requires two physical network cards)

此程式網路拓樸(Network Topology):
===========
<p align="center" width="100%">
    <img src="/examples/Network_Topology/Beverage_and_food_processing_factory-Virtual_map.jpg"> 
</p>

整體拓樸圖可以參考:[ryu](https://github.com/ken7428731/ryu.git)上查看。  

enp7s0f0 實體介面卡為 連接OvS2。  
enp8s0f1 實體介面卡為 連接PLC(FX5U-32MR/ES)(Beverage Injection)。  

安裝步驟(Installation Steps):
===========
安裝 Ansible  
   `sudo apt-get install ansible`

下載 SDN_Containernet  
   `git clone https://github.com/ken7428731/containernet.git`

自動部署安裝環境  
   `sudo ansible-playbook -i "localhost," -c local containernet/ansible/install.yml`

下載OpenPLC image檔  
   `sudo docker pull mfthomps/softplc2.plc.student`

執行步驟(Execution Steps):
===========
進到examples檔案  
   `cd containernet/examples/`

執行程式  
   `sudo python3 Scada_Topology.py`

執行OpenPLC([可以參考此頁面](https://hackmd.io/@rrpSFv-qSLunmXT6FGkwBg/SksRTxVzo)):  
1. 在 containernet上呼叫 openplc  
  containernet> `xterm d1`  
2. 開啟後再啟動openplc  
  root@d1:"/OpenPLC_v3#` ./start_openplc.sh`  
3. 在打開瀏覽器並打  
  http://192.168.3.11:8080/dashboard  
  帳號:openplc  
  密碼:openplc  
4. 再點選左邊的Programs  
  http://192.168.3.11:8080/programs  
5. 再將下面設定好的OpenPLC程式上傳上去，並按下Upload program。   
  [OpenPLC_Program.st](https://drive.google.com/drive/folders/1MOETbarzHGuTUVB_uI-NYxO6iN33DPmu?usp=sharing)
6. 這時會跳出 設定程式名稱，設定完後，再點選Upload program。  
7. 編譯完後，先點選再點Go to Dashboard按鈕，在選左邊的 Start PLC 即可完成啟動。  
另外一台OpenPLC2手法也類似。  

注意(Note)
=======
Scada_Topology.py 此程式有綁定兩張網卡(enp7s0f0、enp8s0f1)，如果沒有兩張網卡請到程式註解 # 71行~80行，或修改其他網卡。  

如果要修改程式，可以到 Containernet 的網站上查看教學。  


參考(Reference)
=======
1. Containernet: https://containernet.github.io/
2. Labtainers: https://nps.edu/web/c3o/labtainers
3. Labtainers softplc2 plc docker image: https://hub.docker.com/r/mfthomps/softplc2.plc.student
4. Industrial Control Field Protection System Based on Software-defined Network Technology: https://hdl.handle.net/11296/3zh3g6