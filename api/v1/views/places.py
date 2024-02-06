#!/usr/bin/python3
'''
Create a view for Place objects - handles all default RESTful API actions
'''
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())