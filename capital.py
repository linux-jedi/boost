import requests
import json
from datetime import date

apiKey = '80caab7e65ab4aa065317a22596e0647'

def new_customer(username, email)
  url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)

  # Build Request payload
  payload = {
    "first_name": username,
    "last_name": email,
    "address": {
      "street_number": "1600",
      "street_name": "Pennsylvania Avenue",
      "city": "Washington",
      "state": "DC",
      "zip": "20500"
    }
  } 
  # Send request
  response = requests.post(url, data=json.dumps(payload),
    headers={'content-type': 'application/json'})
  return response.json()[u'objectCreated'][u'_id']

def new_account(customer_id ):
  url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customer_id,apiKey)

  payload = {
  "type": "Credit Card",
  "nickname": "main card",
  "rewards": 0,
  "balance": 1000,	
  }
  response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)
  return response.json()[u'objectCreated'][u'_id']

def get_account_id(customer_id):
  url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customer_id,apiKey)

  response = requests.get(url)
  return response.json()[u'_id']

def new_purchase(merch_id, account_id, amount):
  url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(account_id,apiKey)

  payload = {
    "merchant_id": merch_id,
    "medium": "balance",
    "purchase_date": date.today().isoformat(),
    "amount": amount,
    "description": "Boost"
  }

  response = requests.post(
    url,
    date=json.dumps(payload),
    headers={'content-type':'application/json'}
  )
  return response.json()[u'objectCreated'][u'_id']