energy_consumption = {
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
       }
water_consumption = {
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
}

def read_materials(materials):
    materials = eval(materials)
    out = map(lambda s: s.split(" "), materials)
    return list(out)

def 
