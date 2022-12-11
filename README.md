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

Note that this is still a work in progress

APIs that are to be implemented:


- [x] [Full Results API](https://products.wolframalpha.com/api/documentation/)
- [x] [Simple API](https://products.wolframalpha.com/simple-api/documentation/)
- [x] [Short Answers API](https://products.wolframalpha.com/short-answers-api/documentation/)
- [x] [Spoken Results API](https://products.wolframalpha.com/spoken-results-api/documentation/)
- [x] [Conversational API](https://products.wolframalpha.com/conversational-api/documentation/)

## - Update 26/9/2022
All APIs have been implemented. However, docstrings and some type hinting is incomplete.

Additionally, the current library does not have any error handling so it is somewhat difficult to debug it

The Full Results and Conversational API on the standard Client has been tested for the most part, and I cannot guarantee that the other APIs will work at all. If you find any bugs with the library, please open an issue. Assistance with debugging would be greatly appreciated

### List of things left to do:
- [x] Implement custom exceptions and error handling to tell users what went wrong
- [ ] More potential bug fixing
- [x] Complete type hinting and docstring
- [ ] Potentially create documentation
- [ ] Setup files for uploading to pypi.org