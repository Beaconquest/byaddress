# byaddress
A web scraper using python and the requests library, that reads a CSV file of addresses, and submits them to the USPS website to check if the addresses are valid or not. The output is the same CSV file as the input, but with an additional column added to it that displays if the address is valid.

---
## Source website
USPS Website:
[https://tools.usps.com/zip-code-lookup.htm?byaddress](https://tools.usps.com/zip-code-lookup.htm?byaddress "USPS Website")

---
## Required Libararies:

```python
pip install beautifulsoup
pip install requests
```

## CSV File Format Example
Program uses _.csv_ files. Use the following headers when creating source document.
|Company|Street|City|St|ZIPCode|
|-------|------|----|--|-------|
|BEND PAWN & TRADING CO-LAPINE|52504 U.S. 97|LA PINE|OR|9773
|CARDIOSTART RESALE THRIFT STR|435 W CASCADE AVE|SISTERS|OR|97759|

---
## Output Format Example
The output of the program should look like this.

|Company|Street|City|St|ZIPCode|AddressStatus|
|-------|------|----|--|-------|-------------|
|BEND PAWN & TRADING CO-LAPINE|52504 U.S. 97|LA PINE|OR|9773|Not Valid
|CARDIOSTART RESALE THRIFT STR|435 W CASCADE AVE|SISTERS|OR|97759|Valid
