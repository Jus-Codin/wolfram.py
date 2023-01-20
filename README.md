# wolfram.py
A wrapper for the Wolfram|Alpha v1.0 and v2.0 API

The library implements both a standard client (powered by [requests](https://requests.readthedocs.io/en/latest/)) and an asynchronous client (powered by [aiohttp](https://docs.aiohttp.org/en/stable/index.html))

Example usage:
```py
from wolfram import Client

client = Client(appid=<YOUR-APP-ID>)
res = client.full_results_query(input="pi")

print(res.primary.subpods[0].plaintext)
>>> '3.1415926535897932384626433832795028841971693993751058209749445923...'
```

If you do not have an API key, you can get one from https://products.wolframalpha.com/api/

## Installation
You can install this package by running the command:
```
pip install wolfram.py
```

Alternatively, install the master branch at:
```
pip install git+https://github.com/Jus-Codin/wolfram.py
```