import json
import math
import pprint

def statement(invoice, plays):

    def playFor(aPerformance):
        return plays[aPerformance['playID']]

    def amountFor(aPerformance):
        result = 0

        if playFor(aPerformance)['type'] == "tragedy":
            result = 40000
            if aPerformance['audience'] > 30:
                result += 1000 * (aPerformance['audience'] - 30)
        elif playFor(aPerformance)['type'] == "comedy":
            result = 30000
            if aPerformance['audience'] > 20:
                result += 10000 + 500 * (aPerformance['audience'] - 20)
            result += 300 * aPerformance['audience']
        else:
            assert True, "Unknown genre : {:s}".format(playFor(aPerformance)['type'])
        return result

    totalAmount = 0
    volumeCredits = 0
    result = "bills (Name : {:s})\n".format(invoice['customer'])
    for perf in invoice['performances']:
        
        # accumulating point
        volumeCredits += max([perf['audience'] - 30, 0])

        # give additional point per each 5 peoples
        if "comedy" == playFor(perf)['type'] :
            volumeCredits += math.floor(perf['audience'] / 5)

        # show bills
        result += "\t{:15s} : $ {:7.2f} ({:3d} Seats)\n".format(playFor(perf)['name'], amountFor(perf)/100, perf['audience']) 
        totalAmount += amountFor(perf)
    result += "Total : $ {:.2f}\n".format(totalAmount/100)
    result += "Accumulated point : {:.0f} points\n".format(volumeCredits)
    print(result)
    return result
        

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
    with open('result.txt','w') as f:
        f.write(receipt_text)
        f.close