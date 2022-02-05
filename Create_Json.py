"""

This creates JSON files with info about names and prices of skins, background and audio

Skins key and price
Music needs key, branding, and price
Backgrounds need key and price

"""

import json


def add_new_account(account_name):
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

        "snakies": 0,
        "bodies": ["BBS"],
        "foods": ["FBS"],
        "backgrounds": ["IBS"],
        "soundtracks": ["SBS"],

        "body_in_use": "BBS",
        "food_in_use": "FBS",
        "background_in_use": "IDF",
        "soundtrack_in_use": "SPD",

        "master_in_use": 100,
        "music_in_use": 100,
        "effects_in_use": 100,
        "grid_opacity": 10,
        "score_opacity": 10,
    }

    with open("common/statistics.json", 'w') as jFile:
        json.dump(stats, jFile)


def create_shop_json():
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


if __name__ == '__main__':
    # with open('common/statistics.json', 'r') as f:
    #     file = json.load(f)
    #
    # print(list(file))
    #
    # with open('common/statistics.json', 'w') as f:
    #     json.dump(file, f)

    add_new_account('teasin951')