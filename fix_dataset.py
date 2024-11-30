import pandas as p


# track_id,artists,album_name,track_name,popularity,duration_ms,explicit,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,time_signature,track_genre
df = p.read_csv('dataset.csv')
df['artists'] = df['artists'].apply(lambda x: x.split(';')[0].strip() if isinstance(x, str) else "Unknown Artist")

df.to_csv('dataset.csv', index=False)