# IRLibCP by Chris Young. See copyright.txt and license.txt
# Sony protocol. Varieties are 8, 12, 15, or 20 bits.
# Automatically sends each frame 3 times according to rule for protocol
import IRLibSendBase
class IRsendSony(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, bits):
		for i in range(3):
			self.sendGeneric(data, 0, bits, 2400,600,1200,600,600,600,40,False,45000)	

#end of file
