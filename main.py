import pandas as p
from random import randint
from faker import Faker
from faker.providers import internet

# track_id,artists,album_name,track_name,popularity,duration_ms,explicit,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,time_signature,track_genre
df = p.read_csv('dataset.csv')

faker = Faker()
Faker.seed(10)
faker.add_provider(internet)

nrows = df.shape[0]

album_artist = df[['album_name', 'artists', 'track_genre']].drop_duplicates()

genre_list = df['track_genre'].unique()

def tabla_artistas():
    # artista_mail, name, password, info, picture (random_url)
    # TODO: en la tabla de artistas, hay un atributo country pero en el dataset no hay esa info
    # TODO: no sé que colocar en info

    tabla_artistas = []

    for a in album_artist['artists']:
        tabla_artistas.append({
            'artista_id': faker.unique.ascii_email(),
            'name': a,
            'password': faker.unique.password(randint(8,12)),
            'picture': faker.image_url()
        })

    return tabla_artistas

t_artists = tabla_artistas()
artist_email_map = {a['name']: a['artista_id'] for a in t_artists}

def tabla_canciones():
    # artist_id, genre#release_date, genre, name, data
    # TODO: en el mapeo hay el atributo json data pero no sé que colocar en data
    # data : explicit, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, track_genre
    tabla_canciones = []
    for index, row in df.iterrows():
        artist_name = row['artists']
        artist_id = artist_email_map.get(artist_name, "")

        tabla_canciones.append({
            'artist_id': artist_id,
            'genre': row['track_genre'],
            'name': row['track_name'],
            'data': {
                'explicit': row['explicit'],
                'danceability': row['danceability'],
                'energy': row['energy'],
                'key': row['key'],
                'loudness': row['loudness'],
                'mode': row['mode'],
                'speechiness': row['speechiness'],
                'acousticness': row['acousticness'],
                'instrumentalness': row['instrumentalness'],
                'liveness': row['liveness'],
                'valence': row['valence'],
                'tempo': row['tempo'],
                'time_signature': row['time_signature'],
                'track_genre': row['track_genre']
            }
        })
    return tabla_canciones



def tabla_albumes():
    # artist_id, name, release_date
    tabla_albumes = []
    for index, row in df.iterrows():
        artist_name = row['artists']
        artist_id = artist_email_map.get(artist_name, "")
        artist_name = row['artists']
        album_name = row['album_name']
        genre = row['track_genre'] #TODO FIX LOGIC
        tabla_albumes.append({
            'artist_id': artist_id,
            'name': album_name,
            'date#genre': faker.date_this_century().strftime('%Y-%m-%d') + "#" + genre,
            'genre': genre

        })
    return tabla_albumes


t_albums = tabla_albumes()
t_songs = tabla_canciones()

df_artists = p.DataFrame(t_artists)
df_songs = p.DataFrame(t_songs)
df_albums = p.DataFrame(t_albums)

# Save to CSV files
df_artists.to_csv('artists.csv', index=False)
df_songs.to_csv('songs.csv', index=False)
df_albums.to_csv('albums.csv', index=False)

print("Done!")

