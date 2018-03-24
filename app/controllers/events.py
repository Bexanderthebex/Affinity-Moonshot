from app.config import GOOGLE_MAPS_API_KEY, ACCESS_TOKEN
import googlemaps
import json
from app import db
import requests

def geocode(location_name):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    result = gmaps.geocode(location_name)[0]['geometry']['location']
    return json.dumps({
        'lat': result['lat'],
        'lng': result['lng']
    })

def create_event(name, description, location, min_budget, max_budget, attendees, event_type_id, starting_date_time, ending_date_time):
    c=db.cursor()
    c.execute("""INSERT INTO event(name, description, location, min_budget, max_budget, attendees, event_type_id, starting_date_time, ending_date_time)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (name, description, location, min_budget, max_budget, 
        attendees, event_type_id, starting_date_time, ending_date_time))
    db.commit()
    c = db.cursor()
    c.execute("""SELECT LAST_INSERT_ID()""")
    result = c.fetchall()
    return json.dumps({'event_id': result[0]['LAST_INSERT_ID()']})    

def set_crew(role_id, event_id, fl_user_id):
    c=db.cursor()
    c.execute("""UPDATE role_event SET fl_user_id=%s WHERE event_id=%s and role_id=%s""", (fl_user_id, event_id, role_id))
    db.commit()

def get_fl_user(fl_user_id):
    url = 'https://www.freelancer-sandbox.com/api/users/0.1/users/{}/'.format(fl_user_id)
    headers = {
        'Content-Type': 'application/json',
        'freelancer-oauth-v1': ACCESS_TOKEN
    }
    r = requests.get(url, headers=headers).json()

    return json.dumps(r['result'])

def add_event_role(name, skill_id, event_id, description, min_budget, max_budget):
    c = db.cursor()
    c.execute("""INSERT INTO event_role(name, skill_id, event_id, description, min_budget, max_budget)
        VALUES(%s, %s, %s, %s, %s, %s)""", (name, skill_id, event_id, description, min_budget, max_budget))
    db.commit()
    return