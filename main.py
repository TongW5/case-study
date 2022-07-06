from fastapi import FastAPI
from fastapi.response import FileResponse
from databases import Database
from datetime import date,time,datetime
from pydantic import BaseSettings
database = Database("sqlite:///test.db")

app = FastAPI()

class Settings(BaseSettings):
   EUR_USD_XRate:float ="1.04"
   EUR_GBP_XRate:float='0.85'

settings=Settings()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#retrieving the EUR-USD Xrate by calling a REST-API('GET')
@app.get("/api/xrate")
async def xrate(fromcur: str=None,tocur: str = None, ):
    if (fromcur=="eur" and tocur=="usd"):
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
                "result":settings.EUR_USD_XRate,
                "success":'true'
               }
    if (fromcur=="eur" and tocur=="gbp"):
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
                "result":settings.EUR_GBP_XRate,
                "success":'true'
               }
    return {"details": "no exchange information regarding this currency"}

@app.get("/api/xrate/{priceEUR}")
async def priceExchange(priceEUR: float):
    return {"price-in-USD": priceEUR*settings.EUR_USD_XRate}

