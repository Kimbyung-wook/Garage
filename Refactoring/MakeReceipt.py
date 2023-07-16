import json, math, copy
import pprint

def statement(invoice, plays):

    class PerformanceCalculator():
        def __init__(self, aPerformance, aPlay):
            self._performance = aPerformance
            self._aplay = aPlay
            self._play = dict()
            self._amount = list()
            self._volumeCredits = list()

        def play(self):
            for idx in range(len(self._performance)):
                self._play[idx] = playFor(self._performance[idx])
            return self._play

        def amount(self):
            for idx in range(len(self._performance)):
                result = 0
                if self._aplay[idx]['type'] == "tragedy":
                    result = 40000
                    if self._performance[idx]['audience'] > 30:
                        result += 1000 * (self._performance[idx]['audience'] - 30)
                elif self._aplay[idx]['type'] == "comedy":
                    result = 30000
                    if self._performance[idx]['audience'] > 20:
                        result += 10000 + 500 * (self._performance[idx]['audience'] - 20)
                    result += 300 * self._performance[idx]['audience']
                else:
                    assert True, "Unknown genre : {:s}".format(self._aplay[idx]['type'])
                self._amount.append(result)
            return self._amount
        
        def volumeCredit(self):
            for idx in range(len(self._performance)):
                result = 0
                # accumulating point
                result += max([self._performance[idx]['audience'] - 30, 0])

                # give additional point per each 5 peoples
                if "comedy" == self._aplay[idx]['type'] :
                    result += math.floor(self._performance[idx]['audience'] / 5)
                self._volumeCredits.append(result)
            return self._volumeCredits

    def playFor(aPerformance):
        return plays[aPerformance['playID']]

    def amountFor(aPerformance):
        return PerformanceCalculator(aPerformance, [playFor(res) for res in aPerformance]).amount()

    def volumeCreditFor(aPerformance):
        return PerformanceCalculator(aPerformance, [playFor(res) for res in aPerformance]).volumeCredit()


    def getTotalAmount(statementData):
        result = 0
        for perf in statementData['performances']:
            result += perf['amount']
        return result

    def getTotalVolumeCredits(statementData):
        result = 0
        for perf in statementData['performances']:
            result += perf['volumeCredit']
        return result

    def enrichPerformance(aPerformance):
        result = aPerformance
        calculator = PerformanceCalculator(aPerformance, [playFor(res) for res in aPerformance])

        for idx in range(len(aPerformance)):
            result[idx]['play']  = calculator.play()[idx]
            result[idx]['amount']= calculator.amount()[idx]
            result[idx]['volumeCredit']= calculator.volumeCredit()[idx]
        return result

    def createStatementData(invoice):
        STATEMENTDATA = {}
        STATEMENTDATA['customer']           = invoice['customer']
        STATEMENTDATA['performances']       = enrichPerformance(invoice['performances'])
        STATEMENTDATA['totalAmount']        = getTotalAmount(STATEMENTDATA)
        STATEMENTDATA['totalVolumeCredits'] = getTotalVolumeCredits(STATEMENTDATA)
        return STATEMENTDATA

    def renderPlainText(statementData):
        def usd(aNumber):
            return aNumber/100

        result = "bills (Name : {:s})\n".format(statementData['customer'])

        for perf in statementData['performances']:
            result += "\t{:15s} : $ {:7.2f} ({:3d} Seats)\n".format(perf['play']['name'], usd(perf['amount']), perf['audience']) 

        result += "Total : $ {:.2f}\n".format(                  usd(statementData['totalAmount']))
        result += "Accumulated point : {:.0f} points\n".format(statementData['totalVolumeCredits'])
        return result

    # Main loop 
    STATEMENTDATA = createStatementData(invoice)
    return renderPlainText(STATEMENTDATA)

def openJSON(fileName:str):
    with open(fileName) as f:
        result = json.load(f)
    # pprint.pprint(result)
    return result

if __name__ == "__main__":
    # Read json files
    invoices = openJSON('invoices.json')
    plays = openJSON("plays.json")
    receipt_text = statement(invoice=invoices, plays=plays)
    print(receipt_text)
    with open('result.txt','w') as f:
        f.write(receipt_text)
        f.close