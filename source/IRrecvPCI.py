# IRLibCP by Chris Young. See copyright.txt and license.txt
# receives raw signals using pin change interrupts and pulseio
import board
import pulseio
import array
import time
class IRrecvPCI:
	def __init__(self, pin):
		self.recvPin = pin
		self.markExcess= 50
	
	def enableIRIn(self):
		self.recvBuffer = pulseio.PulseIn(self.recvPin, maxlen=150, idle_state=True)
		self.prevLength=0
		
	def getResults(self):
		global decodeBuffer
		if not len(self.recvBuffer):
			return False
		# if the buffer got longer, record the time and come back later
		if len(self.recvBuffer) > self.prevLength: 
			self.prevLength=len(self.recvBuffer)
			self.lastTime=time.monotonic()
			return False
		# the length is nonzero and equal to previous length
		# if we have been stuck at this length for half a second, presume we're done

		# it's been long enough we presume were done
		if(time.monotonic()-self.lastTime) > 0.5:
			self.recvBuffer.pause()
			decodeBuffer = array.array('H')
			for x in range(len(self.recvBuffer)):
				if self.recvBuffer[x] > 10000: #truncate list if necessary
					#print("Truncated at:{}".format(x))
					break
				decodeBuffer.append(self.recvBuffer[x]+\
				( self.markExcess if (x % 2) else (-self.markExcess)))
			# Everything is saved in the decode buffer
			# get rid of the receiver so we can reenable later using call to receiver.enableIRIn()
			self.prevLength=0
			self.recvBuffer.deinit() 
			return True
		else:
			# Here although length hasn't changed, let's wait a bit
			return False
		
		
		
				
	

