# IRLibCP by Chris Young. See copyright.txt and license.txt
# RC5 protocol.  Default 13 bits and 36 kHz. Varieties include
# 14 bit 36 kHz and 14 bit 57 kHz.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeRC5(IRLibDecodeBase.IRLibDecodeBase):
	def decode(self):
		#IRLIB_ATTEMPT_MESSAGE ("RC5")
		self.resetDecoder()
		if len(IRrecvPCI.decodeBuffer)<13:
			return False #RAW_COUNT_ERROR
		self.offset=0
		data=0
		self.used=0
		self.RCtime=889
		if self.RCLevel() != IRLibDecodeBase.RCMARK:
			return False #HEADER_MARK_ERROR(self.RCtime)
		n=0
		while self.offset < len(IRrecvPCI.decodeBuffer):
			levelA=self.RCLevel()
			levelB=self.RCLevel()
			if (levelA==IRLibDecodeBase.RCSPACE) and (levelB==IRLibDecodeBase.RCMARK):
				data=(data<<1) | 1
			elif (levelA==IRLibDecodeBase.RCMARK) and (levelB==IRLibDecodeBase.RCSPACE):
				data=data<<1
			else:
				return False #DATA_MARK_ERROR(self.RCtime)
			n=n+1
		self.bits=n
		self.value=data
		self.protocolNum=IRLibProtocols.RC5
		return  True
		
#end of file
