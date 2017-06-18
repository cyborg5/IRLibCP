# IRLibCP by Chris Young. See copyright.txt and license.txt
# G.I.Cable protocol. Returns value=-1 as repeat code.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeGICable(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("G.I. cut cable Repeat")
		if len(IRrecvPCI.decodeBuffer)==3\
		and self.MATCH(IRrecvPCI.decodeBuffer[0],8820)\
		and self.MATCH(IRrecvPCI.decodeBuffer[1],2205)\
		and self.MATCH(IRrecvPCI.decodeBuffer[2], 490):
			self.bits=0
			self.value=-1
			self.protocolNum=IRLibProtocols.GICABLE
			return True
		if (not self.decodeGeneric(35,8820,4410,490,4410,2205)):
			return False
		self.protocolNum=IRLibProtocols.GICABLE
		return True
#end of file
