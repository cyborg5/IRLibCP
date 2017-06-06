# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sample program to decode multiple protocols.
# In this case NEC, Sony and RC5
import board
import IRLibDecodeBase
import IRLib_P01_NECd
import IRLib_P02_Sonyd
import IRLib_P03_RC5d
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
		else:
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
