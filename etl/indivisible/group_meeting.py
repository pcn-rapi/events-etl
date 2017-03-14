# encoding=utf8

import os
import requests
import json
import datetime

#const 
OSDI_MAX_DATA_PER_PAGE = 25
UNNECESSARY_ELEMENTS = ['identifiers','created_date','reminders','action_network:event_campaign_id', \
'_links', 'modified_date', 'status', 'transparence', 'visibility', 'guests_can_invite_others', \
'origin_system', 'action_network:hidden', 'instructions', 'description']
SUPER_GROUP = 'Indivisible'
EVENT_TYPE = 'Group Meeting'

#Headers
_TITLE = 'title'
_URL = 'browser_url'
_STARTDATE = 'start_date'

def save():
    cleaned_data = retrieve_and_clean_data()
    translated_data = translate_data(cleaned_data)
    upload_data(translated_data)    

def grab_data():
    cleaned_data = retrieve_and_clean_data()
    translated_data = translate_data(cleaned_data)
    
    return translated_data
    
def retrieve_and_clean_data():
    """
    We retrieve data through the API and URL given to us by the 
    partner organization. We remove the unnecessary elements as 
    defined in UNNECESSARY_ELEMENTS
    """
    
    print(" -- Retrieving Indivisible Group Meetings")
    # start at page 1
    page = 1
    has_more_content = True
    event_api_key = os.environ.get('INDIVISIBLE_API_KEY')
    event_endpoint = os.environ.get('INDIVISIBLE_TEAM_MEETING_URL')
    
    cleaned_data = []
    
    # traverse the OSDI – only has 1
    while has_more_content:
        req = requests.get(event_endpoint, data={'page': page}, headers={"OSDI-API-Token": event_api_key})
        print ("---- X Going to Page", page, req.status_code)
        
        page = page + 1
        if req.status_code != 200:
            raise ValueError("Error in retrieving ", req.status_code)
        else:
            json_data = json.loads(req.text)
            osdi_events = json_data['_embedded']['osdi:events']
            has_more_content = len(osdi_events) == OSDI_MAX_DATA_PER_PAGE
            
            for event in osdi_events:
                # remove private data
                
                if event["action_network:hidden"]:
                    continue
                    
                for unneeded_key in UNNECESSARY_ELEMENTS:
                    if unneeded_key in event:
                        del event[unneeded_key]
                
                #specifics but not group
                del event['_embedded']['osdi:organizer']
                del event['_embedded']['osdi:creator']['given_name']
                del event['_embedded']['osdi:creator']['family_name']
                del event['_embedded']['osdi:creator']['identifiers']
                del event['_embedded']['osdi:creator']['postal_addresses']
                del event['_embedded']['osdi:creator']['_links']
                
                # print(json.dumps(event))
                # print("\n\n")
            
                cleaned_data.append(event)
            
            # will continue to traverse if has more content
    #endof while has content
        
    return cleaned_data


def translate_data(cleaned_data):
    """
    This is where we translate the data to the necessary information for the map
    """
    print(" -- Translating Indivisible Group Meetings")
    translated_data = []
    
    for data in cleaned_data:
        address = clean_venue(data['location'])
        group_name = data['_embedded']['osdi:creator']['custom_fields']['Group Name'] if 'Group Name' in data['_embedded']['osdi:creator']['custom_fields'] else None
        has_coords = 'location' in data['location']
        
        if not has_coords:
            continue
        
        if data[_STARTDATE][:10] < datetime.date.today().strftime('%Y-%m-%d'):
            continue

        event = {
            'title': data[_TITLE] if _TITLE in data else None, 
            'url': data[_URL] if _URL in data else None,
            'supergroup' : SUPER_GROUP,
            'group': group_name,
            'event_type': EVENT_TYPE,
            'start_datetime': data[_STARTDATE] if _STARTDATE in data else None,
            'venue': address,
            'lat': data['location']['location']['latitude'] if has_coords else None,
            'lng': data['location']['location']['longitude'] if has_coords else None
        }
        
        translated_data.append(event)

    return translated_data

def clean_venue(location):
    """
    We translate the venue information to a flat structure
    """
    print(location['address_lines'])
    venue = location['venue'] + '.' if 'venue' in location else None
    address = ''.join(location['address_lines']) if 'address_lines' in location else None
    locality = location['locality'] if 'locality' in location else None
    region = location['region'] if 'region' in location else None
    postal_code = location['postal_code'] if 'postal_code' in location else None
    
    return ' '.join(['' if i is None else i for i in [venue, address, locality, region, postal_code]])
    
    
def upload_data(to_upload):
    
    print (json.dumps(to_upload))
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
def pretty_print_GET(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
