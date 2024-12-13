## Visualizing IoT Devices with Python, Shodan, and Folium

When it comes to understanding how IoT devices are exposed on the internet, visualization is key. Shodan, the "search engine for the Internet of Things," allows us to query open devices, while Python’s Folium library enables us to map this data interactively.

In this post, we’ll walk you through creating a Python script that leverages the Shodan API to fetch IoT device information and plot it on an interactive map. Whether you’re a security analyst or a tech enthusiast, this is a practical way to explore internet-connected devices.

---

### Why Use Shodan and Folium?

- **Shodan**: A powerful tool to discover internet-connected devices, including routers, cameras, and industrial systems. It provides data like IP addresses, ports, and vulnerabilities.
- **Folium**: A Python library that simplifies creating interactive maps with markers, popups, and clustering options.

By combining these tools, we can gain insights into device exposure and potential vulnerabilities in a visual, user-friendly format.

---

### Step-by-Step Guide

#### 1. Prerequisites

To follow along, you’ll need:

- A valid Shodan API key (sign up at [Shodan.io](https://shodan.io)).
- Python installed on your system.
- Required libraries: Install them with the following commands:

```bash
pip install shodan folium
```

#### 2. Writing the Python Script

Here’s the Python code to fetch IoT device data from Shodan and create an interactive map:

```python
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
```

---

### How It Works

#### **Step 1: Input Query**

- The script prompts you to input a country code (e.g., `GB` for the UK) and a port number (e.g., `23` for Telnet).

#### **Step 2: Fetch Device Data**

- Using the Shodan API, the script retrieves data matching your query. This includes IP addresses, ports, vulnerabilities, and location data.

#### **Step 3: Plot Devices on a Map**

- Each device is represented as a marker on an interactive map. Markers are color-coded:
  - **Red**: Devices with known vulnerabilities.
  - **Blue**: Secure devices.

#### **Step 4: Save the Map**

- The map is saved as an HTML file that you can open in your browser for an interactive experience.

---

### Example Output

After running the script, you’ll see output like this:

```plaintext
Fetching data from Shodan API for country: GB, port: 23...
Found 150 devices.
Interactive map saved as iot_device_map.html.
```

Open the `iot_device_map.html` file to explore the map. Clicking on a marker displays details about the device, including IP address and known vulnerabilities.

---

### Use Cases

1. **Security Research**:
   - Identify vulnerable IoT devices in specific regions.
2. **Educational Purposes**:
   - Demonstrate the risks of exposed devices.
3. **Proactive Defense**:
   - Use the data to secure devices in your network.

---

### Ethical Considerations

This tool is powerful and must be used responsibly. Accessing or interacting with devices without authorization may violate privacy laws. Use it strictly for authorized research or educational purposes.

---

### Conclusion

Mapping IoT devices with Python, Shodan, and Folium is a practical way to visualize internet-connected devices and their vulnerabilities. This script offers a hands-on approach to understanding device exposure while promoting security awareness.

The full code is available on the [GitHub repository](https://github.com/arknet-cyber/shodan_iot_maps). If you found this helpful, check out more articles on [Wirepost.uk](https://wirepost.uk) and [CyberInt.uk](https://cyberint.uk). Happy mapping!