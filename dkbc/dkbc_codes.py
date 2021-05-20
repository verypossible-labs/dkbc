# Digikey uses different code ints and strings as ParametricFilter values
# These were captured using a combination of the codes listed in their docs:
# https://developer.digikey.com/products/product-information/partsearch/keywordsearch
# as well as searching for vague keywords and inspecting the returned values.

#ParameterId
PID = {
    "Package" : 16,
    "Category" : -8,
    "Family" : -2,
    "Part_status" : 1989,

    "Capacitance" : 2049,
    "Resistance" : 2085,
    "Voltage_rated" : 14,
    "Inductance" : 2087,

    "Temperature_coefficient" : 17,
    "Tolerance" : 3
}


#ValueId
VID = {
    "Package" : {
        "0402" : "39158",
        "0603" : "39246",
        "0805" : "39328",
        "1206" : "83711",
        "1210" : "84460",
        },
    "Category" : {
        "Chip_resistor" : "52",
        "Ceramic_capacitor" : "60",
        "Ferrite_beads" : "841",
        "Fixed_Inductors" : "71",
        "IC" : "32"
    },
    "Voltage_rated" : {
        "4V" : "228504",
        "6.3V" : "252155",
        "10V" : "74515",
        "16V" : "108742",
        "25V" : "159247",
        "35V" : "194844",
        "50V" : "238738",
        "100V" : "69629"
    }
}


def lcr_to_codes(lcr, value, *args):
    search = []
    if lcr == "c":
        search.extend(
            [{"ParameterId": PID["Category"],
            "ValueId": VID["Category"]["Ceramic_capacitor"]},
            {"ParameterId": PID["Capacitance"],
            "ValueId": value}])

    elif lcr == 'r':
        search.extend(
            [{"ParameterId": PID["Category"],
            "ValueId": VID["Category"]["Chip_resistor"]},
            {"ParameterId": PID["Resistance"],
            "ValueId": value}])

    if len(args) > 0:
        for a in args[0]:
            b = a.split(',')
            search.append(
                {"ParameterId": PID[b[0]],
                "ValueId": VID[b[0]][b[1]]})
    
    return search
