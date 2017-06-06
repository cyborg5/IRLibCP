# IRLibCP by Chris Young. See copyright.txt and license.txt
# G.I.Cable protocol. Use data=-1 as repeat code.
import IRLibSendBase
class IRsendGICable(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data):
		if data==-1:
			self.enableIROut(39)
			self.mark(8820)
			self.space(2205)
			self.mark(490)
			self.space(87220)
			self.transmit()
		else:
			self.sendGeneric(data,0,16,8820,4410,490,490,4410,2205,39,True)	
#end of file
