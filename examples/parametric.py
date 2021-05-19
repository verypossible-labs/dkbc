import argparse
import re
import time
import os
import sys
from dkbc.dkbc import DKBC
from dkbc.dkbc_codes import *
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("--search", action="store_true", help="Search for parts with filters")
parser.add_argument("--outfile", help="CSV output file")
parser.add_argument("--batch", action="store_true", help="Batch scan")
parser.add_argument("--debug", action="store_true", help="Debug mode")
args = parser.parse_args()

dkbc = DKBC(debug=True)

#data = dkbc.paramter_search("0",lcr_to_codes("c","u1uF",["Voltage_rated","6.3V"],["Package","0402"]))
data = dkbc.paramter_search("0",lcr_to_codes("r","u30k",["Package","0402"]))

if args.debug:
    pprint(data)

if "HttpStatusCode" in data and data["HttpStatusCode"] == 404:
    print(data["Message"])
    print(data["Details"])

if len(data["Products"]) == 0:
    print("Part not found...")
    sys.exit(-1)

print(len(data["Products"]), "products found")

products = []
for product in data["Products"]:
    if product["MinimumOrderQuantity"] > 1:
        continue

    if "Digi-Reel" in product["Packaging"]["Value"]:
        continue

    products.append(product)

for product in products:
    print("\t\t\t".join([product["ManufacturerPartNumber"], str(product["QuantityAvailable"]), product["ProductDescription"]]))

details = data["Products"][0]

print(details["ManufacturerPartNumber"] + "     " + details["ProductDescription"])
