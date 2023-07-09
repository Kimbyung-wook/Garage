import json
import math
import pprint

def statement(invoice, plays):

    def amountFor(perf, PLAY):
        thisAmount = 0

        if PLAY['type'] == "tragedy":
            thisAmount = 40000
            if perf['audience'] > 30:
                thisAmount += 1000 * (perf['audience'] - 30)
        elif PLAY['type'] == "comedy":
            thisAmount = 30000
            if perf['audience'] > 20:
                thisAmount += 10000 + 500 * (perf['audience'] - 20)
            thisAmount += 300 * perf['audience']
        else:
            assert True, "Unknown genre : {:s}".format(PLAY['type'])
        return thisAmount

    totalAmount = 0
    volumeCredits = 0
    result = "bills (Name : {:s})\n".format(invoice['customer'])
    for perf in invoice['performances']:
        PLAY = plays[perf['playID']]
        thisAmount = amountFor(perf, PLAY)

        # accumulating point
        volumeCredits += max([perf['audience'] - 30, 0])

        # give additional point per each 5 peoples
        if "comedy" == PLAY['type'] :
            volumeCredits += math.floor(perf['audience'] / 5)

        # show bills
        result += "\t{:15s} : $ {:7.2f} ({:3d} Seats)\n".format(PLAY['name'], thisAmount/100, perf['audience']) 
        totalAmount += thisAmount
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