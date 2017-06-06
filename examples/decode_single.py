# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sample program to decode one protocol in this case NEC
import board
import IRrecvPCI
import IRLib_P01_NECd

myReceiver=IRrecvPCI.IRrecvPCI(board.REMOTEIN)
myReceiver.enableIRIn() 
myDecoder=IRLib_P01_NECd.IRdecodeNEC()
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
