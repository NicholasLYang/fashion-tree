import csv
from collections import Counter
energy_consumption = Counter({
       'cotton': 49,
       'wool': 8,
       'polyester': 109,
       'viscose': 71,
       'spandex': 135,
       'rayon': 68,
       'acrylic': 2,
       'nylon': 68,
       'metallic fiber': 536,
       'lyocell': 36,
       })
water_consumption = Counter({
    'cotton': 12500,
    'wool': 125,
    'polyester': 0,
    'viscose': 640,
    'spandex': 26,
    'rayon': 190,
    'acrylic': 2,
    'nylon': 2,
    'metallic fiber': 12,
    'lyocell':12
})

def read_materials(materials):
    out = map(lambda s: reversed(s.split(" ")), materials)
    try:
        return dict(list(out))
    except ValueError:
        return None

def calculate_score(materials):
    if materials == None:
        return None
    out = 0.1
    for key in materials:
        val = int(materials[key][:-1])
        out = out + (val * water_consumption[key.lower()] +
                     val * energy_consumption[key.lower()])/2
    return (627450/out + 20)/2


def main(materials):
    return calculate_score(read_materials(materials))

