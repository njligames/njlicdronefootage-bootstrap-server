#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe

is_test = True

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

aerial_service = 'aerial'
construction_service = 'construction'
real_estate_service = 'realestate'

basic_package = 'Basic'
standard_package = 'Standard'
premium_package = 'Premium'

test_prices = {
    aerial_service : {
        basic_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        standard_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        premium_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        }
    },
    construction_service : {
        basic_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        standard_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        premium_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        }
    },
    real_estate_service : {
        basic_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "4" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "5" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "6" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        standard_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "4" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "5" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "6" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        },
        premium_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "3" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "4" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "5" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "6" : 'price_1NfUA7ArNcC9EQIosKcP5x1E'
        }
    },
}

if is_test:
    # This is your test secret API key.
    stripe.api_key = 'sk_test_51Nf6gzArNcC9EQIodukPjdNFlC41NJW2o1lupjvp48BAgkJtoLlzEEhrW1GeYcdTBPHvmqi6Rf3XeHBLNaDnPv5U0023xHLljU'
    the_prices = test_prices
else:
    # This is your test secret API key.
    stripe.api_key = 'sk_test_51Nf6gzArNcC9EQIodukPjdNFlC41NJW2o1lupjvp48BAgkJtoLlzEEhrW1GeYcdTBPHvmqi6Rf3XeHBLNaDnPv5U0023xHLljU'
    the_prices = test_prices

def get_item(quantity, service, size, package):

    packages = the_prices[service]

    if package == standard_package:
        if quantity < 5:
            return None
    if package == premium_package:
        if quantity < 11:
            return None

    if None != packages:

        sizes = packages[package]
        if None != sizes:

            price = sizes[size]
            if None != price:
                return [
                    {
                        'price': price,
                        'quantity': quantity,
                    },
                ]

    return None

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    line_items = None
    if request.method == 'POST':
        package = request.form.get('package')

        if None != package:
            quantity = request.form.get('quantity' + package.capitalize())
            service = request.form.get('service')
            size = request.form.get('dropBox' + package.capitalize() + 'Modal')

            print(quantity, service, size)

            if None != quantity and None != service and None != size:
                line_items = get_item(int(quantity), service, size, package)


    if None != line_items:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
                automatic_tax={'enabled': True}
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)

    return "Record not found", 400


if __name__ == '__main__':
    app.run(port=4242)
