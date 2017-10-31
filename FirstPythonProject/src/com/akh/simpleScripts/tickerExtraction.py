'''
Created on Oct 30, 2017

@author: akhash
'''

rawString = "NASDAQ:TRUP  NYSE:TWLO  NASDAQ:UBNT  NYSE:HXL  NASDAQ:FIZZ  NYSE:GWRE  NASDAQ:OLED  NYSE:HEI  NYSE:VEEV  NASDAQ:TEAM  NASDAQ:QRVO  NASDAQ:CGNX  NYSE:PANW  NYSE:ANET  NYSE:MKL  NASDAQ:KLAC  NASDAQ:XLNX  NASDAQ:IBKR  NYSE:Q  NASDAQ:WDAY  NASDAQ:ILMN  NASDAQ:LRCX  NASDAQ:ADI  NASDAQ:ISRG  NASDAQ:AMAT  NYSE:CRM  NASDAQ:COST  NASDAQ:ASML  NASDAQ:NFLX  NASDAQ:QCOM  NASDAQ:PCLN  NASDAQ:AVGO  NYSE:BMY  NYSE:DIS  NASDAQ:AMZN  OTCMKTS:WFCF  OTCMKTS:SAFRY  NASDAQ:ANSS  NYSE:HEI.A"

def parseString(rawString):
    resultArray = []
    strArray = rawString.split(sep="  ")
    
    for tickerWithEx in strArray :
        ticker = tickerWithEx.split(":")[1]
        resultArray.append(ticker)

    resultArray.reverse()
    print(', '.join(resultArray))

def main():    
    parseString(rawString)    
    
main()   