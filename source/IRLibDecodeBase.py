# IRLibCP by Chris Young. See copyright.txt and license.txt
# base class for decoding
import IRrecvPCI
import IRLibProtocols
PERCENT_TOLERANCE = 25/100
RCMARK=0
RCSPACE=1
RCERROR=3
def PERCENT_LOW(us):
	return int(us*(1.0-PERCENT_TOLERANCE))
def PERCENT_HIGH(us):
	return int(us*(1.0+PERCENT_TOLERANCE))
class IRLibDecodeBase:
	def __init__(self):
		self.ignoreHeader=False
		self.resetDecoder()
	def MATCH(self,v,e):
		return ((v>=PERCENT_LOW(e)) and (v<=PERCENT_HIGH(e)))
	def ABS_MATCH(self,v,e,t):
		return ( (v>=(e-t)) and (v<=(e+t)))
	def resetDecoder(self):
		self.protocolNum=IRLibProtocols.UNKNOWN
		self.value=0
		self.address=0
		self.bits=0
	def dumpResults(self, verbose=True):
		print("Decoded {} ({}): Value:{} Adrs: {} ({} bits)".format(IRLibProtocols.Pnames[self.protocolNum], repr(self.protocolNum),hex(self.value),hex(self.address), self.bits))
		if not verbose:
			return
		print("Raw samples({}):  Head: m{} s{}".format(len(IRrecvPCI.decodeBuffer),IRrecvPCI.decodeBuffer[0], IRrecvPCI.decodeBuffer[1]))
		for x in range(2,len(IRrecvPCI.decodeBuffer)):
			if x % 2:
				print("s{}".format(IRrecvPCI.decodeBuffer[x]),end=' ')
			else:
				print("{:2d}:m{}".format(x//2-1,IRrecvPCI.decodeBuffer[x]),end=' ')
			if (x % 2)==1:
				print(end='\t')
			if (x % 4)==1:
				print("\t",end=' ')
			if (x % 8)==1:
				print(" ")
			if (x % 32)==1:
				print()
		print()
	def decodeGeneric(self,expectedLength,headMark, headSpace, markData, spaceOne, spaceZero):
		self.resetDecoder()
		dataLow=0
		dataHigh=0
		Max=len(IRrecvPCI.decodeBuffer)-1
		if(expectedLength):
			if(len(IRrecvPCI.decodeBuffer)!=expectedLength):
				return False #RAW_COUNT_ERROR()
		if not self.ignoreHeader:
			if(headMark):
				if(not self.MATCH(IRrecvPCI.decodeBuffer[0],headMark)):
					return False #HEADER_MARK_ERROR(headMark)
		if(headSpace):
			if(not self.MATCH(IRrecvPCI.decodeBuffer[1],headSpace)):
				return False #HEADER_SPACE_ERpage andROR(headSpace)
		offset=2 
		while (offset< Max):
			if (not self.MATCH(IRrecvPCI.decodeBuffer[offset], markData)):
				return False #DATA_MARK_ERROR(markData)
			offset=offset+1
			if(self.MATCH(IRrecvPCI.decodeBuffer[offset], spaceOne)):
				dataLow= (dataLow<<1) | 1
			elif(self.MATCH (IRrecvPCI.decodeBuffer[offset], spaceZero)):
				dataLow= dataLow<<1
			else:
				return False #DATA_SPACE_ERROR(spaceZero)
			#print("Data={} offset={}".format(hex(data), offset))
			if offset>57:
				dataHigh= (dataHigh<<1) | (dataLow>>28)
				dataLow= dataLow & 0xfffffff
			offset= offset+1
		self.bits=(offset-1)//2
		self.value= dataLow
		self.address= dataHigh
		return True
	def RCLevel(self):
		if self.offset >= len(IRrecvPCI.decodeBuffer):
			return RCSPACE
		width=IRrecvPCI.decodeBuffer[self.offset]
		if self.offset % 2:
			val=RCSPACE
		else:
			val=RCMARK
		if self.MATCH (width, self.RCtime):
			avail = 1
		elif self.MATCH (width,2*self.RCtime):
			avail = 2
		elif self.MATCH (width,3*self.RCtime):
			avail = 3
		elif self.ignoreHeader and (self.offset==1) and (width<self.RCtime):
			avail = 1
		else:
			return RCERROR
		self.used= self.used+1
		if self.used>=avail:
			self.used=0
			self.offset=self.offset+1
		return val
		
#end of file
