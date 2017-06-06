# IRLibCP by Chris Young. See copyright.txt and license.txt
# JVC protocol.  First frame should have "first=True" and will
# automatically send additional repeat frame. Subsequent repeat
# frames can be sent with first=False
import IRLibSendBase
class IRsendJVC(IRLibSendBase.IRLibSendBase):
	def	__init__(self,outPin):
		IRLibSendBase.IRLibSendBase.__init__(self,outPin)
	def send(self, data, first=True):
		self.sendGeneric(data, 0,16,(8400 if first else 0),\
		(4200 if first else 0),525,525,1575,525,38,True)	
		self.space(23625)
		if first:
			self.sendGeneric(data, 0,16,0,0,525,525,1575,525,38,True)	
			self.space(23625)

#end of file
