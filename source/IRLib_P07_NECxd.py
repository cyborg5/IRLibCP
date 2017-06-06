# IRLibCP by Chris Young. See copyright.txt and license.txt
# NECx protocol.  Similar to NEC but different timing.
# High order 4 bits in address. 28 low order bits in value.
# returns value=-1 as repeat code.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeNECx(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("NECx repeat")
		if len(IRrecvPCI.decodeBuffer)==5 \
		and self.MATCH(IRrecvPCI.decodeBuffer[0],4500)\
		and self.MATCH(IRrecvPCI.decodeBuffer[1],4500)\
		and self.MATCH(IRrecvPCI.decodeBuffer[2], 564)\
		and self.MATCH(IRrecvPCI.decodeBuffer[4], 564):
			self.bits=0
			self.value=-1
			self.protocolNum=IRLibDecodeBase.NECX
			return True
		#IRLIB_ATTEMPT_MESSAGE("NEC")
		if (not self.decodeGeneric(67,4500,4500, 564, 1692, 564)):
			return False
		self.protocolNum=IRLibProtocols.NECX
		return True
#end of file
