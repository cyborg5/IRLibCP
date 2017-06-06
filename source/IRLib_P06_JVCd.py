# IRLibCP by Chris Young. See copyright.txt and license.txt
# JVC protocol.  If first frame received address==True
#  Repeat frames address==False
import IRrecvPCI
import IRLibDecodeBase
import IRLibProtocols
class IRdecodeJVC(IRLibDecodeBase.IRLibDecodeBase):
	def __init__(self):
		IRLibDecodeBase.IRLibDecodeBase.__init__(self)
	def decode(self):
		self.resetDecoder()
		#IRLIB_ATTEMPT_MESSAGE("JVC")
		if not self.decodeGeneric(35,8400,4200,525,1575,525):
			#IRLIB_ATTEMPT_MESSAGE ("JVC Repeat")
			if len(IRrecvPCI.decodeBuffer) != 33:
				return False #RAW_COUNT_ERROR
			if not self.decodeGeneric(0,525,0,525,1575,525):
				return False  #JVC repeat failed generic
			#if this is a repeat then decode Generic
			#fails to add the most significant bit
			if self.MATCH(IRrecvPCI.decodeBuffer[1],1575):
				self.address=self.address+0x8000
			elif not self.MATCH(IRrecvPCI.decodeBuffer[1],525):
				return False #DATA_SPACE_ERROR
			self.bits= self.bits+1
			self.value=self.address				
		self.address= len(IRrecvPCI.decodeBuffer)== 35
		self.protocolNum=IRLibProtocols.JVC
		return True
#end of file
