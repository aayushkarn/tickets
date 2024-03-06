import json

from flask import url_for
from main.config import Config
import requests
from ..utils import DateTimeEncoder, generatePaymentInfo

# def initKhalti(return_url, website_url, amount, purchase_order_id, purchase_order_name, customer_info=None, amount_breakdown=None, product_details=None):
#     url = Config.KHALTI_BASE_URL+"/epayment/initiate/"
#     return_url = return_url
#     website_url = website_url
#     amount = amount*100
#     purchase_order_id = purchase_order_id

#     data={
#         "return_url": return_url,
#         "website_url": website_url,
#         "amount": amount,
#         "purchase_order_id": purchase_order_id,
#         "purchase_order_name": purchase_order_name,
#         "customer_info":customer_info,
#         amount_breakdown:amount_breakdown,
#         "product_details":product_details,
#         "public_key":Config.KHALTI_PUBLIC_KEY,
#     }

#     payload = json.dumps(data, cls=DateTimeEncoder)

#     headers = {
#         'Authorization': f"key {Config.KHALTI_SECRET_KEY}",
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers,data=payload)

#     return response.text


def initkhalti():
    info = generatePaymentInfo()
    url = Config.KHALTI_BASE_URL + "epayment/initiate/"
    return_url = url_for("payment.khalti.finalize_payment", _scheme="http")
    website_url = url_for("home.index", _scheme="http")
    amount = info['totalPrice']*100
    purchase_order_id = info['uniqueid']

    product_details=[]
    for movie in info['movieInfo']:
        product_details.append({
            "identity":movie['seat_id'],
            "unit_price":movie['price'],
            "total_price":movie['price'],
            "quantity":1,
            "seat_id":movie['seat_id'],
            "name":movie['title'],
            "duration":movie['duration'],
            "date":movie['date'],
            "time":movie['time'],
            "screen":movie['screen']
        })
    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_id,
        "customer_info": {
            "name":info['name'],
            "email":info['email']
        },
        "product_details":product_details
    }, cls=DateTimeEncoder)

    headers = {
        'Authorization': f'key {Config.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(json.loads(response.text))


    return json.loads(response.text)


def verifyPayment(pidx):
    url = Config.KHALTI_BASE_URL+'epayment/lookup/'
    pidx = pidx
    data = json.dumps({
        "pidx":pidx
    })

    headers = {
        'Authorization': f'key {Config.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", url, headers=headers, data=data)
    res = json.loads(response.text)
    return res