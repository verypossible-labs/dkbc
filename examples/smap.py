#!/bin/bash python3

import os
import sys
import glob
import re
from dkbc.dkbc import DKBC
from dkbc.dkbc_codes import *

r = open(sys.argv[1])
w = open(sys.argv[1].replace(".sch","_tmp.sch"), 'w')

dkbc = DKBC(debug=True)

def process_data(data):
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

    return products[0]

look_for_mpn = 0
look_for_ref = 0
look_for_AR = 0
ref_des_type = 'C'

for line in r:
    if line.find("$Comp") != -1:
        look_for_ref = 1
        w.write(line)
        continue

    if look_for_ref == 1:
        ref_des = line.split(' ')[-1].strip()
        if ref_des.find('?') != -1:
            look_for_AR = 1
        else:
            look_for_mpn = 1
        look_for_ref = 0

    if look_for_AR == 1:
        looking = re.findall('(?<=Ref=)"([^"]\d{1,})', line)
        if len(looking) == 0:
            w.write(line)
            continue
        else:
            ref_des = looking[0]
            look_for_AR = 0
            look_for_ref = 0
            look_for_mpn = 1

    if look_for_mpn == 1 and ref_des.find(ref_des_type) != -1:
        looking = re.findall('"([^"]*)"', line)
        if len(looking) > 1 and looking[1] == "MPN":
            mpn = looking[0]
            look_for_mpn = 0
            if mpn != "DNP":
                data = dkbc.get_part_details(mpn)
                product = process_data(data)
                print("{:10s}\t{:20s}\t{:20.0f}".format(ref_des, product["ManufacturerPartNumber"],product["QuantityAvailable"]))
               # if product["QuantityAvailable"] == 0:
                 #   print("looking for alternative part")
                    #data = dkbc.paramter_search("0", lcr_to_codes('r', 'u10k', ['Package,0402','Tolerance,1']))
                    #product = process_data(data)
                    #print("{:30.30s}\t{:20s}\t{:<10,.0f}\t{:35s}\t{:^20.2f}".format(product["Manufacturer"]["Value"], product["ManufacturerPartNumber"], product["QuantityAvailable"], product["ProductDescription"], product["StandardPricing"][0]["UnitPrice"]))         

    w.write(line)

r.close()
w.close()
