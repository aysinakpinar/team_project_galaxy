import requests
from models.gym import GymModel, db

def search_gyms_from_google(location):
    # Get the geocoded location (latitude and longitude)
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key=AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y '
    response = requests.get(geocode_url)
    geocode_data = response.json()
    gyms = [] # To store gym data from Google API

    # # Manually add gym data 
    # galaxy_gym = {
    #     'name': 'Galaxy Gym',
    #     'lat': '51.45754',
    #     'lng': '-0.96206'
    # }
    # gyms.append(galaxy_gym)
    if geocode_data['status'] == 'OK':
        lat = geocode_data['results'][0]['geometry']['location']['lat']
        lng = geocode_data['results'][0]['geometry']['location']['lng']

        # Search for gyms using the Places API
        places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=gym&key=AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y '
        places_response = requests.get(places_url)
        gyms = places_response.json().get('results', [])
        #google_gyms = places_response.json().get('results', [])

    #     # Store gyms in the database
        
        for gym in gyms:
            gym_model = GymModel(
                name=gym['name'],
                #address=gym.get('vicinity', ''),
                location=gym.get('vicinity', ''),
                lat=gym['geometry']['location']['lat'],
                lng=gym['geometry']['location']['lng'],
                phone_number=gym.get('formatted_phone_number', 'N/A')
            )
            db.session.add(gym_model)
        db.session.commit()

        # gyms.append({
        #     'name': 'Galaxy Gym',
        #     'lat': 51.45754,
        #     'lng': -0.96206,
        #     'location': '123 Galaxy Ave, London',
        #     'phone_number': '123-456-7890'
        # })
        return gyms  # Optionally return the gyms for displaying in the template
    else:
        return None  # In case of error, return None
    
        # for gym in google_gyms:
        #     gym_data = {
        #         'name': gym['name'],
        #         'lat': gym['geometry']['location']['lat'],
        #         'lng': gym['geometry']['location']['lng'],
        #     }
        #     gyms.append(gym_data)
        # return gyms
