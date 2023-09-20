#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe

is_test = False

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

live_prices = {
    aerial_service : {
        basic_package : {
            "1" : 'price_1No8JOArNcC9EQIoIG4dCx6g',
            "2" : 'price_1No8IyArNcC9EQIoW9C4EzYM',
            "3" : 'price_1No8HlArNcC9EQIo4JVtkT7i'
        },
        standard_package : {
            "1" : 'price_1No8JIArNcC9EQIooy0e6qyq',
            "2" : 'price_1No8IqArNcC9EQIoZNsrpydk',
            "3" : 'price_1No8HQArNcC9EQIohYk945o5'
        },
        premium_package : {
            "1" : 'price_1No8J7ArNcC9EQIoazRuoqX7',
            "2" : 'price_1No8IiArNcC9EQIoqSEca6cp',
            "3" : 'price_1No8H9ArNcC9EQIon48bhnvU'
        }
    },
    construction_service : {
        basic_package : {
            "1" : 'price_1No8PqArNcC9EQIocmZhRxla',
            "2" : 'price_1No8PLArNcC9EQIo3VH1jj7Y',
            "3" : 'price_1No8OaArNcC9EQIoibYDguIb'
        },
        standard_package : {
            "1" : 'price_1No8PgArNcC9EQIo9eTwf4G3',
            "2" : 'price_1No8P8ArNcC9EQIoeh4qODoC',
            "3" : 'price_1No8OMArNcC9EQIo6qQ0DCtr'
        },
        premium_package : {
            "1" : 'price_1No8PXArNcC9EQIoHrnfvYrb',
            "2" : 'price_1No8OuArNcC9EQIoSYFZ7amX',
            "3" : 'price_1No8O5ArNcC9EQIoRKrM6KwU'
        }
    },
    real_estate_service : {
        basic_package : {
            "1" : 'price_1No8N3ArNcC9EQIoncoq39Ko',
            "2" : 'price_1No8MSArNcC9EQIoJlXY0SoR',
            "3" : 'price_1No8LiArNcC9EQIoU5mgfI4Y',
            "4" : 'price_1No8L3ArNcC9EQIozEUAAZTP',
            "5" : 'price_1No8KGArNcC9EQIolaPFBi5k',
            "6" : 'price_1No8JoArNcC9EQIoBItCNEz4'
        },
        standard_package : {
            "1" : 'price_1No8MrArNcC9EQIoiVvItTDf',
            "2" : 'price_1No8MHArNcC9EQIoUcL8IQsy',
            "3" : 'price_1No8LPArNcC9EQIoyiRmD2tQ',
            "4" : 'price_1No8KqArNcC9EQIoXtLgLTs4',
            "5" : 'price_1No8K6ArNcC9EQIorzjQBRyd',
            "6" : 'price_1No8JhArNcC9EQIoKGW1mg9i'
        },
        premium_package : {
            "1" : 'price_1No8MhArNcC9EQIo8KDJ2Azr',
            "2" : 'price_1No8LzArNcC9EQIoEDes2hBU',
            "3" : 'price_1No8LFArNcC9EQIoiu41PXpR',
            "4" : 'price_1No8KXArNcC9EQIoAptLRBs7',
            "5" : 'price_1No8JxArNcC9EQIooVVqgcvz',
            "6" : 'price_1No8JaArNcC9EQIoZ5v63ww8'
        }
    },
}

if is_test:
    # This is your test secret API key.
    stripe.ap.key = os.environ["STRIPE_SECRET_KEY_TEST"]
    the_prices = test_prices
else:
    # This is your test secret API key.
    stripe.ap.key = os.environ["STRIPE_SECRET_KEY_LIVE"]
    the_prices = live_prices

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
