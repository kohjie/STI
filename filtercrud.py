#!/usr/bin/python

import sys, posix, time, md5, binascii, socket, select

class ApiRos:
    "Routeros api"
    def __init__(self, sk):
        self.sk = sk
        self.currenttag = 0
        
    def login(self, username, pwd):
        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify(attrs['=ret'])
        md = md5.new()
        md.update('\x00')
        md.update(pwd)
        md.update(chal)
        self.talk(["/login", "=name=" + username,
                   "=response=00" + binascii.hexlify(md.digest())])
       
    def talk(self, words):
        if self.writeSentence(words) == 0: return
        r = []
        while 1:
            i = self.readSentence();
            if len(i) == 0: continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if (j == -1):
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j+1:]
            r.append((reply, attrs))
            if reply == '!done': return r

    def writeSentence(self, words):
        ret = 0
        for w in words:
            self.writeWord(w)
            ret += 1
        self.writeWord('')
        return ret

    def readSentence(self):
        r = []
        while 1:
            w = self.readWord()
            if w == '': return r
            r.append(w)
            
    def writeWord(self, w):
        print "<<< " + w
        self.writeLen(len(w))
        self.writeStr(w)

    def readWord(self):
        ret = self.readStr(self.readLen())
        print ">>> " + ret
        return ret

    def writeLen(self, l):
        if l < 0x80:
            self.writeStr(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x10000000:        
            l |= 0xE0000000         
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        else:                       
            self.writeStr(chr(0xF0))
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))

    def readLen(self):              
        c = ord(self.readStr(1))    
        if (c & 0x80) == 0x00:      
            pass                    
        elif (c & 0xC0) == 0x80:    
            c &= ~0xC0              
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xE0) == 0xC0:    
            c &= ~0xE0              
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xF0) == 0xE0:    
            c &= ~0xF0              
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xF8) == 0xF0:    
            c = ord(self.readStr(1))     
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        return c                    

    def writeStr(self, str):        
        n = 0;                      
        while n < len(str):         
            r = self.sk.send(str[n:])
            if r == 0: raise RuntimeError, "connection closed by remote end"
            n += r                  

    def readStr(self, length):      
        ret = ''                    
        while len(ret) < length:    
            s = self.sk.recv(length - len(ret))
            if s == '': raise RuntimeError, "connection closed by remote end"
            ret += s
        return ret

    def createRule(self, chain, action, reject, protocol, src, dst, log):
        self.inputsentence = ["/ip/firewall/filter/add"]
        self.inputsentence.append("=chain=" + chain)
        self.inputsentence.append("=action=" + action)
	self.inputsentence.append("=reject-with=" + reject)
	self.inputsentence.append("=protocol=" + protocol)
	self.inputsentence.append("=src-address-list=" + src)
	self.inputsentence.append("=dst-address-list=" + dst)
	self.inputsentence.append("=log=" + log)
        self.writeSentence(self.inputsentence)
        self.readSentence()

    def printRule(self):
        self.inputsentence = ["/ip/firewall/filter/print"]
	self.inputsentence.append("=count-only=")
        self.writeSentence(self.inputsentence)
	count = int(self.readSentence()[1][5:])
	for items in range(count):
	     self.inputsentence = ["/ip/firewall/filter/print"]
             self.writeSentence(self.inputsentence)
             self.readSentence()
        
    def updateRule(self, numbers, chain, action, reject, protocol, src, dst, log):
	self.inputsentence = ["/ip/firewall/filter/set"]
	self.inputsentence.append("=numbers=" + numbers)
	self.inputsentence.append("=chain=" + chain)
	self.inputsentence.append("=action=" + action)
	self.inputsentence.append("=reject-with=" + reject)
	self.inputsentence.append("=protocol=" + protocol)
	self.inputsentence.append("=src-address-list=" + src)
	self.inputsentence.append("=dst-address-list=" + dst)
	self.inputsentence.append("=log=" + log)
	self.writeSentence(self.inputsentence)
	self.readSentence()
      
    def deleteRule(self, number):
        self.inputsentence = ["/ip/firewall/filter/remove"]
        self.inputsentence.append("=numbers=" + number)
        self.writeSentence(self.inputsentence)
        self.readSentence()
    
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.10.10.1', 8728))  
    apiros = ApiRos(s);             
    apiros.login('admin', '');

    if sys.argv[1] == "printrule":
	apiros.printRule();
    elif sys.argv[1] == "createrule":
	apiros.createRule(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]);
    elif sys.argv[1] == "updaterule":
	apiros.updateRule(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]);
    elif sys.argv[1] == "deleterule":
        apiros.deleteRule(sys.argv[2]);

if __name__ == '__main__':
    main()
