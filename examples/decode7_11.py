# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sample program to decode multiple protocols.
# Specifically protocols 7 through 11
import board
import IRLibProtocols
import IRLibDecodeBase
import IRLib_P07_NECxd
import IRLib_P08_Samsung36d
import IRLib_P09_GICabled
import IRLib_P10_DirecTVd
import IRLib_P11_RCMMd
import IRrecvPCI


class MyDecodeClass(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def  decode(self):
		if IRLib_P07_NECxd.IRdecodeNECx.decode(self):
			return True
		elif IRLib_P08_Samsung36d.IRdecodeSamsung36.decode(self):
			return True
		elif IRLib_P09_GICabled.IRdecodeGICable.decode(self):
			return True
		elif IRLib_P10_DirecTVd.IRdecodeDirecTV.decode(self):
			return True
		elif IRLib_P11_RCMMd.IRdecodeRCMM.decode(self):
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
