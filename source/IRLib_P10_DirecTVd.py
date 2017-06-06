# IRLibCP by Chris Young. See copyright.txt and license.txt
# DirecTV protocol. Six varieties uses frequencies of 38, 40, 
# or 57 and a lead out time that is short or long depending on
# boolean value self.longLeadOut. Address value is true for
# first frame and false for repeat frames.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeDirecTV(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("DirecTV")
		if len(IRrecvPCI.decodeBuffer) != 19:
			return False #RAW_COUNT_ERROR
		#use address value as repeat flag
		if not self.ignoreHeader:
			if self.MATCH(IRrecvPCI.decodeBuffer[0], 3000):
				address=False
			elif not self.MATCH(IRrecvPCI.decodeBuffer[0], 6000):
				return False #HEADER_MARK_ERROR(6000)
			else:
				address= True
		if not self.MATCH(IRrecvPCI.decodeBuffer[1],1200):
			return False #HEADER_SPACE_ERROR(1200)
		data=0
		offset=2
		while offset < 17:
			if self.MATCH(IRrecvPCI.decodeBuffer[offset],1200):
				data= (data<<1) | 1
			elif self.MATCH(IRrecvPCI.decodeBuffer[offset],600):
				data= data<<1
			else:
				return False #DATA_MARK_ERROR(1200)
			offset=offset+1
			if self.MATCH(IRrecvPCI.decodeBuffer[offset], 1200):
				data= (data<<1) | 1
			elif self.MATCH(IRrecvPCI.decodeBuffer[offset], 600):
				data= data<<1
			else:
				return False #DATA_SPACE_ERROR(1200)
			offset=offset+1
		self.bits= 16
		self.value= data
		self.address= address
		self.protocolNum=IRLibProtocols.DIRECTV
		return True
#end of file
