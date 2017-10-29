#coding:utf-8
import BitVector
import os
import sys

class SimpleHash():  
    
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
    
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        return (self.cap-1) & ret    

class BloomFilter():
    
    def __init__(self, BIT_SIZE=1<<25):
        self.BIT_SIZE = 1 << 25   #2^25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE) #
        self.hashFunc = []
        
        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))#哈希表的几个数组，指向后边的链表
        
    def insert(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1
    def isContains(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            ret &= self.bitset[loc]
        return ret

def main():
    bloomfilter = BloomFilter()
    with open("urls.txt",'r') as fd:
        urls = fd.read().split('\n')
        fd.close()
    for url in urls:
        if not bloomfilter.isContains(url):
            bloomfilter.insert(url)
        else:
            print 'url :%s has exist' % url 

if __name__ == '__main__':
    main()