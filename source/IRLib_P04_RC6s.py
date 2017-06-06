# IRLibCP by Chris Young. See copyright.txt and license.txt
# RC6 protocol. Varieties 16, 20, 24, 32 however we encode
# as 20, 24, 28, 32 respectively. See documentation.
# High order 4 bits in address. Low order 28 bits in data.
import IRLibSendBase
class IRsendRC6(IRLibSendBase.IRLibSendBase):
#Varieties include 20, 24, 28, and 36
#We encode 36 as 32 with a fixed OEM value
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def sendRC6Bits(self, data, numBits, first):
		data=data&((2**numBits)-1)
		data=data<<(28-numBits)
		for i in range(numBits):
			if first and (i==3):
				t=888
			else:
				t=444
			if data & 0x8000000:
				self.mark(t)
				self.space(t)
			else:
				self.space(t)
				self.mark(t)
			data= (data<<1) &0x0fffffff
	def send(self, data, address, numBits=20):
		self.enableIROut(36)
		if numBits==0:
			numBits=13
		self.mark(2666)#header
		self.space(889)
		self.mark(444) #start bit
		self.space(444)
		sendTrailer=True
		if numBits==32:
			address= address+0xc0
			IRsendRC6.sendRC6Bits(self,address,8, sendTrailer)
			sendTrailer=False
			numBits= 28 #remaining bits after init 8
		IRsendRC6.sendRC6Bits(self,data,numBits,sendTrailer)
		self.space(107000-self.extent)
		self.transmit()
#end of file
