import json, requests
from app.config import ACCESS_TOKEN
from app import db

def post_project(title, description, min_budget, max_budget, lat, lng, job_ids, event_id, role_id):
    url = 'https://www.freelancer-sandbox.com/api/projects/0.1/projects/'
    data = {
        'title': title,
        'description': description,
        'currency': {
            'id': 7
        },
        'budget': {
            'minimum': float(min_budget),
            'maximum': float(max_budget),
            'id': 7
        },
        'jobs': [{'id': x} for x in job_ids],
        'location': {
            'latitude': lat,
            'longitude': lng
        }
    }
    headers = {
        'content-type': 'application/json',
        'freelancer-oauth-v1': ACCESS_TOKEN
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    
    j = r.json()
    c = db.cursor()
    c.execute("""UPDATE event_role SET fl_project_id=%s WHERE event_id=%s and id=%s""", (j[result][id],event_id,role_id))
    db.commit()

    return r.text

def award_bid(bid_id, action):
    url = 'https://www.freelancer-sandbox.com/api/projects/0.1/bids/%d/' % bid_id
    data = {
        'action': action
    }

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'freelancer-oauth-v1': ACCESS_TOKEN
    }
    r = requests.put(url, data=data, headers=headers)
    return r.text

def get_bids_handler(project_id):
    url = 'https://www.freelancer-sandbox.com/api/projects/0.1/projects/{}/bids/'.format(project_id)
    print(project_id)
    return requests.get(url).text

def get_skills_handler():    
    c=db.cursor()
    c.execute("""SELECT name, id, name FROM skill""")
    return json.dumps({"data": list(c.fetchall())})
