import requests

def find_nearest_supermarket(api_key, location):
  """
  Uses Google Maps API to find the nearest supermarket.

  Args:
      api_key: Your Google Maps API key.
      location: Your current location as latitude,longitude string.

  Returns:
      A dictionary containing details of the nearest supermarket, 
      or None if no results found.
  """
  url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
  params = {
      "location": location,
      "radius": 5000,  # Search radius in meters (adjust as needed)
      "type": "grocery store",
      "key": api_key
  }
  response = requests.get(url, params=params)
  data = response.json()

  if data["status"] == "OK":
    return data["results"][0]  # Return details of first result
  else:
    print("Error:", data["status"])
    return None

def open_in_google_maps(place_id):
  """
  Opens the place details in Google Maps app or web browser.
  """
  url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
  print(f"Opening supermarket in Google Maps: {url}")
  # This might not work on all systems, explore platform-specific options for launching

# Example Usage (replace with your API key and location)
your_api_key = ""
your_location = "19.266309458257684, 72.87160523923795"

# Find nearest supermarket
nearest_supermarket = find_nearest_supermarket(your_api_key, your_location)

if nearest_supermarket:
  open_in_google_maps(nearest_supermarket["place_id"])
else:
  print("No supermarkets found nearby.")
