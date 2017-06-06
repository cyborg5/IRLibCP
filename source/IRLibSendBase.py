# IRLibCP by Chris Young. See copyright.txt and license.txt
# base class for sending
import board
import pulseio
import array
import time
import IRLibProtocols
class IRLibSendBase:
	def __init__(self,outPin):
		self.outPin= outPin
		self.longLeadOut=True #used by DirecTV only
	def enableIROut(self,kHz):
		self.extent=0
		self.irPWM= pulseio.PWMOut(self.outPin, frequency=kHz*1000, duty_cycle=0)
		self.irSend= pulseio.PulseOut(self.irPWM)
		self.irPWM.duty_cycle=(2**16)//3
		self.sendBuffer= array.array('H')
		time.sleep(0.4)
	def mark(self,usec):
		self.extent=self.extent+1
		last=len(self.sendBuffer)
		if last % 2:
#			print("Adding value to mark")
			self.sendBuffer[last-1]= usec+self.sendBuffer[last-1]
		else:
			self.sendBuffer.append(usec)
	def space(self,usec):
		self.extent=self.extent+1
		last=len(self.sendBuffer)
		if (last % 2)==0:
#			print("Adding value to space")
			self.sendBuffer[last-1]= usec+self.sendBuffer[last-1]
		else:
			self.sendBuffer.append(usec)
	def sendBits(self,data,numBits,markOne,markZero,spaceOne, spaceZero):
		#print("SendBits data:{} bits:{}".format(hex(data),numBits))
		data=data&((2**numBits)-1)
		data=data<<(28-numBits)
		for i in range(numBits):
			if data & 0x8000000:
				self.mark(markOne)
				self.space(spaceOne)
			else:
				self.mark(markZero)
				self.space(spaceZero)
			data= (data<<1) &0x0fffffff
	def transmit(self):
		#print(self.sendBuffer)
		self.irSend.send(self.sendBuffer)
		self.irPWM.duty_cycle=0
		time.sleep(0.5)
		self.irPWM.deinit()
	def sendGeneric(self,value, address,numBits, headMark, headSpace,\
	markOne, markZero,spaceOne,spaceZero,kHz, useStop, maxExtent=0):
		self.enableIROut(kHz)
		if headMark:
			self.mark(headMark)
		if headSpace:
			self.space(headSpace)
		if numBits> 28:
			self.sendBits(address,numBits-28, markOne, markZero, spaceOne, spaceZero)
			numBits=28
		self.sendBits(value,numBits, markOne,markZero,spaceOne, spaceZero)
		if useStop:
			self.mark(markOne)
		if maxExtent:
			self.space(maxExtent-self.extent)
		else:
			self.space(spaceOne)
		self.transmit()
