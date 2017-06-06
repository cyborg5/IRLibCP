# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sony protocol. Varieties are 8, 12, 15, or 20 bits.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeSony(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		data=0
		#IRLIB_ATTEMPT_MESSAGE("Sony")
		if len(IRrecvPCI.decodeBuffer) != 17\
		and len(IRrecvPCI.decodeBuffer)!= 25\
		and len(IRrecvPCI.decodeBuffer)!= 31\
		and len(IRrecvPCI.decodeBuffer)!= 41:
			return False #RAW_COUNT_ERROR
		if not self.ignoreHeader:
			if not self.MATCH(IRrecvPCI.decodeBuffer[0], 2400):
				return False #HEADER_MARK_ERROR(2400)
		offset=1
		while offset < len(IRrecvPCI.decodeBuffer):
			if  not self.MATCH(IRrecvPCI.decodeBuffer[offset], 600):
				return False #DATA_SPACE_ERROR(600)
			offset=offset+1
			if self.MATCH(IRrecvPCI.decodeBuffer[offset], 1200):
				data= (data<<1) | 1
			elif self.MATCH(IRrecvPCI.decodeBuffer[offset], 600):
				data= data<<1
			else:
				return False #DATA_MARK_ERROR (600)
			offset=offset+1
		self.bits= (offset-1)//2
		self.value= data
		self.protocolNum=IRLibProtocols.SONY
		return True
#end of file
