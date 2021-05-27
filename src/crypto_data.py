from tiingo import TiingoClient
import yaml
import pandas as pd
import os

yaml_path = os.path.abspath(os.path.join((__file__), '..', '..', 'yaml'))
crypto_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'crypto'))
with open(os.path.join(yaml_path, "crypto_data_config.yaml"), 'r') as stream:
    crypto_yaml = yaml.safe_load(stream)

config = {}
# To reuse the same HTTP Session across API calls (and have better performance), include a session key.
config['session'] = crypto_yaml['session']
# If you don't have your API key as an environment variable,
# pass it in via a configuration dictionary.
config['api_key'] = crypto_yaml['api_key']
client = TiingoClient(config)

# You can obtain cryptocurrency metadata using the following method.
# NOTE: Crypto symbol MUST be encapsulated in brackets as a Python list!


def get_crypto_data(top_of_book=False):
    crypto_pair = crypto_yaml['crypto']+crypto_yaml['currency']
    client.get_crypto_metadata([crypto_pair], fmt='json')

    if top_of_book == True:
        crypto_price = client.get_crypto_top_of_book([crypto_pair])
        return crypto_price
    # You can obtain historical Cryptocurrency price quotes from the get_crypto_price_history() method.
    # NOTE: Crypto symbol MUST be encapsulated in brackets as a Python list!
    else:
        crypto_data = client.get_crypto_price_history(tickers=[crypto_pair], startDate=crypto_yaml['start_date'],
                                                      endDate=crypto_yaml['end_date'], resampleFreq=crypto_yaml['Freq'])
        # The intraday frequencies are specified using an integer followed by “Min” or “Hour”, for example “30Min” or “1Hour”.
    crypto_data_df = pd.DataFrame(crypto_data[0]['priceData'])
    crypto_data_df.to_json(crypto_json_path + '/' +
                           crypto_data[0]['ticker']+'_'+crypto_yaml['Freq'])


a = get_crypto_data(top_of_book=True)
#out = pd.read_json(os.path.join(crypto_json_path, 'btcusd_30Min'))


''' crypto_info = {
    'crypto': 'BTC',
    'currency': 'USD',
    'start_date': '2020-12-2',
    'end_date': '2020-12-3',
    'Freq': '30Min'}
import io
with io.open(os.path.join(yaml_path, 'data.yaml'), 'w', encoding='utf8') as outfile:
    yaml.dump(crypto_info, outfile,
              default_flow_style=False, allow_unicode=True)

 '''
