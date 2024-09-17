import asyncio
from typing import Annotated, Literal, Optional
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.commodities import Commodities
from alpha_vantage.alphaintelligence import AlphaIntelligence
from semantic_kernel.functions import kernel_function

class AlphaVantagePlugin:
    def __init__(self, api_key):
        self.api_key = api_key
        self.ts = TimeSeries(key=api_key, output_format='json')
        self.forex = ForeignExchange(key=api_key, output_format='json')
        self.commodities = Commodities(key=api_key, output_format='json')
        self.ai = AlphaIntelligence(key=api_key, output_format='json')

         
        
        
    @kernel_function(description="Get the stock price for a symbol")
    async def get_stock_price(self, symbol: Annotated[str, "The stock symbol to retrieve the price for"]) -> Annotated[tuple[Literal['GLOBAL_QUOTE'], Literal['Global Quote'], None], "The stock price data"]:
        loop = asyncio.get_event_loop()
        data, meta_data = await loop.run_in_executor(None, self.ts.get_quote_endpoint, symbol)
        return data
    
    @kernel_function(description="Get the foreign exchange rate for a currency pair")
    async def get_exchange_rate(self, from_currency: Annotated[str, "The currency to convert from"], to_currency: Annotated[str, "The currency to convert to"]) -> Annotated[tuple[Literal['CURRENCY_EXCHANGE_RATE'], Literal['Realtime Currency Exchange Rate']], "The exchange rate data"]:
        loop = asyncio.get_event_loop()
        data, meta_data = await loop.run_in_executor(None, self.forex.get_currency_exchange_rate, from_currency, to_currency)
        return data
    
    @kernel_function(description="Returns the global price for Aluminium")
    async def get_aluminium_price(self, interval: Annotated[str, "The interval. Supported values are 'monthly', 'quarterly', 'annual' " ]) -> Annotated[tuple[Literal['ALUMINUM'], Literal['data'], None]
, "The Aluminium price data"]:
        loop = asyncio.get_event_loop()
        #data, meta_data = self.commodities.get_aluminum(interval='daily')
        data, meta_data = await loop.run_in_executor(None, self.commodities.get_aluminum, interval)
        return data
    
    @kernel_function(description="Get live and historical market news and sentiment data.")
    async def get_news_sentiment(self, 
                                 tickers: Annotated[str, "the symbols of your choice."], 
                                 topics: Annotated[str, "Optional news topics of your choice"]
                                 ) -> Annotated[tuple[Literal['NEWS_SENTIMENT'], Literal['feed'], None], "The news sentiment data"]:
        loop = asyncio.get_event_loop()
        data, meta_data = await loop.run_in_executor(None, self.ai.get_news_sentiment, tickers, topics)
        #data_json = data.to_json(orient="records")
        return data