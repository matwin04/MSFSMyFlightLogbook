import sqlite3
from main import connectDB
import folium
import folium.plugins


def createMap():
    conn = connectDB()
    cursor = conn.cursor()
    #airports
    cursor.execute("SELECT * FROM airports")
    airports = cursor.fetchall()
    #Flights
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()



    m = folium.Map(location=[20,0],zoom_start=2)
    for airport in airports:
        folium.Marker(
            location=[airport['lat'],airport['lon']],
            popup=f"{airport['name']} ({airport['icao']})\n{airport['city']}, {airport['subd']}\n{airport['country']}\n{airport['elv']} FEET MSL",
            tooltip=airport['name']
        ).add_to(m)
    for flight in flights:
        depart_icao = flight['depart_icao']
        arrive_icao = flight['arrive_icao']
        cursor.execute("SELECT lat, lon FROM airports WHERE icao=?", (depart_icao,))
        depart_airport = cursor.fetchone()

        cursor.execute("SELECT lat, lon FROM airports WHERE icao=?", (arrive_icao,))
        arrive_airport = cursor.fetchone()

        if depart_airport and arrive_airport:
            folium.PolyLine(
                locations=[
                    [depart_airport['lat'],depart_airport['lon']],
                    [arrive_airport['lat'],arrive_airport['lon']]
                ],
                color = "red",
                weight = 2.5,
                opacity = 1
            ).add_to(m)
    m.save("pages/map.html")