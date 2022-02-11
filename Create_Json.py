"""

This creates JSON files with all information necessary for main.py to work

I have separated this file for easier access and editing of any given information

"""

import json
from cryptography.fernet import Fernet


def add_new_account(account_name, key):
    stats = {
        "account_name": "{}".format(account_name),

        "easy_best": 0,
        "normal_best": 0,
        "hard_best": 0,
        "impossible_best": 0,

        "easy_games": 0,
        "normal_games": 0,
        "hard_games": 0,
        "impossible_games": 0,

        "easy_food": 0,
        "normal_food": 0,
        "hard_food": 0,
        "impossible_food": 0,

        "easy_playtime": 0,
        "normal_playtime": 0,
        "hard_playtime": 0,
        "impossible_playtime": 0,

        "easy_snakies": 0,
        "normal_snakies": 0,
        "hard_snakies": 0,
        "impossible_snakies": 0,

        "snakies": 10000,
        "bodies": ["BBS"],
        "foods": ["FBS"],
        "backgrounds": ["IBS"],
        "soundtracks": ["SBS"],

        "body_in_use": "BBS",
        "food_in_use": "FBS",
        "background_in_use": "IBS",
        "soundtrack_in_use": "SPD",  # TODO put this back to default!!

        "master_in_use": 30,
        "music_in_use": 0,
        "effects_in_use": 50,
        "grid_opacity": 3,
        "score_opacity": 12,
    }

    fernet = Fernet(key)

    original = json.dumps(stats)
    en_file = fernet.encrypt(bytes(original, 'utf-8'))

    with open("common/statistics.json", 'wb') as jFile:
        jFile.write(en_file)


def create_shop_json(key):
    shop = {
        "skins": {
            "BBS": 0,
            "BRD": 1000,
            "BJG": 3000,
            "FBS": 0
        },

        "music": {
            "SBS": {
                "branding": "Snake Original",
                "price": 0
            },
            "SPD": {
                "branding": "Payday Soundtrack",
                "price": 8000
            }
        },

        "background": {
            "IBS": 0,
            "IDF": 5000,
            "ILR": 6000
        }
    }

    fernet = Fernet(key)

    original = json.dumps(shop)
    en_file = fernet.encrypt(bytes(original, 'utf-8'))

    with open("resources/shopsheet.json", 'wb') as jFile:
        jFile.write(en_file)


if __name__ == '__main__':
    create_shop_json('tNXSr3w1v29_cBJhhN16BXNh_nVu7pmtD61KYnfmwK4=')  # TODO remove in the final version
    add_new_account('teasin951', 'tNXSr3w1v29_cBJhhN16BXNh_nVu7pmtD61KYnfmwK4=')
