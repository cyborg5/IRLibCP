# IRLibCP by Chris Young. See copyright.txt and license.txt
# RC6 protocol. Varieties 16, 20, 24, 32 however we encode
# as 20, 24, 28, 32 respectively. See documentation.
# High order 4 bits in address. Low order 28 bits in data.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeRC6(IRLibDecodeBase.IRLibDecodeBase):
	def decode(self):
		#IRLIB_ATTEMPT_MESSAGE ("RC5")
		self.resetDecoder()
		if (len(IRrecvPCI.decodeBuffer)<23) or \
		(len(IRrecvPCI.decodeBuffer)>77):
			return False #RAW_COUNT_ERROR
		if not self.ignoreHeader:
			if not self.MATCH(IRrecvPCI.decodeBuffer[0],2666):
				return False #HEADER_MARK_ERROR(2666)
		if not self.MATCH(IRrecvPCI.decodeBuffer [1],889):
			return False  #HEADER_SPACE_ERROR(889)
		self.offset=2
		dataLow=0
		dataHigh=0
		self.used=0
		self.RCtime=444
		#Get start bit (1)
		if self.RCLevel() != IRLibDecodeBase.RCMARK:
			return False #DATA_MARK_ERROR(self.RCtime)
		if self.RCLevel() != IRLibDecodeBase.RCSPACE:
			return False #DATA_SPACE_ERROR(self.RCtime)
		n=0
		while self.offset < len(IRrecvPCI.decodeBuffer):
			levelA=self.RCLevel()
			if n==3:
				#T bit is double wide, make sure second half matches
				if levelA != self.RCLevel():
					return False #TRAILER_BIT_ERROR
			levelB=self.RCLevel()
			if n==3:
				if levelB != self.RCLevel():
					return  False #TRAILER_BIT_ERROR
			if (levelA==IRLibDecodeBase.RCMARK) and (levelB==IRLibDecodeBase.RCSPACE):#backwards from RC5
				dataLow=(dataLow<<1)|1
			elif (levelA==IRLibDecodeBase.RCSPACE) and (levelB==IRLibDecodeBase.RCMARK):
				dataLow=dataLow<<1
			else:
				return False #DATA_MARK_ERROR(self.RCtime)
			if n>27:
				dataHigh=(dataHigh<<1) | (dataLow>>28)
				dataLow= dataLow & 0xfffffff
			n=n+1
		if n== 36:
			n= 32#OEM and trailer bits discarded in 32 bit version
			dataHigh= dataHigh & 0xf
		self.bits=n
		self.address=dataHigh
		self.value= dataLow
		self.protocolNum=IRLibProtocols.RC6
		return  True
		
#end of file
