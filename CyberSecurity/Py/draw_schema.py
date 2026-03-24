import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

def draw_schema():
    conn = sqlite3.connect('Chinook_Sqlite.sqlite')
    cursor = conn.cursor()
    
    # Визначаємо зв'язки між таблицями (на основі зовнішніх ключів)
    edges = [
        ("Artist", "Album"),
        ("Album", "Track"),
        ("Genre", "Track"),
        ("MediaType", "Track"),
        ("Track", "InvoiceLine"),
        ("Invoice", "InvoiceLine"),
        ("Customer", "Invoice"),
        ("Employee", "Customer"),
        ("Employee", "Employee"), # ReportsTo
        ("Playlist", "PlaylistTrack"),
        ("Track", "PlaylistTrack")
    ]
    
    G = nx.DiGraph()
    G.add_edges_from(edges)
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold', 
            arrows=True, arrowsize=20)
    
    plt.title("Chinook Database Schema Relations", size=15)
    plt.savefig("chinook_schema.png")
    print("Зображення збережено як chinook_schema.png")
    
    conn.close()

if __name__ == '__main__':
    draw_schema()
