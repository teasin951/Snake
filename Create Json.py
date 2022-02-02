"""

This creates JSON files with info about names and prices of skins, background and audio

Skins key and price
Music needs key, branding, and price
Backgrounds need key and price

"""

import json

shop = {
    "skins": {
        "BBS": 0,
        "BRD": 1000,
        "BJG": 3000,
        "FBS": 0
    },

    "music": {
        "SPD": {
            "branding": "Payday Soundtrack",
            "price": 8000
        },
        "SBS": {
            "branding": "Snake Original",
            "price": 0
        }
    },

    "background": {
        "IBS": 0,
        "IDF": 5000
    }
}

with open("resources/shopsheet.json", 'w') as jFile:
    json.dump(shop, jFile)
