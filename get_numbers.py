#!/usr/bin/env python2

from prettytable import PrettyTable
from twilio.rest import Client

import os

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN  = os.environ["TWILIO_AUTH_TOKEN"]

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
TABLE = PrettyTable()

TABLE.field_names = [
        "Account",
        "Name",
        "Number",
        "customer_name",
        "friendly_name",
        "country",
        "region",
        "postal_code",
        "street",
        "validated"
]

TABLE.sortby = "Name"

for account in CLIENT.api.accounts.list(status='active'):
    client = Client(ACCOUNT_SID, AUTH_TOKEN, account.sid)

    for number in client.incoming_phone_numbers.list():
        if number.address_requirements != 'none':
            account = client.api.accounts(number.account_sid).fetch()

            if number.address_sid:
                address = client.addresses(number.address_sid).fetch()
                customer_name = address.customer_name
                friendly_name = address.friendly_name
                country = address.iso_country
                region = address.region
                postal_code = address.postal_code
                street = address.street
                validated = address.validated
            else:
                address = None
                customer_name = None
                friendly_name = None
                country = None
                region = None
                postal_code = None
                street = None
                validated = None

            TABLE.add_row(
                    [
                        account.friendly_name,
                        number.friendly_name,
                        number.phone_number,
                        customer_name,
                        friendly_name,
                        country,
                        region,
                        postal_code,
                        street,
                        validated
                    ]
            )

print(TABLE)
