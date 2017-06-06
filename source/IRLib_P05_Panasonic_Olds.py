# IRLibCP by Chris Young. See copyright.txt and license.txt
# Panasonic_Old protocol. 22 bits in data. No variations.
import IRLibSendBase
class IRsendPanasonic_Old(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data):
		self.sendGeneric(data, 0,22,3332,3332,833,833,2499,833,57,True)	

#end of file
