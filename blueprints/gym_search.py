from encodings import undefined
from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.gym import GymModel
from extension import db
from datetime import datetime
from forms.gym_search_form import GymSearchForm
from services.gym_search_service import search_gyms_from_google
#import random
import googlemaps

gym_search = Blueprint("gym_search", __name__, url_prefix="/gym_search")

API_KEY = 'AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y '
GOOGLE_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# @gym_search.route('home')
# def index():
#     return render_template('home.html')  # Basic page with a form to search gyms

# @gym_search.route('/search', methods=['POST'])
# def search_gyms():
#     location = request.form['location']  # Get location input from the user
#     radius = 5000  # Search radius in meters

#     # Get the geolocation of the entered location
#     geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y }'
#     geocode_response = request.get(geocode_url).json()

#     if geocode_response['status'] == 'OK':
#         # Extract latitude and longitude of the location
#         lat = geocode_response['results'][0]['geometry']['location']['lat']
#         lng = geocode_response['results'][0]['geometry']['location']['lng']

#         # Now search for gyms using Google Places API
#         places_url = f'{GOOGLE_PLACES_URL}?location={lat},{lng}&radius={radius}&type=gym&key={AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y }'
#         places_response = request.get(places_url).json()

#         # If results are found, save them in the database
#         if places_response['status'] == 'OK':
#             for place in places_response['results']:
#                 name = place.get('name')
#                 #address = place.get('vicinity')
#                 location = place.get('vicinity')
#                 gym_lat = place['geometry']['location']['lat']
#                 gym_lng = place['geometry']['location']['lng']
#                 phone_number = place.get('formatted_phone_number', 'N/A')

#                 # Save to the database
#                 gym = GymModel(
#                     name=name,
#                     #address=address,
#                     location=location,
#                     lat=gym_lat,
#                     lng=gym_lng,
#                     #phone_number=phone_number
#                 )

#                 # Add the gym data to the session and commit
#                 db.session.add(gym)

#                 try:
#                     db.session.commit()
#                 except IntegrityError:
#                     db.session.rollback()  # Avoid duplicate entries

#         # Return the results to the template (or any other way you wish to show them)
#         return render_template('results.html', gyms=places_response['results'])
#     else:
#         return "Location not found", 400

#gym_search = Blueprint('gym_search', __name__)
# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y')
def get_lat_lng_from_location(location):
    geocode_result = gmaps.geocode(location)
    print(geocode_result, "druha")
    if geocode_result:
        lat = geocode_result[0] ['geometry']['location']['lat']
        lng = geocode_result[0] ['geometry']['location']['lng']
        print(lat, "prva")
        return lat,lng
    return None, None #Return None if the location couldn't be geocoded

@gym_search.route('/search_gyms', methods=['GET', 'POST'])
def search_gyms():
    form = GymSearchForm()
    query = GymModel.query
    print(form, "caf")
    if request.method == 'GET':
        print("ahoj")
        location = request.args.get('location') or form.location.data 
        print(location, "dnes")
        #gyms = GymModel.query.all()
        #gym_query = session.query(GymModel)  # Create a query object
        if location:
            filtered_query = query.filter(GymModel.location.ilike(f"%{location.strip()}%"))
            #filtered_gyms = gym_query.filter(GymModel.location.ilike(f"%{location.strip()}%")).all()
            #filtered_gyms = gyms.filter(GymModel.location.ilike(f"%{location.strip()}%"))
            print(filtered_query, "vecer")
            #gyms = search_gyms_from_google(location) # Call the helper function
        # Perform the search for gyms based on the location
        # Call Google Maps API to get the gyms
        # Store gyms in the database
        # Return a result template
            lat, lng = get_lat_lng_from_location(location)
            print(lat,lng, "tretia")
            if filtered_query.count() != 0:
                print(filtered_query.count(), "staci")
                #lat = filtered_query(lat)
                #lng = filtered_query(lng)
                #reverse_geocode_result = gmaps.reverse_geocode(filtered_query(lat, lng))
                #return render_template('search.html', form=form, location=reverse_geocode_result, gyms=filtered_query)
                return render_template('search.html', form=form, location=location, gyms=filtered_query, lat=lat, lng=lng)
            else:
                #return render_template('search.html', form=form, location=reverse_geocode_result, error="No gyms found or invalid location")
                return render_template('search.html', form=form, location=location, lat=lat, lng=lng, error="No gyms found or invalid location")
    return render_template('search.html', form=form)
#address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDCctO8HTJKGB3UB7-8IlxRRWnkIXtkq-Y