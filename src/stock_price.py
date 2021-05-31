from tiingo import TiingoClient
import yaml
import pandas as pd
import os

yaml_path = os.path.abspath(os.path.join((__file__), '..', '..', 'yaml'))
stock_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'stockprice'))
with open(os.path.join(yaml_path, "stock_data_config.yaml"), 'r') as stream:
    stock_yaml = yaml.safe_load(stream)

config = {}
config['session'] = stock_yaml['session']
config['api_key'] = stock_yaml['api_key']
client = TiingoClient(config)


def get_stock_data():
    # get lastest prices
    # set daily instead of 1 day
    historical_prices_df = client.get_dataframe(stock_yaml['ticker'],
                                                fmt='json',
                                                startDate=stock_yaml['start_date'],
                                                endDate=stock_yaml['end_date'],
                                                frequency=stock_yaml['Freq']
                                                )

    historical_prices_df = historical_prices_df.rename(
        {'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, axis='columns')

    historical_prices_df.to_json(
        stock_json_path + '/' + stock_yaml['ticker']+'_'+stock_yaml['Freq'])


get_stock_data()
