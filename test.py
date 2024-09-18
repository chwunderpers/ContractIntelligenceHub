from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.commodities import Commodities
from alpha_vantage.alphaintelligence import AlphaIntelligence
import os

api_key = 'R3QKLXGNDRCXB1X7'
ts = TimeSeries(key=api_key, output_format='json')
forex = ForeignExchange(key=api_key, output_format='json')
commodities = Commodities(key=api_key, output_format='json')
ai = AlphaIntelligence(key=api_key, output_format='json')


test = ai.get_news_sentiment('AA')
print(test)