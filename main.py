import csv
import requests
import collections


# constantes
INDEX_NAMES = 3
INDEX_CATEGORY = 17
INDEX_NUM_VOTES = 12
INDEX_IMAGE_URL = 13
INDEX_MAX_PLAYERS = 5


def is_cardgame_for_less_than3(category, players):
    """Retorna True si es juego de cartas para menos de 3 personas."""
    return 'Card Game' in category.split(', ') and int(players) < 3


def save_image(url, game_name):
    """Guarda una imagen en carpeta /images"""
    ext = url.split(".")[-1]
    
    try:
        icono = requests.get(url)
        with open(f'images/{game_name}.{ext}', 'wb') as imagen:
            imagen.write(icono.content)
    except requests.exceptions.RequestException as e:
        print('No pudo obtenerse la imagen del url.')

        

def process_top10(top10):
    """Imprime los urls de las imagenes de top 10 de juegos.
    
        Además de ser posible, guarda las imágenes.
    """
    for item in top10:
        print(f'URL de la imagen del juego {item[0][0]}: {item[0][1]}')
        save_image(item[0][1], item[0][0])


with open('bgg_db_1806.csv', encoding = 'utf-8') as games:
    reader = csv.reader(games)

    # no preciso del header, pero lo leo.
    _header = reader.__next__()

    top10 = collections.Counter()
    for row in reader:
        # proceso los juegos de cartas que necesitan menos de 3 jugadores
        if is_cardgame_for_less_than3(row[INDEX_CATEGORY], row[INDEX_MAX_PLAYERS]):
            print(row[INDEX_NAMES])

        # obtengo los votos y los url de las imágenes
        top10[(row[INDEX_NAMES], row[INDEX_IMAGE_URL])] = int(row[INDEX_NUM_VOTES])
            
process_top10(top10.most_common(10))
