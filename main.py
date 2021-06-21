import hashlib


class Block:
    nonce = 1
    def __init__(self, data, preHash):
        self.data = data
        self.preHash = preHash
        self.hash = self.computeHash()

    def computeHash(self):
        bytesData = bytes(self.data, encoding='utf-8') + bytes(self.preHash, encoding='utf-8') + bytes(self.nonce)
        return hashlib.sha256(bytesData).hexdigest()

    def getAnswer(self,difficulty):
        index = 0
        answer = ""
        while index<difficulty:
            answer+='0'
            index+=1
        return answer

    def mine(self,difficulty):#利用pow机制防止篡改
        while True:
            self.hash = self.computeHash()
            if(self.hash[:difficulty] != self.getAnswer(difficulty)):
                self.nonce+=1
                continue
            else:
                break

        print("finishing Mining")

class Chain:
    def __init__(self):
        genesisBlock = Block("ancestor", "")
        self.chain = [genesisBlock]
        self.difficulty = 4

    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlockToChain(self, newBlock):
        newBlock.preHash = self.getLatestBlock().hash
        newBlock.mine(self.difficulty)
        self.chain.append(newBlock)

    def isValid(self):
        if (len(self.chain) == 1 and
                self.chain[0].hash != hashlib.sha256(bytes(self.chain[0].data, encoding='utf-8') + bytes(self.chain[0].preHash,encoding='utf-8')).hexdigest()):
            return False

        index = 1
        while index < len(self.chain):
            if(self.chain[index].hash != self.chain[index].computeHash()):
                print("data has been tampered!")
                return False
            if (self.chain[index].preHash != self.chain[index - 1].hash):
                print("block chain has been broken!")
                return False

            index += 1

        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ch = Chain()
    ch.addBlockToChain(Block("456", ""))
    print(ch.getLatestBlock().hash)
    #ch.chain[1].data = "123"
    print(ch.isValid())

