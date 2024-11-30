import pandas as p
from random import randint
from faker import Faker
from faker.providers import internet

# track_id,artists,album_name,track_name,popularity,duration_ms,explicit,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,time_signature,track_genre
df = p.read_csv('dataset_mod.csv')

faker = Faker()
Faker.seed(10)
faker.add_provider(internet)

nrows = df.shape[0]

album_artist = df[['album_name', 'artists', 'track_genre']].drop_duplicates()
print(album_artist.to_csv(index=False))
genre_list = df['track_genre'].unique()

def tabla_artistas():
    unique_emails = [faker.unique.ascii_email() for _ in range(len(album_artist))]
    unique_passwords = [faker.unique.password(randint(8, 12)) for _ in range(len(album_artist))]
    unique_pictures = [faker.image_url() for _ in range(len(album_artist))]

    tabla_artistas = [
        {
            'artista_id': unique_emails[i],
            'name': a,
            'password': unique_passwords[i],
            'picture': unique_pictures[i]
        }
        for i, a in enumerate(album_artist['artists'])
    ]

    return tabla_artistas

t_artists = tabla_artistas()
artist_email_map = {a['name']: a['artista_id'] for a in t_artists}

def tabla_canciones():
    tabla_canciones = []
    artist_ids = df['artists'].map(artist_email_map.get)

    for index, row in df.iterrows():
        tabla_canciones.append({
            'artist_id': artist_ids[index],
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
    albumes = []
    for index, row in df.iterrows():
        artist_name = row['artists']
        artist_id = artist_email_map.get(artist_name, "")

        albumes.append({
            'artist_id': artist_id,
            'name': row['album_name'],
            'release_date': faker.date_this_decade()
        })
    return


# t_albums = tabla_albumes()
# t_songs = tabla_canciones()
#
# df_artists = p.DataFrame(t_artists)
# df_songs = p.DataFrame(t_songs)
# df_albums = p.DataFrame(t_albums)
#
# # Save to CSV files
# df_artists.to_csv('artists.csv', index=False)
# df_songs.to_csv('songs.csv', index=False)
# df_albums.to_csv('albums.csv', index=False)
#
# print("Done!")

