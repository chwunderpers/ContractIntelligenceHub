import asyncio
import pandas 
from typing import Annotated 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.commodities import Commodities
from semantic_kernel.functions import kernel_function

class AlphaVantagePlugin:
    def __init__(self, api_key):
        self.api_key = api_key
        self.ts = TimeSeries(key=self.api_key, output_format='json')
        self.forex = ForeignExchange(key=self.api_key, output_format='json')
        self.commodities = Commodities(key=self.api_key, output_format='json')
        
    @kernel_function(description="Get the stock price for a symbol")
    async def get_stock_price(self, symbol: Annotated[str, "The stock symbol to retrieve the price for"]) -> Annotated[dict, "The stock price data"]:
        loop = asyncio.get_event_loop()
        data, meta_data = await loop.run_in_executor(None, self.ts.get_quote_endpoint, symbol)
        return data
    
    @kernel_function(description="Get the foreign exchange rate for a currency pair")
    async def get_exchange_rate(self, from_currency: Annotated[str, "The currency to convert from"], to_currency: Annotated[str, "The currency to convert to"]) -> Annotated[dict, "The exchange rate data"]:
        loop = asyncio.get_event_loop()
        data, meta_data = await loop.run_in_executor(None, self.forex.get_currency_exchange_rate, from_currency, to_currency)
        return data
    
    @kernel_function(description="Returns the global price for Aluminum")
    async def get_aluminium_price(self, interval: Annotated[str, "The interval. Supported values are 'monthly', 'quarterly', 'annual' " ]) -> Annotated[dict, "The Aluminum price data"]:
        loop = asyncio.get_event_loop()
        #data, meta_data = self.commodities.get_aluminum(interval='daily')
        data, meta_data = await loop.run_in_executor(None, self.commodities.get_aluminum, interval)
        return data
    