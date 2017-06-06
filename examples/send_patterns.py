# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sample program for sending test patterns of any protocol.
import board
import IRLibSendBase
import IRLibProtocols
import IRLib_P01_NECs
import IRLib_P02_Sonys
import IRLib_P03_RC5s
import IRLib_P04_RC6s
import IRLib_P05_Panasonic_Olds
import IRLib_P06_JVCs
import IRLib_P07_NECxs
import IRLib_P08_Samsung36s
import IRLib_P09_GICables
import IRLib_P10_DirecTVs
import IRLib_P11_RCMMs

class MySendClass (IRLibSendBase.IRLibSendBase):
	def __init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self,protocolNum, data, data2=0,kHz=38):
		if kHz==0:
			kHz=38
		if protocolNum==IRLibProtocols.NEC:
			print("Sending NEC value:{} address:{} kHz:{}".format(hex(data),hex(data2),kHz))
			IRLib_P01_NECs.IRsendNEC.send(self,data,data2,kHz)
		elif protocolNum==IRLibProtocols.SONY:
			print("Sending Sony value:{} bits:{}".format(hex(data),data2))
			IRLib_P02_Sonys.IRsendSony.send(self,data,data2)
		elif protocolNum==IRLibProtocols.RC5:
			print("Sending RC5 value:{} bits:{} kHz: {}".format(hex(data),data2,kHz))
			IRLib_P03_RC5s.IRsendRC5.send(self,data,data2)
		elif protocolNum==IRLibProtocols.RC6:
			print("Sending RC6 value:{} address:{} bits:{}".format(hex(data),hex(data2),kHz))
			IRLib_P04_RC6s.IRsendRC6.send(self,data,data2,kHz)
		elif protocolNum==IRLibProtocols.PANASONIC_OLD:
			print("Sending Panasonic_Old value:{}".format(hex(data)))
			IRLib_P05_Panasonic_Olds.IRsendPanasonic_Old.send(self,data)
		elif protocolNum==IRLibProtocols.JVC:
			print("Sending JVC value:{} First:{}".format(hex(data), data2))
			IRLib_P06_JVCs.IRsendJVC.send(self,data, data2)
		elif protocolNum==IRLibProtocols.NECX:
			print("Sending NECx value:{} address:{}".format(hex(data),hex(data2)))
			IRLib_P07_NECxs.IRsendNECx.send(self,data,data2)
		elif protocolNum==IRLibProtocols.SAMSUNG36:
			print("Sending Samsung36 value:{} address:{}".format(hex(data),hex(data2)))
			IRLib_P08_Samsung36s.IRsendSamsung36.send(self,data,data2)
		elif protocolNum==IRLibProtocols.GICABLE:
			print("Sending G.I.Cable value:{}".format(hex(data)))
			IRLib_P09_GICables.IRsendGICable.send(self,data)
		elif protocolNum==IRLibProtocols.DIRECTV:
			print("Sending DirecTV value:{} repeat:{} kHz:{}".format(hex(data), data2,kHz))
			IRLib_P10_DirecTVs.IRsendDirecTV.send(self,data, data2,kHz)
		elif protocolNum==IRLibProtocols.RCMM:
			print("Sending RCMM value:{} address:{} bits:{}".format(hex(data),hex(data2),kHz))
			IRLib_P11_RCMMs.IRsendRCMM.send(self,data, data2,kHz)
	
#end of MySendClass
def	SendTest(protocol):
	if protocol==IRLibProtocols.NEC:
		mySend.send(protocol,0x00ff00f,0xf)
		mySend.send(protocol,-1,0)
		mySend.send(protocol,0x1234567,0xf, 40)
	elif protocol==IRLibProtocols.SONY:
		mySend.send(protocol,0x12,8)
		mySend.send(protocol,0x123,12)
		mySend.send(protocol,0x1234,15)
		mySend.send(protocol,0x12345,20)
	elif protocol==IRLibProtocols.RC5:
		mySend.send(protocol,0xffff,13)
		mySend.send(protocol,0xffff,14)
		mySend.send(protocol,0xffff,14,57)
	elif protocol==IRLibProtocols.RC6:
		mySend.send(protocol,0x12345,0,20)
		mySend.send(protocol,0x123456,0,24)
		mySend.send(protocol,0x1234567,0,28)
		mySend.send(protocol,0x2345678,0x1,32)
	elif protocol==IRLibProtocols.PANASONIC_OLD:
		mySend.send(protocol,0x37c906)
	elif protocol==IRLibProtocols.JVC:
		mySend.send(protocol,0x1234, True)
		mySend.send(protocol,0x1234, False)
	elif protocol==IRLibProtocols.NECX:
		mySend.send(protocol,0x00ff00f,0xf)
		mySend.send(protocol,-1,0)
	elif protocol==IRLibProtocols.SAMSUNG36:
		mySend.send(protocol,0x56789,0x1234)
	elif protocol==IRLibProtocols.GICABLE:
		mySend.send(protocol,0x1234)
		mySend.send(protocol,-1,0)
	elif protocol==IRLibProtocols.DIRECTV:
		mySend.send(protocol,0x1234, True)
		mySend.send(protocol,0x1234, False,40)
	elif protocol==IRLibProtocols.RCMM:
		mySend.send(protocol,0x123, 0,12)
		mySend.send(protocol,0x123456, 0,24)
		mySend.send(protocol,0x2345678,0x1,32)
#end of SendTest

mySend=MySendClass(board.REMOTEOUT)
#Test=IRLibProtocols.NEC
Test=-1
if Test<0:
	for i in range(IRLibProtocols.RCMM+1):
		SendTest(i)
else:
	SendTest(Test)
	
