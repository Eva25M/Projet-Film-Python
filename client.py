import requests
import json
from pprint import pprint

# URL de base de l'API
BASE_URL = 'http://localhost:5000'

print("\n" + "="*60)
print("TESTS DE L'API FILMS")
print("="*60)

# _______________________________________________________________________________________________________________________
# TEST 1 : Tous les films

print("\n=== TEST 1 : Tous les films ===")
response = requests.get(f'{BASE_URL}/movies')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 2 : Top 10 par rating

print("\n=== TEST 2 : Top 10 par rating ===")
response = requests.get(f'{BASE_URL}/movies/top_rating')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 3 : Films par acteur

print("\n=== TEST 3 : Films par acteur (Tom Hanks) ===")
response = requests.get(f'{BASE_URL}/movies/Tom Hanks')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 4 : Films par genre

print("\n=== TEST 4 : Films par genre (Horror) ===")
response = requests.get(f'{BASE_URL}/movies/genre/Horror')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 5 : Ajouter un film (POST)

print("\n=== TEST 5 : Ajouter un film ===")
nouveau_film = {
    'title': 'Mon Film Test',
    'budget': 50000000,
    'revenue': 150000000,
    'vote_average': 8.5,
    'release_date': '2024-01-01'
}
response = requests.post(f'{BASE_URL}/movies/add', json=nouveau_film)
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 6 : Recherche avec filtres

print("\n=== TEST 6 : Recherche (année=2020, min_rating=7.5) ===")
response = requests.get(f'{BASE_URL}/movies/search?year=2020&min_rating=7.5&limit=5')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 7 : Statistiques sur le budget

print("\n=== TEST 7 : Statistiques sur le budget ===")
response = requests.get(f'{BASE_URL}/stats/budget')
print(f"Status: {response.status_code}")
pprint(response.json())

# _______________________________________________________________________________________________________________________
# TEST 8 : Statistiques sur la note

print("\n=== TEST 8 : Statistiques sur vote_average ===")
response = requests.get(f'{BASE_URL}/stats/vote_average')
print(f"Status: {response.status_code}")
pprint(response.json())

print("\n" + "="*60)
print("TESTS TERMINÉS !")
print("="*60)