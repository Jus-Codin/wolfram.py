# wolfram.py
A wrapper for the Wolfram|Alpha v1.0 and v2.0 API

This is still a work in progress, and the name might be changed

APIs that are to be implemented:


- [x] [Full Results API](https://products.wolframalpha.com/api/documentation/)
- [x] [Simple API](https://products.wolframalpha.com/simple-api/documentation/)
- [x] [Short Answers API](https://products.wolframalpha.com/short-answers-api/documentation/)
- [x] [Spoken Results API](https://products.wolframalpha.com/spoken-results-api/documentation/)
- [x] [Conversational API](https://products.wolframalpha.com/conversational-api/documentation/)

## - Update 26/9/2022
All APIs have been implemented. However, docstrings and some type hinting is incomplete.

Additionally, the current library does not have any error handling so it is somewhat difficult to debug it

The Full Results and Conversational API has been tested for the most part, and I cannot guarantee that the other APIs will work at all. If you find any bugs with the library, please open an issue. Assistance with debugging would be greatly appreciated

### List of things left to do:
- [ ] Implement custom exceptions and error handling to tell users what went wrong
- [ ] More potential bug fixing
- [ ] Complete type hinting and docstring
- [ ] Potentially create documentation
- [ ] Setup files for uploading to pypi.org