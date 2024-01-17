import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def regions_btn():
    with open('utils/regions.json', 'r') as f:
        json_data = json.load(f)

    keyboard = []

    for region in json_data:
        # print(region['id'], region['name_uz'])
        keyboard.append(
            [
                InlineKeyboardButton(
                    region['name_uz'], callback_data=f"region={region['id']}")
            ]
        )
    markup = InlineKeyboardMarkup(keyboard)
    return markup


def district_btn(region_id):
    with open('utils/districts.json', 'r') as f:
        json_data = json.load(f)

    keyboard = []

    for district in json_data:
        if district['region_id'] == region_id:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        district['name_uz'], callback_data=f"district={district['id']}")
                ]
            )

    keyboard.append(
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="district=back")
        ])

    return InlineKeyboardMarkup(keyboard)


def main_btn():
    markup = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("Bugungi ob-havo ⛅️")
            ],
            [
                KeyboardButton("1 haftalik ob-havo ⛅️")
            ],
            [
                KeyboardButton("Manzilni o'zgartirish ✏️")
            ]
            # [
            #     KeyboardButton("1 haftalik ob-have")
            # ],
        ], resize_keyboard=True)
    return markup
