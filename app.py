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
    # price_1NjtmdArNcC9EQIoRhEDtn6M	prod_OWxiNkkrN1Cw6c	Aerial Photography - Size A - Basic
    # price_1NjtoVArNcC9EQIoIazH2aVb	prod_OWxjLHwXiBxo1I	Aerial Photography - Size B - Basic
    # price_1NjtsmArNcC9EQIoHmpK7NRZ	prod_OWxosjxyBhO3QI	Aerial Photography - Size C - Basic
    #
    # price_1NjtnXArNcC9EQIoClfEjHRI	prod_OWxiICuJBrcz3e	Aerial Photography - Size A - Standard
    # price_1NjtoxArNcC9EQIoV2O7Jgld	prod_OWxkfH4GVXqFNz	Aerial Photography - Size B - Standard
    # price_1NjttrArNcC9EQIomdKDBxV4	prod_OWxpCKbrS4q4Pw	Aerial Photography - Size C - Standard
    #
    # price_1NjtnuArNcC9EQIo7KLgsEH4	prod_OWxjdtfjmpf548	Aerial Photography - Size A - Premium
    # price_1NjtreArNcC9EQIoOTmZSycp	prod_OWxnolnOa1n44q	Aerial Photography - Size B - Premium
    # price_1NjtuJArNcC9EQIo6aka48LO	prod_OWxpDDEPMhZ4LN	Aerial Photography - Size C - Premium
    aerial_service : {
        basic_package : {
            "1" : 'price_1NjtmdArNcC9EQIoRhEDtn6M',
            "2" : 'price_1NjtoVArNcC9EQIoIazH2aVb',
            "3" : 'price_1NjtsmArNcC9EQIoHmpK7NRZ'
        },
        standard_package : {
            "1" : 'price_1NjtnXArNcC9EQIoClfEjHRI',
            "2" : 'price_1NjtoxArNcC9EQIoV2O7Jgld',
            "3" : 'price_1NjttrArNcC9EQIomdKDBxV4'
        },
        premium_package : {
            "1" : 'price_1NjtnuArNcC9EQIo7KLgsEH4',
            "2" : 'price_1NjtreArNcC9EQIoOTmZSycp',
            "3" : 'price_1NjtuJArNcC9EQIo6aka48LO'
        }
    },
    # price_1NfUA7ArNcC9EQIosKcP5x1E	prod_OSOyhwHtskPssu	Construction - Size A - Basic
    # price_1Njt4rArNcC9EQIo0dZWMGIB	prod_OWwyLxpcJrSeba	Construction - Size B - Basic
    # price_1NjtHoArNcC9EQIo8SjQH5lx	prod_OWxCfcQEjOBsfS	Construction - Size C - Basic
    #
    # price_1NfUARArNcC9EQIo8fvzF4q9	prod_OSOyYherLST7v6	Construction - Size A - Standard
    # price_1NjtGEArNcC9EQIoBbpK9q87	prod_OWxALHYsGVtrBJ	Construction - Size B - Standard
    # price_1NjtIqArNcC9EQIoNBrn05bJ	prod_OWxD38YvInZ7nI	Construction - Size C - Standard
    #
    # price_1NfUArArNcC9EQIoPBnXN6qS	prod_OSOyp2earCJ6jV	Construction - Size A - Premium
    # price_1NjtGsArNcC9EQIoIXj2jhvn	prod_OWxBDgAHzAMrJy	Construction - Size B - Premium
    # price_1NjtJPArNcC9EQIo9YZgiVcs	prod_OWxDzFQd90Xzwk	Construction - Size C - Premium
    construction_service : {
        basic_package : {
            "1" : 'price_1NfUA7ArNcC9EQIosKcP5x1E',
            "2" : 'price_1Njt4rArNcC9EQIo0dZWMGIB',
            "3" : 'price_1NjtHoArNcC9EQIo8SjQH5lx'
        },
        standard_package : {
            "1" : 'price_1NfUARArNcC9EQIo8fvzF4q9',
            "2" : 'price_1NjtGEArNcC9EQIoBbpK9q87',
            "3" : 'price_1NjtIqArNcC9EQIoNBrn05bJ'
        },
        premium_package : {
            "1" : 'price_1NfUArArNcC9EQIoPBnXN6qS',
            "2" : 'price_1NjtGsArNcC9EQIoIXj2jhvn',
            "3" : 'price_1NjtJPArNcC9EQIo9YZgiVcs'
        }
    },
    # price_1NjtVRArNcC9EQIoCst4phSW	prod_OWxQWDpihyvy2S	Real Estate - Size A - Basic
    # price_1NjtXHArNcC9EQIodKBCuFPw	prod_OWxSTU20GoVaI1	Real Estate - Size B - Basic
    # price_1NjtZZArNcC9EQIoB7jN3dfl	prod_OWxUgdHwm6IQ2B	Real Estate - Size C - Basic
    # price_1NjtcEArNcC9EQIov6bUtSqc	prod_OWxXkYXF2qBfJ4	Real Estate - Size D - Basic
    # price_1NjtdpArNcC9EQIoCpKT6L63	prod_OWxY9b84y0dRJs	Real Estate - Size E - Basic
    # price_1NjtgoArNcC9EQIoXUnH1mAq	prod_OWxcju1xhloHTL	Real Estate - Size F - Basic
    #
    # price_1NjtVuArNcC9EQIoesFiqEdS	prod_OWxQmVJi6MMyuy	Real Estate - Size A - Standard
    # price_1NjtXuArNcC9EQIoN20BNDub	prod_OWxS0zJTck10sM	Real Estate - Size B - Standard
    # price_1NjtaXArNcC9EQIo9zTUJAVo	prod_OWxV5kZMSZzF3n	Real Estate - Size C - Standard
    # price_1NjtcrArNcC9EQIoll88TN6T	prod_OWxXW9tfc6Zo9F	Real Estate - Size D - Standard
    # price_1NjtfEArNcC9EQIouBX0iHef	prod_OWxa5j1lWS5Qc7	Real Estate - Size E - Standard
    # price_1NjthKArNcC9EQIoNgFcmSal	prod_OWxcKA5oa6mWPX	Real Estate - Size F - Standard
    #
    # price_1NjtWNArNcC9EQIo1Lyys1if	prod_OWxROgQjrHEnON	Real Estate - Size A - Premium
    # price_1NjtYXArNcC9EQIoSGFtr67O	prod_OWxTyt341s8wWv	Real Estate - Size B - Premium
    # price_1Njtb7ArNcC9EQIoutVZyJw0	prod_OWxWUEj24Dhnms	Real Estate - Size C - Premium
    # price_1NjtdHArNcC9EQIovxqSidzA	prod_OWxYeJaPGJ4oL9	Real Estate - Size D - Premium
    # price_1NjtgFArNcC9EQIo157h4Rjc	prod_OWxbG8znF0S7vU	Real Estate - Size E - Premium
    # price_1Njti9ArNcC9EQIov3Oytb9u	prod_OWxdcu8scT2Eno	Real Estate - Size F - Premium
    real_estate_service : {
        basic_package : {
            "1" : 'price_1NjtVRArNcC9EQIoCst4phSW',
            "2" : 'price_1NjtXHArNcC9EQIodKBCuFPw',
            "3" : 'price_1NjtZZArNcC9EQIoB7jN3dfl',
            "4" : 'price_1NjtcEArNcC9EQIov6bUtSqc',
            "5" : 'price_1NjtdpArNcC9EQIoCpKT6L63',
            "6" : 'price_1NjtgoArNcC9EQIoXUnH1mAq'
        },
        standard_package : {
            "1" : 'price_1NjtVuArNcC9EQIoesFiqEdS',
            "2" : 'price_1NjtXuArNcC9EQIoN20BNDub',
            "3" : 'price_1NjtaXArNcC9EQIo9zTUJAVo',
            "4" : 'price_1NjtcrArNcC9EQIoll88TN6T',
            "5" : 'price_1NjtfEArNcC9EQIouBX0iHef',
            "6" : 'price_1NjthKArNcC9EQIoNgFcmSal'
        },
        premium_package : {
            "1" : 'price_1NjtWNArNcC9EQIo1Lyys1if',
            "2" : 'price_1NjtYXArNcC9EQIoSGFtr67O',
            "3" : 'price_1Njtb7ArNcC9EQIoutVZyJw0',
            "4" : 'price_1NjtdHArNcC9EQIovxqSidzA',
            "5" : 'price_1NjtgFArNcC9EQIo157h4Rjc',
            "6" : 'price_1Njti9ArNcC9EQIov3Oytb9u'
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

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
