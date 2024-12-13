import shodan
import folium

# Shodan API Key
SHODAN_API_KEY = 'your_shodan_api_key_here'

# Initialize Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

# Get user input for country and port
country = input("Enter the country code (e.g., GB, US): ").strip()
port = input("Enter the port number to search for (e.g., 23, 80): ").strip()

# Search query
query = f'country:{country} port:{port}'
print(f"Fetching data from Shodan API for country: {country}, port: {port}...")
try:
    results = api.search(query)
    print(f"Found {len(results['matches'])} devices.")
except Exception as e:
    print(f"Error: {e}")
    results = {'matches': []}

# Create an interactive map centered on the country (default: global view)
device_map = folium.Map(location=[54.5, -4.5], zoom_start=6)

# Add devices to the map
if results['matches']:
    for result in results['matches']:
        # Ensure latitude and longitude are present
        location = result.get('location', {})
        lat = location.get('latitude')
        lon = location.get('longitude')

        if lat and lon:
            ip = result.get('ip_str', 'N/A')
            vulnerabilities = result.get('vulns', {})
            vuln_details = "\n".join(vulnerabilities.keys()) if vulnerabilities else "No known vulnerabilities."

            popup_content = f"""
            <b>IP Address:</b> {ip}<br>
            <b>Vulnerabilities:</b> {vuln_details}
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="red" if vulnerabilities else "blue"),
            ).add_to(device_map)
else:
    print("No devices found or API query returned no results.")

# Save the map to an HTML file
map_file = 'iot_device_map.html'
device_map.save(map_file)
print(f"Interactive map saved as {map_file}. Open it in your browser to view.")