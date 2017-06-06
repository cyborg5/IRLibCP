# IRLibCP by Chris Young. See copyright.txt and license.txt
# Samsung36 protocol. High order 16 bits in address.
# Remaining 20 bit in data.
import IRLibSendBase
class IRsendSamsung36(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, address):
		self.enableIROut(38)
		self.mark(4500)
		self.space(4500)
		self.sendBits(address,16,500,500,1500,500)
		self.mark(500)
		self.space(4500)
		self.sendBits(data>>8,12,500,500,1500,500)
		self.space(68)
		self.sendBits(data,8,500,500,1500,500)
		self.mark(500)
		self.space(59000) #should be 59000
		self.transmit()

#end of file
