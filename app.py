from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Charger le CSV nettoyé
df = pd.read_csv('movies_clean.csv')

print(f"✅ {df.shape[0]} films chargés !")

# Route pour la page d'accueil HTML
@app.route('/')
def home():
    return render_template('index.html') 

# ________________________________________________________________________________________________________________________
#  ROUTE 1 : Tous les films (ou premiers 100)

@app.route('/movies', methods=['GET'])
def get_movies():
    # Prendre seulement 100 films pour tester
    films = df.head(100)
    
    # Prendre seulement quelques colonnes
    films_simple = films[['title', 'vote_average', 'release_date']]
    
    result = films_simple.to_dict('records')
    
    return jsonify({
        'total': len(result),
        'movies': result
    })

# _______________________________________________________________________________________________________________________
# ROUTE 2 : Top 10 par rating

@app.route('/movies/top_rating', methods=['GET'])
def top_rating():
    # Calculer un score pondéré
    min_votes = df['vote_count'].quantile(0.75)  # 25% des films les plus votés
    moyenne_generale = df['vote_average'].mean()
    
    # Formule : (votes × note + min_votes × moyenne) / (votes + min_votes)
    df['score'] = ((df['vote_count'] * df['vote_average']) + (min_votes * moyenne_generale)) / (df['vote_count'] + min_votes)
    
    # Top 10 par score
    top_10 = df.nlargest(10, 'score')
    
    result = top_10[['title', 'vote_average', 'vote_count', 'score', 'release_date']].to_dict('records')
    
    return jsonify({
        'total': len(result),
        'top_movies': result
    })

# _______________________________________________________________________________________________________________________
# ROUTE 3 : Films par acteur

@app.route('/movies/<acteur>', methods=['GET'])
def films_par_acteur(acteur):

    films_acteur = df[df['overview'].str.contains(acteur, case=False, na=False)]
    
    # Convertir en JSON
    result = films_acteur[['title', 'release_date', 'vote_average']].to_dict('records')
    
    return jsonify({
        'acteur': acteur,
        'total': len(result),
        'movies': result
    })

# _______________________________________________________________________________________________________________________
# ROUTE 4 : Films par genre

@app.route('/movies/genre/<genre>', methods=['GET'])
def films_par_genre(genre):
    # Chercher le genre dans la colonne genres
    films_genre = df[df['genres'].str.contains(genre, case=False, na=False)]
    
    # Convertir en JSON
    result = films_genre[['title', 'genres', 'vote_average', 'release_date']].to_dict('records')
    
    return jsonify({
        'genre': genre,
        'total': len(result),
        'movies': result
    })

# _______________________________________________________________________________________________________________________
# ROUTE 5 : Ajouter un film (POST)

@app.route('/movies/add', methods=['POST'])
def add_movie():
    # Récupérer les données envoyées en JSON
    new_movie = request.get_json()
    
    # Vérifier que le titre existe
    if 'title' not in new_movie:
        return jsonify({'error': 'Le titre est obligatoire'}), 400
    
    # Ajouter le film temporairement en mémoire
    # (Il ne sera pas sauvegardé dans le CSV)
    global df
    
    # Créer un nouveau DataFrame avec le film
    new_df = pd.DataFrame([new_movie])
    
    # Ajouter à la fin du DataFrame existant
    df = pd.concat([df, new_df], ignore_index=True)
    
    return jsonify({
        'message': 'Film ajouté avec succès !',
        'movie': new_movie,
        'total_movies': len(df)
    }), 201

# _______________________________________________________________________________________________________________________
# ROUTE 6 : Films avec plusieurs filtres (année, rating, budget)

@app.route('/movies/search', methods=['GET'])
def search_movies():
    # Récupérer tous les paramètres
    year = request.args.get('year')
    min_rating = request.args.get('min_rating')
    max_budget = request.args.get('max_budget')
    limit = request.args.get('limit', 20)  # Par défaut 20 films
    
    # Commencer avec tous les films
    filtered = df.copy()
    
    # Filtrer par année si fournie
    if year:
        filtered['year'] = pd.to_datetime(filtered['release_date'], errors='coerce').dt.year
        filtered = filtered[filtered['year'] == int(year)]
    
    # Filtrer par note minimum si fournie
    if min_rating:
        filtered = filtered[filtered['vote_average'] >= float(min_rating)]
    
    # Filtrer par budget maximum si fourni
    if max_budget:
        filtered = filtered[filtered['budget'] <= float(max_budget)]
    
    # Limiter le nombre de résultats
    filtered = filtered.head(int(limit))
    
    # Convertir en JSON
    result = filtered[['title', 'release_date', 'vote_average', 'budget', 'revenue']].to_dict('records')
    
    return jsonify({
        'filters': {
            'year': year,
            'min_rating': min_rating,
            'max_budget': max_budget,
            'limit': limit
        },
        'total': len(result),
        'movies': result
    })

# _______________________________________________________________________________________________________________________
# ROUTE 7 : Statistiques sur une variable numérique

@app.route('/stats/<variable>', methods=['GET'])
def statistiques(variable):
    # Vérifier que la colonne existe
    if variable not in df.columns:
        return jsonify({'error': f'La colonne {variable} n\'existe pas'}), 400
    
    # Vérifier que c'est une colonne numérique
    if df[variable].dtype not in ['int64', 'float64']:
        return jsonify({'error': f'La colonne {variable} n\'est pas numérique'}), 400
    
    # Calculer les statistiques
    stats = {
        'variable': variable,
        'count': int(df[variable].count()),  # Nombre de valeurs
        'mean': float(df[variable].mean()),  # Moyenne
        'median': float(df[variable].median()),  # Médiane
        'min': float(df[variable].min()),  # Minimum
        'max': float(df[variable].max()),  # Maximum
        'std': float(df[variable].std()),  # Écart-type
        'sum': float(df[variable].sum())  # Somme totale
    }
    
    # la partie médianne et la même que la moyenne car j'ai remplacé plus de 80% de la base avec la moyenne pour pas tout supprimer 


    return jsonify(stats)

# _______________________________________________________________________________________________________________________
# Lancer le serveur

if __name__ == '__main__':
    app.run(debug=True, port=5000)