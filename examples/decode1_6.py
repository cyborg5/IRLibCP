# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sample program to decode multiple protocols.
# Specifically protocols 1 through 6
import board
import IRLibProtocols
import IRLibDecodeBase
import IRLib_P01_NECd
import IRLib_P02_Sonyd
import IRLib_P03_RC5d
import IRLib_P04_RC6d
import IRLib_P05_Panasonic_Oldd
import IRLib_P06_JVCd
import IRrecvPCI


class MyDecodeClass(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def  decode(self):
		if IRLib_P01_NECd.IRdecodeNEC.decode(self): 
			return True
		if IRLib_P02_Sonyd.IRdecodeSony.decode(self):
			return True
		elif IRLib_P03_RC5d.IRdecodeRC5.decode(self):
			return True
		elif IRLib_P04_RC6d.IRdecodeRC6.decode(self):
			return True
		elif IRLib_P05_Panasonic_Oldd.IRdecodePanasonic_Old.decode(self):
			return True
		elif IRLib_P06_JVCd.IRdecodeJVC.decode(self):
			return True
		return False

myDecoder=MyDecodeClass()
myReceiver=IRrecvPCI.IRrecvPCI(board.REMOTEIN)
myReceiver.enableIRIn() 
print("send a signal")
while True:
	while (not myReceiver.getResults()):
		pass
	if myDecoder.decode():
		print("success")
	else:
		print("failed")
	myDecoder.dumpResults(True)
	myReceiver.enableIRIn() 
