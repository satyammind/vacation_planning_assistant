from folium.plugins import AntPath
from fpdf import FPDF
import spacy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

# Load NLP model and geolocator
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="vacation_planner", timeout=10)

class Helper:
    # PDF Generator
    def generate_pdf(itinerary):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, itinerary)
        return pdf

    @staticmethod
    def extract_locations(text):
        doc = nlp(text)
        return list(set(ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]))

    @staticmethod
    def calculate_travel_time(distance_km):
        if distance_km <= 300:
            hours = distance_km // 50
            minutes = round((distance_km % 50) / 50 * 60)
            return f"🚗 {round(distance_km)} km → {hours} hr {minutes} min"
        else:
            hours = distance_km // 500
            minutes = round((distance_km % 500) / 500 * 60)
            return f"✈️ {round(distance_km)} km → {hours} hr {minutes} min"

    @staticmethod
    def geocode(result, destination, starting_point):
        try:
            if not destination or not starting_point:
                return None
            
            # Initialize map
            m = folium.Map(location=[20, 0], zoom_start=3)
            all_locations = []
            path_with_distances = []

            locations = Helper.extract_locations(result.raw)

            st_loc = geolocator.geocode(starting_point, addressdetails=True)
            starting_cords = (st_loc.latitude, st_loc.longitude) if st_loc else None

            destination_loc = geolocator.geocode(destination, addressdetails=True)
            dest_cords = (destination_loc.latitude, destination_loc.longitude) if destination_loc else None

            dist = geodesic(starting_cords, dest_cords).km
            popup_text_start = Helper.calculate_travel_time(dist)
            folium.Marker(
                location=starting_cords,
                popup=popup_text_start,
                tooltip=str(st_loc),  
                icon=folium.Icon("green")
            ).add_to(m)

            input_dest_state = destination_loc.raw['address']['state'] if destination_loc and 'state' in destination_loc.raw['address'] else None

            for location in locations:
                loc = geolocator.geocode(location, language="en", country_codes="IN", addressdetails=True)

                if loc is None:
                    continue

                dest_state = loc.raw['address']['state'] if 'state' in loc.raw['address'] else None

                if dest_state is not None and dest_state == input_dest_state:
                    coords = (loc.latitude, loc.longitude)
                    all_locations.append(coords)
                    folium.Marker(
                        location=coords,
                        popup=location,
                        tooltip=str(loc),
                        icon=folium.Icon("blue")
                    ).add_to(m)

            # Append Starting Point First
            all_locations.insert(0, starting_cords)

            # Calculate Distance & Add Orange Markers
            for i in range(len(all_locations) - 1):
                dist = geodesic(all_locations[i], all_locations[i + 1]).km
                path_with_distances.append(all_locations[i])
                popup_text = Helper.calculate_travel_time(dist)
                
                # Only add orange markers for travel locations, not the starting point
                if i > 0:  
                    folium.Marker(
                        location=all_locations[i],
                        popup=popup_text,
                        tooltip=str(geolocator.reverse(all_locations[i])),
                        icon=folium.Icon("orange")
                    ).add_to(m)

            path_with_distances.append(all_locations[-1])

            # Draw Animated Path
            AntPath(path_with_distances, color="blue", weight=3, delay=500).add_to(m)

            if all_locations:
                m.fit_bounds(all_locations)

            return m

        except Exception as e:
            print("Geocoding Error:", e)
            return None

