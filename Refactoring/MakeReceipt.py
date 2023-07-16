import json, math, copy
import pprint

def statement(invoice, plays):

    class PerformanceCalculator():
        def __init__(self, aPerformance, aPlay):
            self._performance = aPerformance
            self._play = aPlay
            pprint.pprint(self._performance)
            pprint.pprint(self._play)
            self.play = dict()

        def update(self):
            for idx in range(len(self._performance)):
                self.play[idx] = playFor(self._performance[idx])

    def playFor(aPerformance):
        return plays[aPerformance['playID']]

    def amountFor(aPerformance):
        result = 0

        if aPerformance['play']['type'] == "tragedy":
            result = 40000
            if aPerformance['audience'] > 30:
                result += 1000 * (aPerformance['audience'] - 30)
        elif aPerformance['play']['type'] == "comedy":
            result = 30000
            if aPerformance['audience'] > 20:
                result += 10000 + 500 * (aPerformance['audience'] - 20)
            result += 300 * aPerformance['audience']
        else:
            assert True, "Unknown genre : {:s}".format(aPerformance['play']['type'])
        return result

    def volumeCreditFor(aPerformance):
        result = 0
        # accumulating point
        result += max([aPerformance['audience'] - 30, 0])

        # give additional point per each 5 peoples
        if "comedy" == playFor(aPerformance)['type'] :
            result += math.floor(aPerformance['audience'] / 5)
        return result

    def getTotalVolumeCredits(statementData):
        result = 0
        for perf in statementData['performances']:
            result += volumeCreditFor(perf)
        return result

    def getTotalAmount(statementData):
        result = 0
        for perf in statementData['performances']:
            result += perf['amount']
        return result

    def enrichPerformance(aPerformance):
        result = aPerformance
        calculator = PerformanceCalculator(aPerformance, [playFor(res) for res in aPerformance])
        calculator.update()

        for idx in range(len(aPerformance)):
            result[idx]['play']  = calculator.play[idx]
        for res in result: res['amount']= amountFor(res)
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