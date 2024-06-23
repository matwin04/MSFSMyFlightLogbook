from main import connectDB
import folium
import folium.plugins


def createMap():
    m = folium.Map(location=[20,0],zoom_start=2)
    icon_plane = folium.plugins.BeautifyIcon(
        icon="plane", border_color="#b3334f", text_color="#b3334f", icon_shape="triangle"
    )
    with connectDB() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM airports")
        rows = cursor.fetchall()
        for row in rows:
            folium.Marker(
                location=[row['lat'],row['lon']],
                popup=f"{row['name']} ({row['icao']})\n{row['city']}, {row['subd']}\n{row['country']}\n{row['elv']} FEET MSL",
                tooltip=row['name']
            ).add_to(m)
    m.save("pages/map.html")