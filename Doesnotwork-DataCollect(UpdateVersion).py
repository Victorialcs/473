#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install web3


# In[2]:


pip install graphqlclient


# In[10]:


# Get basic feature related to a token
import json
from graphqlclient import GraphQLClient

def get_token_info(token_id):
    query = """
    {
      token(id: "%s") {
        name
        symbol
        decimals
        derivedETH
        tradeVolumeUSD
        totalLiquidity
      }
    }
    """ % (token_id)

    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    result = client.execute(query)

    data = json.loads(result)

    token_info = data['data']['token']

    return token_info

# Example usage
token_id = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token ID (DAI)

token_info = get_token_info(token_id)
if token_info:
    print("Token Name:", token_info['name'])
    print("Token Symbol:", token_info['symbol'])
    print("Decimals:", token_info['decimals'])
    print("Derived ETH:", token_info['derivedETH'])
    print("Trade Volume USD:", token_info['tradeVolumeUSD'])
    print("Total Liquidity:", token_info['totalLiquidity'])
else:
    print("No data found for the specified token ID.")


# In[8]:


# Trying to get same data as above but specified block at which we want the data to be from

import json
from graphqlclient import GraphQLClient

def get_token_info_at_timestamp(token_id, timestamp):
    query = """
    {{
      token(id: "{token_id}", block: {{ timestamp: "{timestamp}" }}) {{
        name
        symbol
        decimals
        derivedETH
        tradeVolumeUSD
        totalLiquidity
      }}
      blocks(first: 1, orderBy: timestamp, orderDirection: asc, where: {{ timestamp_gte: "{timestamp}" }}) {{
        number
      }}
    }}
    """.format(token_id=token_id, timestamp=timestamp)

    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    result = client.execute(query)

    data = json.loads(result)

    if 'data' in data and 'token' in data['data']:
        token_info = data['data']['token']
        block_number = data['data']['blocks'][0]['number'] if 'blocks' in data['data'] and data['data']['blocks'] else None
        return token_info, block_number
    else:
        print("No data found for the specified token ID at timestamp", timestamp)
        return None, None

token_id = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token ID (DAI)
timestamp = '1614556800'  # Example timestamp (in seconds)

token_info, block_number = get_token_info_at_timestamp(token_id, timestamp)
if token_info:
    print("Token Name:", token_info['name'])
    print("Token Symbol:", token_info['symbol'])
    print("Decimals:", token_info['decimals'])
    print("Derived ETH:", token_info['derivedETH'])
    print("Trade Volume USD:", token_info['tradeVolumeUSD'])
    print("Total Liquidity:", token_info['totalLiquidity'])
    if block_number:
        print("Block Number:", block_number)
else:
    print("No data found for the specified token ID at timestamp", timestamp)


# In[3]:


# Getting the highest price of a token between two blocks
import json
from graphqlclient import GraphQLClient

def get_max_token_price_between_blocks(token_id, from_date, to_date):
    query = """
    {{
      tokenDayDatas(
        orderBy: priceUSD,
        orderDirection: desc,
        where: {{
          token: "{token_id}",
          date_gte: {from_date},
          date_lte: {to_date}
        }}
      ) {{
        priceUSD
      }}
    }}
    """.format(token_id=token_id, from_date=from_date, to_date=to_date)

    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    result = client.execute(query)

    data = json.loads(result)

    if 'data' in data and 'tokenDayDatas' in data['data']:
        if data['data']['tokenDayDatas']:
            max_price = data['data']['tokenDayDatas'][0]['priceUSD']
            return max_price
        else:
            print("No data found for the specified time range.")
            return None
    else:
        print("No data found for the specified token ID.")
        return None

token_id = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token ID (DAI)
from_date = 1614556800  # Example start date timestamp (in seconds)
to_date = 1614643199  # Example end date timestamp (in seconds)

max_price = get_max_token_price_between_blocks(token_id, from_date, to_date)
if max_price is not None:
    print("Maximum token price between blocks:", max_price)


# In[4]:


import json
from graphqlclient import GraphQLClient

def get_min_token_price_between_blocks(token_id, from_date, to_date):
    query = """
    {{
      tokenDayDatas(
        orderBy: priceUSD,
        orderDirection: asc,
        where: {{
          token: "{token_id}",
          date_gte: {from_date},
          date_lte: {to_date}
        }}
      ) {{
        priceUSD
      }}
    }}
    """.format(token_id=token_id, from_date=from_date, to_date=to_date)

    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    result = client.execute(query)

    data = json.loads(result)

    if 'data' in data and 'tokenDayDatas' in data['data']:
        if data['data']['tokenDayDatas']:
            min_price = data['data']['tokenDayDatas'][0]['priceUSD']
            return min_price
        else:
            print("No data found for the specified time range.")
            return None
    else:
        print("No data found for the specified token ID.")
        return None

token_id = '0x6b175474e89094c44da98b954eedeac495271d0f'  # Example token ID (DAI)
from_date = 1614556800  # Example start date timestamp (in seconds)
to_date = 1614643199  # Example end date timestamp (in seconds)

min_price = get_min_token_price_between_blocks(token_id, from_date, to_date)
if min_price is not None:
    print("Lowest token price between blocks:", min_price)


# In[16]:


import json
from graphqlclient import GraphQLClient

def get_pair_day_data(pair_address, start_date):
    # GraphQL query to get pair day data
    query = """
    {{
      pairDayDatas(first: 100, orderBy: date, orderDirection: asc,
        where: {{
          pairAddress: "{pair_address}",
          date_gt: {start_date}
        }}
      ) {{
          date
          dailyVolumeToken0
          dailyVolumeToken1
          dailyVolumeUSD
          reserveUSD
      }}
    }}
    """.format(pair_address=pair_address, start_date=start_date)

    # Initialize GraphQL client
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    # Send GraphQL query
    result = client.execute(query)

    # Parse response string into JSON object
    data = json.loads(result)

    # Check if 'data' key exists
    if 'data' in data and 'pairDayDatas' in data['data']:
        pair_day_datas = data['data']['pairDayDatas']
        return pair_day_datas
    else:
        print("No data found for the specified pair address and start date.")
        return None

# Example usage
pair_address = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'  # Example pair address
start_date = 1592505859  # Example start date

pair_day_datas = get_pair_day_data(pair_address, start_date)
if pair_day_datas:
    for data in pair_day_datas:
        print("Date:", data['date'])
        print("Daily Volume Token 0:", data['dailyVolumeToken0'])
        print("Daily Volume Token 1:", data['dailyVolumeToken1'])
        print("Daily Volume USD:", data['dailyVolumeUSD'])
        print("Reserve USD:", data['reserveUSD'])
        print()  # Add a newline for readability
else:
    print("No pair day data found for the specified pair address and start date.")


# In[17]:


import json
from graphqlclient import GraphQLClient

def get_pair_info(pair_address, date_gt):
    # GraphQL query to get all available information for a pair
    query = """
    {{
      pairDayDatas(first: 100, orderBy: date, orderDirection: asc,
        where: {{
          pairAddress: "{pair_address}",
          date_gt: {date_gt}
        }}
      ) {{
        date
        dailyVolumeToken0
        dailyVolumeToken1
        dailyVolumeUSD
        reserveUSD
        pair {{
          id
          token0 {{
            id
            name
            symbol
          }}
          token1 {{
            id
            name
            symbol
          }}
          reserve0
          reserve1
          totalSupply
          reserveETH
          reserveUSD
          trackedReserveETH
          token0Price
          token1Price
          volumeToken0
          volumeToken1
          volumeUSD
          untrackedVolumeUSD
          txCount
          createdAtTimestamp
          createdAtBlockNumber
          liquidityProviderCount
          pairHourData {{
            id
            hourlyVolumeToken0
            hourlyVolumeToken1
            hourlyVolumeUSD
          }}
          liquidityPositions {{
            id
            liquidityTokenBalance
            user {{
              id
            }}
          }}
          liquidityPositionSnapshots {{
            id
            liquidityTokenBalance
            user {{
              id
            }}
          }}
          mints {{
            id
            amount
            sender
          }}
          burns {{
            id
            amount
            sender
          }}
          swaps {{
            id
            amount0In
            amount1In
            amount0Out
            amount1Out
            to
          }}
        }}
      }}
    }}
    """.format(pair_address=pair_address, date_gt=date_gt)

    # Initialize GraphQL client
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    # Send GraphQL query
    result = client.execute(query)

    # Parse response string into JSON object
    data = json.loads(result)

    # Check if 'data' key exists
    if 'data' in data and 'pairDayDatas' in data['data']:
        # Extract pair information
        pair_info = data['data']['pairDayDatas']
        return pair_info
    else:
        print("No data found for the specified pair address and date_gt.")
        return None

# Example usage
pair_address = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'  # Example pair address
date_gt = 1592505859  # Example date_gt value

pair_info = get_pair_info(pair_address, date_gt)
if pair_info:
    print("Pair Information:")
    for info in pair_info:
        print("Date:", info['date'])
        print("Daily Volume Token 0:", info['dailyVolumeToken0'])
        print("Daily Volume Token 1:", info['dailyVolumeToken1'])
        print("Daily Volume USD:", info['dailyVolumeUSD'])
        print("Reserve USD:", info['reserveUSD'])
        # Add similar print statements for other fields as needed
        print("------------------------------------")
else:
    print("No data found for the specified pair address and date_gt.")


# In[ ]:




