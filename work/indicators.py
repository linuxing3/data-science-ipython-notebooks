import json 
import urllib 
results = json.load(urllib.urlopen("http://api.tradingeconomics.com/historical/country/country_name/indicator/indicator_name?c=guest:guest"))

print(results)