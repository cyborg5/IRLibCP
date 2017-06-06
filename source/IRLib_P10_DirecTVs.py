# IRLibCP by Chris Young. See copyright.txt and license.txt
# DirecTV protocol. Six varieties uses frequencies of 38, 40, 
# or 57 and a lead out time that is short or long depending on
# boolean value self.longLeadOut. Second parameter is true for
# first frame and false for repeat frames.
import IRLibSendBase
class IRsendDirecTV(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, first=True,kHz=38):
		data=data&((2**16)-1)
		self.enableIROut(kHz)
		self.mark(6000 if first else 3000)
		self.space(1200)
		for i in range(8):
			if data & 0x8000:
				self.mark(1200)
			else:
				self.mark(600)
			data=(data<<1) & 0xffff
			if data & 0x8000:
				self.space(1200)
			else:
				self.space(600)
			data=(data<<1) & 0xffff
		self.mark(600) 
		self.space(30000 if self.longLeadOut else 9000)
		self.transmit()
#end of file
