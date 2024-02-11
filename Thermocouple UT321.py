import hid
import time
from datetime import datetime
#import atexit
  

class UT321:
    def __init__(self):
        self.thermocoupleType={'0':'K', '1':'J', '2':'T', '3':'E'}
        self.units={'1':'C', '2':'F', '3':'K'}
        self.vid=0x1a86
        self.pid=0xe008
        try:
            self.dev=hid.Device(self.vid, self.pid)
            print(f'Device manufacturer: {self.dev.manufacturer}')
            print(f'Product: {self.dev.product}')
            startdata=bytearray(5)
            startdata=b"\x60\x09\x00\x00\x03"
            self.dev.send_feature_report(startdata)
            msg=bytearray(8)
            msg=b"\x02\x5A\x00\x00\x00\x00\x00\x00"
            self.dev.write(msg)
            msg=b"\x01\x01\x00\x00\x00\x00\x00\x00"
            self.dev.write(msg)
        except:
            print("Can't open device")
            self.dev=None
            
    def __del__(self):
        stopdata=b"\x60\x09\x00\x00\x03"
        self.dev.send_feature_report(stopdata)
        msg=bytearray(8)
        msg=b"\x01\x02\x00\x00\x00\x00\x00\x00"
        self.dev.write(msg)
        self.dev.__exit__()

        
    #the devise sends 8-byte sized packets, starting with 0xf0 for delimiting packets and with 0xf1 for data packets.
    #Each data packet contains one charachter (at least for temperature value). 19 data packets embraced by delimiting packets form useful data.
    #These data starts with "2:", followed by three characters for temperature value.
    #Have no idea, what happens for negative temperature (where does minus sign go?). Leaving it for later. 
    def get_temp(self):
        ret=[]
        if self.dev==None:
            return 'No device'
        temperature=''
        maxPackets=0
        frameStart=False
        while frameStart==False:
            
            try:
                if self.dev.read(8,500)[0]==240:       
                   if self.dev.read(8,500)[0]==240:
                       if self.dev.read(8,500)[0]==240:
                           firstDataMessage=self.dev.read(8,500)
                           if firstDataMessage[0]==241:
                               frameStart=True
                maxPackets+=1
            except:
                return('Cant read')
                break
            if maxPackets>50:
                print('Cant find frame start')
                break
            
        if frameStart==True:
                message=bytearray(19)
                message[0]=firstDataMessage[1]
                for packets in range(1,18):
                    message[packets]=self.dev.read(8,100)[1]

                for i in range(1,4):   
                    if (chr(message[i])==':'):
                        continue
                    if (chr(message[i])==';'):
                        temperature+='-'
                    else:
                        temperature+=chr(message[i])
                temperature+='.'
                temperature+=chr(message[4])
                ret.append(float(temperature))
                ret.append(self.units.get(chr(message[5])))
                ret.append(self.thermocoupleType.get(chr(message[8])))
               # print(message)
        return ret
        


#example use 

#device=UT321()
#while True:
 #   now = datetime.now()
  #  current_time = now.strftime("%H:%M:%S")
   # ut321_packet= device.get_temp()
    #print(current_time, ut321_packet)
    #time.sleep(5)

