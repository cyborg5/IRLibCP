# IRLibCP by Chris Young. See copyright.txt and license.txt
# Panasonic_Old protocol. 22 bits in data. No variations.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodePanasonic_Old(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("Panasonic_Old")
		if (not self.decodeGeneric(47,3332,3332,833,2499,833)):
			return False
		self.protocolNum=IRLibProtocols.PANASONIC_OLD
		return True
#end of file
