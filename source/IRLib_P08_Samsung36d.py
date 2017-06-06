# IRLibCP by Chris Young. See copyright.txt and license.txt
# Samsung36 protocol. High order 16 bits in address.
# Remaining 20 bit in valu.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeSamsung36(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def getBits(self,lastOffset):
		while self.offset < lastOffset:
			if not self.MATCH(IRrecvPCI.decodeBuffer[self.offset], 500):
				return False #DATA_MARK_ERROR(500)
			self.offset=self.offset+1
			if self.MATCH(IRrecvPCI.decodeBuffer[self.offset], 1500):
				self.data=(self.data<<1) | 1
			elif self.MATCH(IRrecvPCI.decodeBuffer[self.offset], 500):
				self.data=self.data<<1
			else:
				return False #DATA_SPACE_ERROR(1500)
			self.offset=self.offset+1
		return True
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("Samsung36")
		if len(IRrecvPCI.decodeBuffer)!= 77:
			return False #RAW_COUNT_ERROR
		if not self.MATCH(IRrecvPCI.decodeBuffer[0],4500):
			return False #HEADER_MARK_ERROR (4500)
		if not self.MATCH(IRrecvPCI.decodeBuffer[1],4500):
			return False
		self.data=0
		self.offset=2
		if not IRdecodeSamsung36.getBits(self,33):
			return False
		if not self.MATCH(IRrecvPCI.decodeBuffer[self.offset], 500):
			return False
		self.offset=self.offset+1
		if not self.MATCH(IRrecvPCI.decodeBuffer[self.offset], 4500):
			return False
		self.offset=self.offset+1
		address= self.data
		self.data=0
		#12 bits into this segment the space is extended by 68 µs
		#so we adjust the value so it will match
		IRrecvPCI.decodeBuffer[61]=IRrecvPCI.decodeBuffer[62]- 68
		#now decode remain 20 bits
		if not IRdecodeSamsung36.getBits(self,76):
			#put back the value we fudged
			IRrecvPCI.decodeBuffer[61]=IRrecvPCI.decodeBuffer[62]+68
			return False 
		self.bits=36
		self.value=self.data
		self.address=address
		self.protocolNum=IRLibProtocols.SAMSUNG36
		return True
#end of file
