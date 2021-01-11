import json
from bs4 import BeautifulSoup
from urllib import request

ICY_URL = 'https://www.icy-veins.com/heroes/'
DIV_CLASS_S = 'heroes_synergies'
DIV_CLASS_C = 'heroes_counters'

DIV_CLASS_MAP_S = 'heroes_maps_stronger'
DIV_CLASS_MAP_A = 'heroes_maps_average'
DIV_CLASS_MAP_W = 'heroes_maps_weaker'

HEROES = {
    'stukov', 'ana', 'rehgar', 'probius', 'li-li', 'samuro', 'zeratul', 'uther', 'malfurion', 'genji', 'lunara', 'raynor', 'zagara', 'hogger', 'brightwing', 'cassia', 'mephisto', 'qhira', 'gazlowe', 'yrel', 'tychus', 'garrosh', 'nazeebo', 'arthas', 'artanis', 'alarak', 'tracer', 'lucio', 'hanzo', 'varian', 'johanna', 'rexxar', 'zarya', 'deckard', 'tyrande', 'azmodan', 'zuljin', 'sonya', 'orphea', 'blaze', 'muradin', 'valla', 'abathur', 'lt-morales', 'deathwing', 'junkrat', 'sylvanas', 'greymane', 'illidan', 'malthael', 'guldan', 'medivh', 'gall', 'anubarak', 'dehaka', 'thrall', 'alexstrasza', 'maiev', 'falstad', 'tyrael', 'the-butcher', 'fenix', 'cho', 'chromie', 'imperius', 'li-ming', 'kaelthas', 'malganis', 'diablo', 'tassadar', 'anduin', 'sgt-hammer', 'murky', 'valeera', 'auriel', 'whitemane', 'kharazim', 'dva', 'ragnaros', 'stitches', 'kerrigan', 'nova', 'jaina', 'mei', 'e-t-c', 'chen', 'the-lost-vikings', 'kel-thuzad', 'leoric', 'xul'
}
MAPS = {
    'map-tomb-of-the-spider-queen',
    'map-sky-temple',
    'map-warhead-junction',
    'map-infernal-shrines',
    'map-towers-of-doom',
    'map-blackhearts-bay',
    'map-hanamura-temple',
    'map-dragon-shire',
    'map-garden-of-terror',
    'map-volskaya-foundry',
    'map-battlefield-of-eternity',
    'map-alterac-pass',
    'map-braxis-holdout',
    'map-cursed-hollow'
}

def get_build_guide_sections(hero):
    html = request.urlopen(f'{ICY_URL}{hero}-build-guide').read()
    soup = BeautifulSoup(html, 'html.parser')

    synergies = set()
    counters = set()
    stronger_maps = set()
    average_maps = set()
    weaker_maps = set()

    div_s = soup.find('div', {'class': DIV_CLASS_S})
    for img in div_s.find_all('img', {'data-heroes-tooltip': True}):
        synergies.add(img['data-heroes-tooltip'].split('hero-')[1])

    div_c = soup.find('div', {'class': DIV_CLASS_C})
    for img in div_c.find_all('img', {'data-heroes-tooltip': True}):
        counters.add(img['data-heroes-tooltip'].split('hero-')[1])

    div_ms = soup.find('div', {'class': DIV_CLASS_MAP_S})
    for span in div_ms.find_all('span', {'data-heroes-tooltip': True}):
        stronger_maps.add(span['data-heroes-tooltip'])

    div_ma = soup.find('div', {'class': DIV_CLASS_MAP_A})
    for span in div_ma.find_all('span', {'data-heroes-tooltip': True}):
        average_maps.add(span['data-heroes-tooltip'])

    div_mw = soup.find('div', {'class': DIV_CLASS_MAP_W})
    for span in div_mw.find_all('span', {'data-heroes-tooltip': True}):
        weaker_maps.add(span['data-heroes-tooltip'])

    return synergies, counters, stronger_maps, average_maps, weaker_maps

if __name__ == '__main__':
    all_data = {}
    for hero in HEROES:
        print(f'Trying to get {hero}')
        s, c, ms, ma, mw = get_build_guide_sections(hero)
        all_data[hero] = {
            'synergies': s,
            'counters': c,
            'stronger_maps': ms,
            'average_maps': ma,
            'weaker_maps': mw
        }
        print(f'Got: {hero} - ex {s}')


    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        return TypeError

    with open('heroes_output.json', 'w') as f:
        f.write(json.dumps(all_data, indent=2, default=set_default))
