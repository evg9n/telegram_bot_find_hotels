from datetime import datetime
from sqlite3 import connect
from utils.misc.url import path_base
from typing import Dict, Union, Optional, List


def add_user(user_id: Union[str, int]) -> None:

    with connect(path_base) as base:
        base_connect = base.cursor()
        base_connect.execute(f"""CREATE TABLE IF NOT EXISTS history_{user_id} (
            date TEXT,
            hotel_id TEXT,
            time TEXT,
            check_in TEXT,
            check_out TEXT,
            info TEXT,
            url TEXT,
            photo TEXT,
            coordinate_lat TEXT,
            coordinate_lon TEXT
        )""")

        base_connect.execute(f"""CREATE TABLE IF NOT EXISTS favorite_{user_id} (
                    hotel_id TEXT,
                    name TEXT,
                    info TEXT,
                    url TEXT,
                    photo TEXT,
                    coordinate_lat TEXT,
                    coordinate_lon TEXT
                )""")

        base_connect.execute(f"""CREATE TABLE IF NOT EXISTS settings (
            user_id TEXT,
            currency TEXT,
            sort TEXT,
            min_guest_rating TEXT,
            star_rating TEXT,
            min_price TEXT,
            max_price TEXT,
            adults TEXT,
            children TEXT,
            amenity TEXT,
            min_distance TEXT,
            max_distance TEXT
        )""")

        base_connect.execute(f"SELECT * FROM settings WHERE user_id = '{user_id}'")
        if not base_connect.fetchall():
            base.execute(f"""INSERT INTO settings 
                                (user_id, currency, sort, min_guest_rating, star_rating,
                                min_price, max_price, adults, children, amenity, min_distance, max_distance) 
                VALUES ('{user_id}', 'RUB', 'PRICE', 0, 0, 0, 0, 1, 0, 0, '-', '-')
            """)

        base_connect.execute(f"""CREATE TABLE IF NOT EXISTS chat_{user_id} (
            username TEXT,
            message TEXT,
            time TEXT            
            )""")


def get_settings(user_id: Union[str, int]) -> Dict:
    with connect(path_base) as base:
        base_connect = base.cursor()
        data = base_connect.execute(f"SELECT * FROM settings WHERE user_id = '{str(user_id)}'").fetchone()

        if not data:
            result = dict()
        else:
            result = {
                'currency': data[1],
                'sort': data[2],
                'min_guest_rating': data[3],
                'star_rating': data[4],
                'min_price': data[5],
                'max_price': data[6],
                'adults': data[7],
                'children': data[8],
                'amenity': data[9],
                'min_distance': data[10],
                'max_distance': data[11],
            }

    return result


def write_chat(user_id: Union[str, int], username: str, message: str) -> None:
    with connect(path_base) as base:
        base_connect = base.cursor()
        base_connect.execute(f"""INSERT INTO chat_{str(user_id)} VALUES
            ('{username}', '{message}', '{datetime.now().strftime("%d.%m.%Y %H:%M")}')
        """)


def write_history(user_id: Union[str, int], hotel_id: str, check_in: str, check_out: str,
                  info: str, url: str, photo: str, coordinate_lat: str, coordinate_lon: str) -> None:
    with connect(path_base) as base:
        base_connect = base.cursor()
        base_connect.execute(f"""INSERT INTO history_{str(user_id)} VALUES
            ("{datetime.now().strftime("%d.%m.%Y")}", "{hotel_id}", "{datetime.now().strftime("%H:%M")}", 
            "{check_in}", "{check_out}", "{info}", "{url}", "{photo}", 
            "{coordinate_lat}", "{coordinate_lon}")
        """)


def write_favorite(user_id: Union[str, int], hotel_id: str, info: str, url: str,
                   photo: str, coordinate_lat: str, coordinate_lon: str) -> None:
    with connect(path_base) as base:
        name  = info[7:info.find('\n')]
        base_connect = base.cursor()
        base_connect.execute(f"""INSERT INTO favorite_{str(user_id)} VALUES
            ("{hotel_id}", "{name}", "{info}", "{url}", "{photo}", 
            "{coordinate_lat}", "{coordinate_lon}")
        """)


def check_hotel_favorite(user_id: Union[str, int], hotel_id: str) -> bool:
    with connect(path_base) as base:
        base_connect = base.cursor()
        data = base_connect.execute(f"""SELECT (hotel_id) FROM favorite_{str(user_id)}
                WHERE hotel_id = '{hotel_id}' 
                """).fetchone()

        return True if data else False


def delet_favorite(user_id: Union[str, int], hotel_id: str) -> None:
    with connect(path_base) as base:
        base_connect = base.cursor()
        base_connect.execute(f"DELETE FROM favorite_{str(user_id)} WHERE hotel_id = {hotel_id}")


def get_favorite(user_id: Union[int, str]) -> Optional[List[Dict]]:
    with connect(path_base) as base:
        result = list()
        base_connect = base.cursor()
        data = base_connect.execute(f"SELECT * FROM favorite_{str(user_id)}").fetchall()
        if not data:
            return None
        for favorite in data:
            element = {
                'hotel_id': favorite[0],
                'name': favorite[1],
                'info': favorite[2],
                'url': favorite[3],
                'photo': favorite[4],
                'coordinate': {'lat': favorite[5], 'lon': favorite[6]}
            }
            result.append(element)

        return result


def get_history(user_id: Union[str, int]) -> Optional[Dict]:
    with connect(path_base) as base:
        result = dict()
        base_connect = base.cursor()
        data = base_connect.execute(f"SELECT * FROM history_{str(user_id)}").fetchall()
        if not data:
            return None
        for element in data:
            if element[0] in result:
                result[element[0]].append(element[2:])
            else:
                result[element[0]] = [element[2:]]

    return result


def update_settings(user_id: str, setting: str, value: str) -> None:
    with connect(path_base) as base:
        base_connect = base.cursor()
        base_connect.execute(f"""UPDATE settings
                                SET '{setting}' = '{value}'
                                WHERE user_id = {user_id}""")
