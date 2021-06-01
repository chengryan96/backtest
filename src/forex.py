from alpha_vantage.foreignexchange import ForeignExchange
import yaml
import pandas as pd
import os

yaml_path = os.path.abspath(os.path.join((__file__), '..', '..', 'yaml'))
forex_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'forex'))
with open(os.path.join(yaml_path, "forex_config.yaml"), 'r') as stream:
    forex_yaml = yaml.safe_load(stream)


def get_forex_data():
    cc = ForeignExchange(key=forex_yaml['api_key'])
    if forex_yaml['Freq'] == 'daily':
        data, _ = cc.get_currency_exchange_daily(
            from_symbol=forex_yaml['from_symbol'], to_symbol=forex_yaml['to_symbol'], outputsize='full')
        forex_df = pd.DataFrame.from_dict(data, orient='index')
        forex_df = forex_df.sort_index()
        forex_df = forex_df.rename(
            {'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close'}, axis='columns')

    elif forex_yaml['Freq'] != 'daily':
        data, _ = cc.get_currency_exchange_intraday(
            from_symbol=forex_yaml['from_symbol'], to_symbol=forex_yaml['to_symbol'], interval=forex_yaml['Freq'], outputsize='full')
        # supported values are '1min', '5min', '15min', '30min', '60min'
        forex_df = pd.DataFrame.from_dict(data, orient='index')
        forex_df = forex_df.sort_index()
        forex_df = forex_df.rename(
            {'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close'}, axis='columns')

    forex_df.to_json(
        forex_json_path + '/' + forex_yaml['from_symbol'] + forex_yaml['to_symbol']+'_'+forex_yaml['Freq'])


get_forex_data()
