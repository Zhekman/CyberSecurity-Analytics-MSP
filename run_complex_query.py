import sqlite3
import os

def run_query():
    db_path = 'Chinook_Sqlite.sqlite'
    
    if not os.path.exists(db_path):
        print(f"Error: File {db_path} not found!")
        return

    # Підключення до бази даних
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Складний SQL запит
    query = """
    WITH TrackRevenue AS (
        -- 1. Розраховуємо загальний дохід для кожного треку
        SELECT 
            t.TrackId,
            t.Name AS TrackName,
            t.GenreId,
            t.AlbumId,
            SUM(il.UnitPrice * il.Quantity) AS TotalTrackRevenue
        FROM Track t
        JOIN InvoiceLine il ON t.TrackId = il.TrackId
        GROUP BY t.TrackId
    ),
    ArtistGenreStats AS (
        -- 2. Збираємо статистику по артистах у розрізі жанрів
        SELECT 
            g.Name AS Genre,
            art.Name AS Artist,
            tr.TrackName AS TopTrack,
            tr.TotalTrackRevenue,
            SUM(tr.TotalTrackRevenue) OVER(PARTITION BY g.GenreId, art.ArtistId) AS TotalArtistGenreRevenue,
            RANK() OVER(
                PARTITION BY g.GenreId 
                ORDER BY SUM(tr.TotalTrackRevenue) OVER(PARTITION BY g.GenreId, art.ArtistId) DESC
            ) AS ArtistRank,
            ROW_NUMBER() OVER(
                PARTITION BY g.GenreId, art.ArtistId 
                ORDER BY tr.TotalTrackRevenue DESC
            ) AS TrackRankInArtist
        FROM TrackRevenue tr
        JOIN Genre g ON tr.GenreId = g.GenreId
        JOIN Album alb ON tr.AlbumId = alb.AlbumId
        JOIN Artist art ON alb.ArtistId = art.ArtistId
    )
    -- 3. Вибираємо тільки найкращого артиста для кожного жанру та їхній топ-трек
    SELECT 
        Genre,
        Artist,
        TopTrack,
        ROUND(TotalArtistGenreRevenue, 2) AS TotalRevenueInGenre
    FROM ArtistGenreStats
    WHERE ArtistRank = 1 AND TrackRankInArtist = 1
    ORDER BY TotalRevenueInGenre DESC;
    """

    print(f"{'GENRE':<15} | {'ARTIST':<25} | {'TOP TRACK':<35} | {'REVENUE'}")
    print("-" * 90)

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            genre, artist, track, revenue = row
            # Обрізаємо довгі назви для красивого виводу
            print(f"{str(genre)[:15]:<15} | {str(artist)[:25]:<25} | {str(track)[:35]:<35} | ${revenue}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print("\nПорада: Якщо ви бачите помилку 'near \"(\": syntax error', це означає, що ваша версія Python використовує занадто стару версію SQLite (менше 3.25.0).")
    finally:
        conn.close()

if __name__ == "__main__":
    run_query()
