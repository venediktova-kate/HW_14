import sqlite3

from flask import jsonify


def get_all(query: str):
    with sqlite3.connect('netflix.db') as con:
        con.row_factory = sqlite3.Row
        result = []

        for item in con.execute(query).fetchall():
            s = dict(item)

            result.append(s)

        return result


def get_one(query: str):
    with sqlite3.connect('netflix.db') as con:
        con.row_factory = sqlite3.Row
        res = con.execute(query).fetchone()

        if res is None:
            return None
        else:
            return dict(res)


def search_by_cast(name1: str = 'Rose McIver', name2: str = 'Ben Lamb'):
    query = f"""
                SELECT `cast` 
                FROM netflix
                WHERE `cast` LIKE '%{name1}%' AND `cast` LIKE '%{name2}%'
            """

    cast = []
    result = get_all(query)

    for item in result:
        list_cast = item['cast'].split(", ")
        cast.extend(list_cast)

    cast_result = [x for x in cast if cast.count(x) > 2]
    cast_result = list(set(cast_result))
    return cast_result


def search_by_three_input(type_n: str = 'Movie', release_year: int = 2016, listed_in: str = 'Dramas'):
    query = f"""
                SELECT `title`, description
                FROM netflix
                WHERE `type` = '{type_n}' 
                AND release_year = {release_year} 
                AND listed_in LIKE '%{listed_in}%'
    """

    result = get_all(query)
    return jsonify(result)
