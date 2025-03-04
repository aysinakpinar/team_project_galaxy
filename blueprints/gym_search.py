from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.gym import GymModel
from extension import db
from datetime import datetime
from forms.gym_search_form import GymSearchForm
from services.gym_search_service import search_gyms_from_google
import random

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

@gym_search.route('/search', methods=['GET', 'POST'])
def search_gyms():
    form = GymSearchForm()
    if request.method == 'GET':
        location = request.form.get('location')
        gyms = search_gyms_from_google(location) # Call the helper function
        # Perform the search for gyms based on the location
        # Call Google Maps API to get the gyms
        # Store gyms in the database
        # Return a result template
        if gyms:
            return render_template('result.html', gyms=gyms)
        else:
            return render_template('search.html', error="No gyms found or invalid location")
    return render_template('search.html', form=form)


