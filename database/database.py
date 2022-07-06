import sqlite3
from datetime import date,time,datetime

conn=sqlite3.connect('Fictive.db')

c =conn.cursor()

EUR_USD_XRate:float ="1.04"
EUR_GBP_XRate:float='0.85'

#define the function for returning the currency exchange information
def Xrate(fromcur: str=None,tocur: str = None, ):
    if (fromcur=="eur" or "EUR" and tocur=="usd" or "USD"):
        return {
                "date":date.today(),
                "historical":'',
                "info":{
                    datetime.timestamp(datetime.today())
                },
                "query":{
                    "date":date.today(),
                    "from":fromcur,
                    "to": tocur
                },
                "result":EUR_USD_XRate,
                "success":'true'
               }
    if (fromcur=="EUR" and tocur=="gbp"):
        return {"date":date.today(),
                "historical":'',
                "info":{
                    datetime.timestamp(datetime.today())
                },
                "query":{
                    "date":date.today(),
                    "from":fromcur,
                    "to": tocur
                },
                "result":EUR_GBP_XRate,
                "success":'true'
               }
    return {"details": "no exchange information regarding this currency"}

 #an example of how to use the Xrate function   

 #create a class containing information of material,country, and priceEur 
class Goods:
    def __init__(self,meterialId,countryId,priceEur):   
     self.meterialId=meterialId
     self.countryId=countryId
     self.priceEur=priceEur

#get a instace of the class which contain information of the cotten price in Germany
cotGer=Goods(1,2,2.25)
#eur to usd exchange rate
eur_usd_Xrate=Xrate('eur','usd')['result']
#calculate the cotton price in usd
cotten_price_usd=float(cotGer.priceEur)*float(eur_usd_Xrate)

#check if the combination of the material and country already exist
c.execute("SELECT * FROM PRICE_PER_COUNTRY_Material WHERE FK_MATERIALNUMBER==cotGer.meterialId AND FK_COUNTRY==cotGer.countryId")
#if the record does not exist,add a new record with the calculated price
if c.fetchone()==None:
   c.execute("INSERT INTO PRICE_PER_COUNTRY_Material VALUES (NULL,cotGer.meterialId,cotGer.countryId,'USD',cotten_price_usd)")
#if the record already exists, uodate the PriceValue attribute
else:
   c.execute("UPDATE PRICE_PER_COUNTRY_Material SET PriceValue =cotten_price_usd WHERE FK_MATERIALNUMBER==cotGer.meterialId AND FK_COUNTRY==cotGer.countryId")

conn.commit()
conn.close()