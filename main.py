import pandas as pd
import uuid
import json
from faker import Faker
from random import randint

faker = Faker()
Faker.seed(0)

def cargar_archivo_csv(archivo):
    try:
        df = pd.read_csv(archivo)
        print("Archivo leído correctamente.")
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def generar_artistas(album_artist):
    print("Generando artistas...")
    artistas = album_artist['artists'].drop_duplicates().reset_index(drop=True)

    df_artists = pd.DataFrame({
        'artista_id': [faker.unique.ascii_email() for _ in range(len(artistas))],
        'country': [faker.country() for _ in range(len(artistas))],
        'name': artistas,
        'password': [faker.unique.password(length=randint(8, 12)) for _ in range(len(artistas))],
        'picture': [faker.image_url() for _ in range(len(artistas))]
    })

    df_artists = df_artists[['artista_id', 'country', 'name', 'password', 'picture']]

    print(f"Generados {len(df_artists)} artistas.")
    return df_artists

def generar_albumes(df, df_artists):
    print("Generando tabla de álbumes...")

    artist_id_map = dict(zip(df_artists['name'], df_artists['artista_id']))

    unique_albums = df.drop_duplicates(subset=['album_name'])

    album_dates = {album: faker.date_this_century().strftime('%Y-%m-%d')
                   for album in unique_albums['album_name']}

    albumes = pd.DataFrame({
        'artist_id': unique_albums['artists'].map(artist_id_map),
        'genre#date': unique_albums['track_genre'] + '#' + unique_albums['album_name'].map(album_dates),
        'genre': unique_albums['track_genre'],
        'album_uuid': [str(uuid.uuid4()) for _ in range(len(unique_albums))],
        'name': unique_albums['album_name']
    })

    albumes = albumes[['artist_id', 'genre#date', 'genre', 'album_uuid', 'name']]

    print(f"Generados {len(albumes)} álbumes.")
    return albumes, album_dates

def serializar_datos_cancion(row):
    return json.dumps({
        key: row[key] for key in [
            'explicit', 'danceability', 'energy', 'key', 'loudness',
            'mode', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'time_signature', 'track_genre'
        ]
    })

def generar_canciones(df, df_artists, album_dates):
    print("Generando tabla de canciones...")

    artist_id_map = dict(zip(df_artists['name'], df_artists['artista_id']))
    album_date_map = {album: date for album, date in album_dates.items()}

    canciones = pd.DataFrame({
        'artist_id': df['artists'].map(artist_id_map),
        'genre#date': df['track_genre'] + '#' + df['album_name'].map(album_date_map),
        'genre': df['track_genre'],
        'song_uuid': [str(uuid.uuid4()) for _ in range(len(df))],
        'name': df['track_name'],
        'data': df.apply(serializar_datos_cancion, axis=1)
    })

    canciones = canciones[['artist_id', 'genre#date', 'genre', 'song_uuid', 'name', 'data']]

    print(f"Generadas {len(canciones)} canciones.")
    return canciones

def main():
    df = cargar_archivo_csv('dataset_mod.csv')
    if df is None:
        return

    album_artist = df[['album_name', 'artists', 'track_genre']].drop_duplicates()

    df_artists = generar_artistas(album_artist)

    df_albums, album_dates = generar_albumes(df, df_artists)

    df_songs = generar_canciones(df, df_artists, album_dates)

    print("Guardando archivos CSV...")
    df_artists.to_csv('artists.csv', index=False)
    df_songs.to_csv('songs.csv', index=False)
    df_albums.to_csv('albums.csv', index=False)

    print("¡Archivos generados correctamente!")

if __name__ == "__main__":
    main()