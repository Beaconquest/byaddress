# byaddress - Description
A web scraper using python and the requests library, that reads a CSV file of addresses, and submits them to the USPS website to check if the addresses are valid or not. The output is the same CSV file as the input, but with an additional column added to it that displays if the address is valid.

---
## Source website
[USPS Website](https://tools.usps.com/zip-code-lookup.htm?byaddress "USPS Website")

---
## Project Setup

### Python Dependencies
Ensure the prerequisites are installed:
```
- python3.8+
- pip (tool for installing Python packages)
```


Create a virtual env for Python3.8+ inside project directory:
```
python3.8 -m venv venv
```

Activate newly created environment:
```bash
. venv/bin/activate
```


Install the required Python packages:  
```python
pip install beautifulsoup
pip install requests
```
or
```
pip install -r requirements.txt
```

OPTIONAL: Exit the virtual environment using the following command:
```bash
deactivate
```
---

## CSV File Format Example
Project uses _.csv_ files. Use the following headers when creating source document.
|Company|Street|City|St|ZIPCode|
|-------|------|----|--|-------|
|BEND PAWN & TRADING CO-LAPINE|52504 U.S. 97|LA PINE|OR|9773
|CARDIOSTART RESALE THRIFT STR|435 W CASCADE AVE|SISTERS|OR|97759|

---
## Output Format Example
The output of the project should look like this.

|Company|Street|City|St|ZIPCode|AddressStatus|
|-------|------|----|--|-------|-------------|
|BEND PAWN & TRADING CO-LAPINE|52504 U.S. 97|LA PINE|OR|9773|Not Valid
|CARDIOSTART RESALE THRIFT STR|435 W CASCADE AVE|SISTERS|OR|97759|Valid
