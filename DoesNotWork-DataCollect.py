#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install web3


# In[3]:


from web3 import Web3
from datetime import datetime, timedelta

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a6ac94518f4f43278a65899c03f80eea'))

print(w3.eth.block_number) #Check if the notebook is connected to the Infura node
print(w3.__dict__)


# Check connection
print(w3.is_connected())


# In[12]:


pip install graphqlclient


# In[40]:


#Trying to get token's highest price
import json
from graphqlclient import GraphQLClient

def get_max_token_price(token_address, from_date, to_date):
    # GraphQL query to get token prices
    query = """
    query {{
      tokenDayDatas(
        where: {{
          token: "{token_address}",
          date_gt: {from_date},
          date_lt: {to_date}
        }},
        orderBy: date,
        orderDirection: desc,
        first: 1
      ) {{
        priceUSD
      }}
    }}
    """.format(token_address=token_address, from_date=from_date, to_date=to_date)


    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')
    

    result = client.execute(query)
    print(result)


    data = json.loads(result)
    print(data)


    if 'data' in data and 'tokenDayDatas' in data['data'] and data['data']['tokenDayDatas']:
        max_price = data['data']['tokenDayDatas'][0]['priceUSD']
        return max_price
    else:
        print("No data found for the specified token address and date range.")
        return None

# Example usage
token_address = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'  # Example token address (USDC)
from_date = '10000835'  # Start date timestamp (in seconds)
to_date = '10112000'  # End date timestamp (in seconds)

max_price = get_max_token_price(token_address, from_date, to_date)
print("Maximum token price:", max_price)


# In[27]:


#Trying to get token's highest and lowst price

import json
from graphqlclient import GraphQLClient
def get_token_price_extremes(token_address, from_date, to_date):
    # GraphQL query to get token prices for the lowest price
    query_lowest = """
    query {{
      tokenDayDatas(
        where: {{
          token: "{token_address}",
          date_gt: {from_date},
          date_lt: {to_date}
        }},
        orderBy: date,
        orderDirection: asc,
        first: 1
      ) {{
        priceUSD
      }}
    }}
    """.format(token_address=token_address, from_date=from_date, to_date=to_date)


    query_highest = query_lowest.replace("asc", "desc")  # Change orderDirection to desc for highest price


    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')


    result_lowest = client.execute(query_lowest)
    data_lowest = json.loads(result_lowest)


    result_highest = client.execute(query_highest)
    data_highest = json.loads(result_highest)


    lowest_price = data_lowest['data']['tokenDayDatas'][0]['priceUSD'] if 'data' in data_lowest and 'tokenDayDatas' in data_lowest['data'] and data_lowest['data']['tokenDayDatas'] else None
    highest_price = data_highest['data']['tokenDayDatas'][0]['priceUSD'] if 'data' in data_highest and 'tokenDayDatas' in data_highest['data'] and data_highest['data']['tokenDayDatas'] else None

    return lowest_price, highest_price

# Example usage
token_address = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token address (USDC)
from_date = '1614556800'  # Start date timestamp (in seconds)
to_date = '1614643199'  # End date timestamp (in seconds)

lowest_price, highest_price = get_token_price_extremes(token_address, from_date, to_date)

if lowest_price is not None:
    print("Lowest token price:", lowest_price)
else:
    print("No data found for the lowest price.")

if highest_price is not None:
    print("Highest token price:", highest_price)
else:
    print("No data found for the highest price.")


# In[29]:


import json
from graphqlclient import GraphQLClient

def get_token_info_at_block(token_id, block):
    # GraphQL query to get token information at a specific block
    query = """
    {{
      token(id: "{token_id}", block: {{ number: {block} }}) {{
        name
        symbol
        decimals
        derivedETH
        tradeVolumeUSD
        totalLiquidity
      }}
    }}
    """.format(token_id=token_id, block=block)

    # Initialize GraphQL client
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    # Send GraphQL query
    result = client.execute(query)

    # Parse response string into JSON object
    data = json.loads(result)

    # Extract token information
    token_info = data['data']['token']

    return token_info

# Example usage
token_id = '0x8E870D67F660D95d5be530380D0eC0bd388289E1'  # Example token ID (DAI)
block = 10000835  # Specify the block number

token_info = get_token_info_at_block(token_id, block)
if token_info:
    print("Token Name:", token_info['name'])
    print("Token Symbol:", token_info['symbol'])
    print("Decimals:", token_info['decimals'])
    print("Derived ETH:", token_info['derivedETH'])
    print("Trade Volume USD:", token_info['tradeVolumeUSD'])
    print("Total Liquidity:", token_info['totalLiquidity'])
else:
    print("No data found for the specified token ID at block", block)


# In[31]:


import json
from graphqlclient import GraphQLClient

def get_token_mint_burn_counts_at_block(token_id, block):
    # GraphQL query to get token mint and burn counts at a specific block
    query = """
    {{
      token(id: "{token_id}", block: {{ number: {block} }}) {{
        mintCount
        burnCount
      }}
    }}
    """.format(token_id=token_id, block=block)

    # Initialize GraphQL client
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    # Send GraphQL query
    result = client.execute(query)

    # Parse response string into JSON object
    data = json.loads(result)

    # Check if 'data' key exists
    if 'data' in data and 'token' in data['data']:
        # Extract mint and burn counts
        token_data = data['data']['token']
        mint_count = token_data.get('mintCount', 0)
        burn_count = token_data.get('burnCount', 0)
        return mint_count, burn_count
    else:
        print("No data found for the specified token ID at block", block)
        return None, None

# Example usage
token_id = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token ID (DAI)
block = 10000835  # Specify the block number

mint_count, burn_count = get_token_mint_burn_counts_at_block(token_id, block)
if mint_count is not None and burn_count is not None:
    print("Mint Count:", mint_count)
    print("Burn Count:", burn_count)


# In[33]:


import json
from graphqlclient import GraphQLClient

def get_token_mint_burn_counts(token_id):
    # GraphQL query to get token mint and burn counts
    query = """
    {{
      token(id: "{token_id}") {{
        mintCount
        burnCount
      }}
    }}
    """.format(token_id=token_id)

    # Initialize GraphQL client
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    # Send GraphQL query
    result = client.execute(query)

    # Parse response string into JSON object
    data = json.loads(result)

    # Check if 'data' key exists
    if 'data' in data and 'token' in data['data']:
        # Extract mint and burn counts
        token_data = data['data']['token']
        mint_count = token_data.get('mintCount', 0)
        burn_count = token_data.get('burnCount', 0)
        return mint_count, burn_count
    else:
        print("No data found for the specified token ID.")
        return None, None

# Example usage
token_id = '0x8E870D67F660D95d5be530380D0eC0bd388289E1'  # Example token ID (DAI)

mint_count, burn_count = get_token_mint_burn_counts(token_id)
if mint_count is not None and burn_count is not None:
    print("Mint Count:", mint_count)
    print("Burn Count:", burn_count)


# In[ ]:




