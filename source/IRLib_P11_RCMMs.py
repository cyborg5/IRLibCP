# IRLibCP by Chris Young. See copyright.txt and license.txt
# RCMM protocol a.k.a. Nokia and AT&T U-Verse
# Varieties are 12, 24, or 32 bits. Specify address=0 if 12 or
# 24-bit varieties.
import IRLibSendBase
class IRsendRCMM(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def sendRCMMBits(self, data,  bits):
		data=data&((2**bits)-1)
		data=data<<(28-bits)
		for i in range(bits//2):
			self.mark(167)
			switch=data>>26
			if switch==0:
				self.space(278)
			elif switch==1:
				self.space(444)
			elif switch==2:
				self.space(611)
			else:
				self.space(778)
			data=(data<<2)&0x0fffffff
	def send(self, data, address,bits=12):
		self.enableIROut(36)
		if bits==0:
			bits=12
		self.extent=0
		self.mark(417)
		self.space(278)
		if bits> 28:
			IRsendRCMM.sendRCMMBits(self,address,4)
			bits=28
		IRsendRCMM.sendRCMMBits(self,data,bits)
		self.mark(167)
		self.space(27778-self.extent)
		self.transmit()
#end of file
