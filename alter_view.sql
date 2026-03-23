
ALTER VIEW View_TotalArtistSales AS
SELECT ar.Name as ArtistName,
    SUM(il.UnitPrice * il.Quantity) AS TotalArtistSales
    FROM Artist ar 
    JOIN Album al ON ar.AlbumId = al.ArtistId
    JOIN Track t ON al.AlbumId = t.AlbumId
    JOIN Genre g on t.GenreId = g.GenreId
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    WHERE g.Name not in ('TV Shows', 'Drama', 'Sci Fi & Fantasy', 'Comedy', 'Horror', 'Science Fiction')
    GROUP by ar.Name