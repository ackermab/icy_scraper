import json

from icy_veins_scraper import HEROES, MAPS

hero_data = {}
with open('heroes_output.json') as f:
    hero_data = json.loads(f.read())

for hero in HEROES:
    print(f'{hero}')
    is_countered_by = hero_data[hero]['counters']
    is_countered_by_str = ', '.join(is_countered_by)
    print(f'---- is countered by: {is_countered_by_str}')

    counters = []

    for hero_name, hero_dict in hero_data.items():
        if hero in hero_dict['counters']:
            counters.append(hero_name)

    counters_str = ', '.join(counters)
    print(f'---- counters: {counters_str}')
    print('')

for map_name in MAPS:
    stronger_heroes = []
    average_heroes = []
    weaker_heroes = []
    for hero_name, hero_dict in hero_data.items():
        if map_name in hero_dict['stronger_maps']:
            stronger_heroes.append(hero_name)
        if map_name in hero_dict['average_maps']:
            average_heroes.append(hero_name)
        if map_name in hero_dict['weaker_maps']:
            weaker_heroes.append(hero_name)
    print(f'{map_name}')

    strong_str = ', '.join(stronger_heroes)
    average_str = ', '.join(average_heroes)
    weak_str = ', '.join(weaker_heroes)

    print(f'---- strong heroes are: {strong_str}')
    print(f'---- averag heroes are: {average_str}')
    print(f'---- weaker heroes are: {weak_str}')
    print('')
