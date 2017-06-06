# IRLibCP by Chris Young. See copyright.txt and license.txt
# NEC protocol. High order 4 bits are address, low order 28 bits
# are value. Optional third parameter allows alternate frequency 40.
# Returns value=-1 as repeat code.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeNEC(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("NEC repeat")
		if len(IRrecvPCI.decodeBuffer)==3\
		and self.MATCH(IRrecvPCI.decodeBuffer[0], 9000)\
		and self.MATCH(IRrecvPCI.decodeBuffer[1], 2256)\
		and self.MATCH(IRrecvPCI.decodeBuffer[2], 564):
			self.bits=0
			self.value=-1
			self.protocolNum=IRLibProtocols.NEC
			return True
		#IRLIB_ATTEMPT_MESSAGE("NEC")
		if (not self.decodeGeneric(67, 9000, 4500, 564, 1692, 564)):
			return False
		self.protocolNum=IRLibProtocols.NEC
		return True
#end of file
