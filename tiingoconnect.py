import os
import requests
import pandas as pd
from tiingo import TiingoClient

yourtoken = os.getenv("TIINGO_API_KEY")

config = {}
config['session'] = True
config['api_key'] = yourtoken

client = TiingoClient(config)

def DataReader(ticker, d_start, d_end):

      # We are expecting DateTime type for input dates !! (just like original Pandas DataReader)

      d_end = d_end.strftime("%Y-%m-%d")
      d_start = d_start.strftime("%Y-%m-%d")
      # print d_start
      # print d_end

      #  headers = {
      #        'Content-Type': 'application/json',
      #        'Authorization' : 'Token ' + yourtoken
      #        }
      #  url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + d_start + "&endDate="+ d_end

      #  print(f"url: {url}")
      #  requestResponse = requests.get(url,headers=headers)
      #  print(type(requestResponse))
      #  print(requestResponse)

      #  json_result = requestResponse.json()

      #  print(f"json_result type: {type(json_result)}")

      #  df = pd.DataFrame.from_records(json_result)
      print("Getting Data from Tiingo")
      df = client.get_dataframe(ticker, startDate=d_start, endDate=d_end)
      print(df.head())

      # Check for existance of Adj Close column
      # If not, check for existance of Close column
      # If not -> throw error
      # If no Adj Close, but Close, copy Close to Adj close

      if not "adjClose" in df.columns:
            if "close" in df.columns:
                  df["adjClose"] = df["close"]
            else:
                  print("Error: No Close information")
            return
      
      # Convert ISO date format to Pandas DateTime
      #df["date"] = pd.to_datetime(df["date"])
      # Align Column Names to previous DataReader names
      print(df.columns)
      df = df.rename(
            columns={
            "date": "Date",
            "open": "Open",
            "adjClose": "Adj Close",
            "volume": "Volume",
            "high": "High",
            "low": "Low",
            "close": "Close",
            }
      )
      a = df.set_index(["Date"])
      print(a)
      return a

