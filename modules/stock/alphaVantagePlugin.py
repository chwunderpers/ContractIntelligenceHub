import asyncio
import json
import os
import logging
from typing import Annotated, Literal, Optional
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.commodities import Commodities
from alpha_vantage.alphaintelligence import AlphaIntelligence
from semantic_kernel.functions import kernel_function

class AlphaVantagePlugin:
    def __init__(self, api_key):
        self.logger = logging.getLogger("kernel")
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        self.ts = TimeSeries(key=self.api_key, output_format='json')
        self.forex = ForeignExchange(key=self.api_key, output_format='json')
        self.commodities = Commodities(key=self.api_key, output_format='json')
        self.ai = AlphaIntelligence(key=self.api_key, output_format='json')

    @kernel_function(description="Gets the current stock price for the commodity listed in the commodity")
    async def get_commodity_price(self, commodity: Annotated[str, "The commodity to retrieve the price for"]) -> Annotated[dict, "The historical commodity prices"]:
        if commodity == 'Aluminium':
            loop = asyncio.get_event_loop()
            data, meta_data = await loop.run_in_executor(None, self.commodities.get_aluminum, 'monthly')
            return data.head(24)
   
    @kernel_function(description="Get live and historical market news and sentiment data.")
    async def get_news_sentiment(self, 
                                 tickers
                                 ) -> Annotated[tuple[Literal['NEWS_SENTIMENT'], Literal['feed'], None], "The news sentiment data"]:
        result = []
        for ticker in tickers:
            loop = asyncio.get_event_loop()
            data, meta_data = await loop.run_in_executor(None, self.ai.get_news_sentiment, 'AA')
            data = data[:5]
            data = data[["title","overall_sentiment_label"]]
            result.append(data)
        return result