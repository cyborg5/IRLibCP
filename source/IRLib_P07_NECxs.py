# IRLibCP by Chris Young. See copyright.txt and license.txt
# NECx protocol.  Similar to NEC but different timing.
# High order 4 bits in address. 28 low order bits in data.
# Use data=-1 as repeat code.
import IRLibSendBase
class IRsendNECx(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, address):
		if data==-1:
			self.enableIROut(38)
			self.mark(4500)
			self.space(4500)
			self.mark(564)
			self.space(564)
			self.mark(564)
			self.space(32767)#should be  97572
			self.transmit()
		else:
			self.sendGeneric(data, address, 32,4500, 4500, 564, 564, 1692, 564,38,True)	

#end of file
