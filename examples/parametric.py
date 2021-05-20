import argparse
import json
import re
import time
import os
import sys
from dkbc.dkbc import DKBC
from dkbc.dkbc_codes import *
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("--search", "-s", nargs="+", type=str, help="Search for parts with filters")
parser.add_argument("--outfile", help="CSV output file")
parser.add_argument("--batch", action="store_true", help="Batch scan")
parser.add_argument("--debug", action="store_true", help="Debug mode")
args = parser.parse_args()

dkbc = DKBC(debug=True)

if args.search:
    if args.search[1].find('u') != 0:
        args.search[1] = "u" + args.search[1]

#data = dkbc.paramter_search("0",lcr_to_codes("c","u1uF",['Voltage_rated,100V', 'Package,1206']))
data = dkbc.paramter_search("0",lcr_to_codes(args.search[0], args.search[1], args.search[2:]))

if args.debug:
    pprint(data)

if "HttpStatusCode" in data and data["HttpStatusCode"] == 404:
    print(data["Message"])
    print(data["Details"])

if len(data["Products"]) == 0:
    print("Part not found...")
    sys.exit(-1)

#print(len(data["Products"]), "products found")

products = []
for product in data["Products"]:
    if product["MinimumOrderQuantity"] > 1:
        continue

    if "Digi-Reel" in product["Packaging"]["Value"]:
        continue

    products.append(product)

print("{:30s}\t{:20s}\t{:<10s}\t{:35s}\t{:^20s}".format("Manufacturer", "MPN", "Quantity", "ProductDescription", "UnitPrice"))

for product in products:
    print("{:30.30s}\t{:20s}\t{:<10,.0f}\t{:35s}\t{:^20.2f}".format(product["Manufacturer"]["Value"], product["ManufacturerPartNumber"], product["QuantityAvailable"], product["ProductDescription"], product["StandardPricing"][0]["UnitPrice"]))

details = data["Products"][0]