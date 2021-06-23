import datetime
import hashlib
from Crypto import Signature

class Transaction:
    def __init__(self,start,end,amount):#这里的start，end对应lutuocoin里面的from,to
        self.start = start
        self.end = end
        self.amount = amount

    def computeHash(self):
        bytesData = bytes(str(self.start), encoding='utf-8') + bytes(self.end, encoding='utf-8') \
                    + bytes(str(self.amount), encoding='utf-8')
        return hashlib.sha256(bytesData).hexdigest()

    def sign(self,privateKey):
        self.signature = Signature.pkcs1_15.new(privateKey).sign(self.computeHash())

    def isValid(self):
        if self.start == None:
            return True
        if self.signature == None:
            print("miss signature")
            return False

        return Signature.pkcs1_15.new(self.start).verify(self.computeHash(), self.signature)

class Block:
    nonce = 1
    def __init__(self, transactions, preHash):
        self.transactions = transactions
        self.preHash = preHash
        self.timeStamp = datetime.datetime.now()
        self.hash = self.computeHash()

    def computeHash(self):
        bytesData = bytes(str(self.transactions), encoding='utf-8') + bytes(self.preHash, encoding='utf-8') \
                    + bytes(self.nonce) + bytes(str(self.timeStamp), encoding='utf-8')
        return hashlib.sha256(bytesData).hexdigest()

    def getAnswer(self,difficulty):
        index = 0
        answer = ""
        while index<difficulty:
            answer+='0'
            index+=1
        return answer

    def mine(self,difficulty):#利用pow机制防止篡改
        if self.validateTransactions() == False:
            raise Exception("invalid transaction in pool, stop mining")

        while True:
            self.hash = self.computeHash()
            #print("enter while.log")
            if(self.hash[:difficulty] != self.getAnswer(difficulty)):
                self.nonce+=1
                continue
            else:
                break

        print("finishing Mining")

    def validateTransactions(self):
        for transaction in self.transactions:
            if transaction.isValid() != True:
                print("illegal transaction")
                return False

        return True

class Chain:
    def __init__(self):
        genesisBlock = Block("ancestor", "")
        self.chain = [genesisBlock]
        self.difficulty = 3
        self.transactionPool = []
        self.minerReward = 50

    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    def addTransaction(self,transaction):
        if(transaction.start == None or transaction.end == None):
            raise Exception("invalid start or end")

        if transaction.isValid() == False:
            raise Exception("invalid transaction")

        self.transactionPool.append(transaction)


    '''def addBlockToChain(self, newBlock):
        newBlock.preHash = self.getLatestBlock().hash
        newBlock.mine(self.difficulty)
        self.chain.append(newBlock)'''

    def mineTransactionPool(self,minerRewardAddress):
        minerRewardTransaction = Transaction(
            "",#矿工奖励由系统发放，所以没有转账人
            minerRewardAddress,#矿工的转账地址
            self.minerReward
        )
        self.transactionPool.append(minerRewardTransaction)

        #挖矿
        newBlock = Block(
            self.transactionPool,
            self.getLatestBlock().hash
        )
        newBlock.mine(self.difficulty)

        self.chain.append(newBlock)
        self.transactionPool = []

    def isValid(self):
        if (len(self.chain) == 1 and
                self.chain[0].hash != hashlib.sha256(bytes(self.chain[0].transactions, encoding='utf-8')
                                                     + bytes(self.chain[0].preHash,encoding='utf-8')
                                                     + bytes(str(self.chain[0].timeStamp), encoding='utf-8')).hexdigest()):
            return False

        index = 1
        while index < len(self.chain):
            if(self.chain[index].hash != self.chain[index].computeHash()):
                print("transaction has been tampered!")
                return False
            if (self.chain[index].preHash != self.chain[index - 1].hash):
                print("block chain has been broken!")
                return False

            index += 1

        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transaction = Transaction("li","liu","3")
    transaction2 = Transaction("wang", "liu", "4")
    ch = Chain()
    ch.addTransaction(transaction)
    ch.addTransaction(transaction2)
    ch.mineTransactionPool("xiao")
    #ch.addBlockToChain(Block(transaction, ""))
    print(ch.getLatestBlock().hash)
    print(ch.chain[1].__dict__)
    #ch.chain[1].data = "123"
    print(ch.isValid())

