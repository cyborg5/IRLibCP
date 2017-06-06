# IRLibCP by Chris Young. See copyright.txt and license.txt
# RC5 protocol.  Default 13 bits and 36 kHz. Varieties include
# 14 bit 36 kHz and 14 bit 57 kHz.
import IRLibSendBase
class IRsendRC5(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, numBits=13,kHz=36):
		if numBits==0:
			numBits=13
		if kHz==0:
			kHz=36
		data=data&((2**numBits)-1)
		data=data<<(28-numBits)
		self.enableIROut(kHz)
		self.mark(889)
		for i in range(numBits):
			if data & 0x8000000:
				self.space(889)
				self.mark(889)
			else:
				self.mark(889)
				self.space(889)
			data= (data<<1) &0x0fffffff
		self.space(114000-self.extent)
		self.transmit()
#end of file
