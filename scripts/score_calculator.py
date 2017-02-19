import csv
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

def calculate_score(materials):
    p1 = float(read_materials(materials)[0][0].replace("%",""))/100
    f1 = read_materials(materials)[0][1].lower()
    if len(eval(materials)) == 1:
        score = .5 * water_consumption[f1] + .5 * energy_consumption[f1]
        score = score * .7
    elif len(eval(materials)) == 2:
        f2 = eval(materials)[1].split(" ")[1].lower()
        p2 = float(read_materials(materials)[1][0].replace("%",""))
        score = .25 * water_consumption[f1] + .25 * energy_consumption[f1] + .25 * water_consumption[f2] + .25 * energy_consumption[f2]
        score = score * .7
    elif len(eval(materials)) == 3:
        f2 = eval(materials)[1].split(" ")[1].lower()
        p2 = float(read_materials(materials)[1][0].replace("%",""))
        f3 = eval(materials)[2].split(" ")[1].lower()
        p3 = float(read_materials(materials)[2][0].replace("%",""))
        score = (1/6) * water_consumption[f1] + (1/6) * energy_consumption[f1] + (1/6) * water_consumption[f2] + (1/6) * energy_consumption[f2] + (1/6) * water_consumption[f3] + (1/6) * energy_consumption[f3]
        score = score * .7

