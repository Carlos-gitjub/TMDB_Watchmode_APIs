import urllib.request
import urllib.parse
import json

# Configuración
TMDB_API_KEY = ""
WATCHMODE_API_KEY = ""
REGION = "ES"

# Lista de películas
peliculas = [
    "Braveheart",   
    "Inception",
    "The Godfather"
]

def buscar_en_tmdb(nombre):
    query = urllib.parse.quote(nombre)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        resultados = data.get("results", [])
        if not resultados:
            return None
        mejor = resultados[0]
        return {
            "tmdb_id": mejor["id"],
            "title": mejor["title"],
            "year": mejor.get("release_date", "").split("-")[0] or "¿?",
        }

def obtener_imdb_id(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data.get("imdb_id")

def buscar_en_watchmode(imdb_id):
    url = f"https://api.watchmode.com/v1/search/?apiKey={WATCHMODE_API_KEY}&search_field=imdb_id&search_value={imdb_id}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data.get("title_results", [])

def obtener_plataformas(title_id):
    url = f"https://api.watchmode.com/v1/title/{title_id}/sources/?apiKey={WATCHMODE_API_KEY}&regions={REGION}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

# Procesar películas
print("🔎 Procesando lista de películas...\n")

for nombre in peliculas:
    print(f"🎬 Buscando: {nombre}")
    tmdb = buscar_en_tmdb(nombre)
    if not tmdb:
        print(f"❌ No encontrada en TMDb\n")
        continue

    imdb_id = obtener_imdb_id(tmdb["tmdb_id"])
    if not imdb_id:
        print(f"❌ No se encontró IMDb ID\n")
        continue

    resultados = buscar_en_watchmode(imdb_id)
    if not resultados:
        print(f"❌ No encontrada en Watchmode\n")
        continue

    pelicula = resultados[0]
    plataformas = obtener_plataformas(pelicula["id"])
    if not plataformas:
        print("❌ No hay plataformas disponibles\n")
        continue

    print(f"✅ Título detectado: {pelicula['name']} ({pelicula['year']})")
    print("📺 Plataformas disponibles:")

    mostradas = set()
    for s in plataformas:
        clave = (s['name'], s['type'], s['format'])
        if clave in mostradas:
            continue
        mostradas.add(clave)

        tipo = {
            "sub": "Suscripción",
            "rent": "Alquiler",
            "buy": "Compra"
        }.get(s["type"], s["type"])

        precio = "(precio suscripción)" if s["type"] == "sub" else f"{s['price']} €"
        print(f"  - {s['name']}: {tipo} | {s['format']} | {precio}")
    print()
