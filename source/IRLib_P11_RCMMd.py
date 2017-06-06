# IRLibCP by Chris Young. See copyright.txt and license.txt
# RCMM protocol a.k.a. Nokia and AT&T U-Verse
# Varieties are 12, 24, or 32 bits. Specify address=0 if 12 or
# 24-bit varieties.
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
RCMM_TOLERANCE= 80
class IRdecodeRCMM(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("RCMM")
		if len(IRrecvPCI.decodeBuffer) != 15\
		and len(IRrecvPCI.decodeBuffer) != 27\
		and len(IRrecvPCI.decodeBuffer) != 35:
			return False #RAW_COUNT_ERROR
		if not self.ignoreHeader:
			if not self.MATCH(IRrecvPCI.decodeBuffer[0],417):
				return False #HEADER_MARK_ERROR(417)
		if not self.MATCH(IRrecvPCI.decodeBuffer[1],278):
				return False #HEADER_MARK_ERROR(278)
		dataLow=0
		dataHigh=0
		offset=2
		while offset < (len(IRrecvPCI.decodeBuffer)-1):
			if not self.ABS_MATCH(IRrecvPCI.decodeBuffer[offset],167,RCMM_TOLERANCE):
				print("Data Mark error. Offset", offset)
				return False #DATA_MARK_ERROR(167)
			offset=offset+1
			if self.ABS_MATCH(IRrecvPCI.decodeBuffer[offset],278,RCMM_TOLERANCE):
				dataLow= dataLow<<2 #logical "0"
			elif self.ABS_MATCH(IRrecvPCI.decodeBuffer[offset],444,RCMM_TOLERANCE):
				dataLow= (dataLow<<2) + 1 #logical "1"
			elif self.ABS_MATCH(IRrecvPCI.decodeBuffer[offset],611,RCMM_TOLERANCE):
				dataLow= (dataLow<<2) + 2 #logical "2"
			elif self.ABS_MATCH(IRrecvPCI.decodeBuffer[offset],778,RCMM_TOLERANCE):
				dataLow= (dataLow<<2) + 3 #logical "3"
			else:
				return False #DATA_MARK_ERROR(1200)
			if offset>30:
				dataHigh= (dataHigh<<2) | (dataLow>>28)
				dataLow= dataLow & 0xfffffff
			offset=offset+1
		if not self.MATCH(IRrecvPCI.decodeBuffer[offset],167):
			return False #DATA_MARK_ERROR(1200)
		self.bits= len(IRrecvPCI.decodeBuffer)-3
		self.value= dataLow
		self.address=  dataHigh
		self.protocolNum=IRLibProtocols.RCMM
		return True
#end of file
