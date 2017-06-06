# IRLibCP by Chris Young. See copyright.txt and license.txt
# NEC protocol. High order 4 bits are address, low order 28 bits
# are data. Optional third parameter allows alternate frequency 40.
# Use data= -1 as repeat code.
import IRLibSendBase
class IRsendNEC(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, address=0,kHz=38):
		if data==-1:
			self.enableIROut(kHz)
			self.mark(9000)
			self.space(2256)
			self.mark(564)
			self.space(32767)#should be  97572
			self.transmit()
		else:
			self.sendGeneric(data, address, 32, 9000, 4500, 564, 564, 1692, 564,kHz,True,108000)	

#end of file
