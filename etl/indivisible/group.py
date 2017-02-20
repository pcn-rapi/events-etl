# encoding=utf8

import os
import requests
import json
import csv

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import urllib

#const 
OSDI_MAX_DATA_PER_PAGE = 25
UNNECESSARY_ELEMENTS = []
SUPER_GROUP = 'Indivisible'
EVENT_TYPE = 'Group'

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
    
    # print(translated_data)
    return translated_data
    
# def get_files():
#     print('Retrieving postal codes and indivisible group data')
#     
#     indivisible_aws_access_key = os.environ.get('INDIVISIBLE_AWS_ACCESS_KEY')
#     indivisible_aws_secret_key = os.environ.get('INDIVISIBLE_AWS_SECRET_KEY')
#     
#     conn = S3Connection(aws_access_key_id=indivisible_aws_access_key, \
#                         aws_secret_access_key=indivisible_aws_secret_key)
#     
#     
#     k_indivisible = bucket.get_key('indivisible-data.csv')
#     k_indivisible.get_contents_to_filename('data/indivisible.csv')
    
def retrieve_and_clean_data():
    """
    We retrieve data through the API and URL given to us by the 
    partner organization. We remove the unnecessary elements as 
    defined in UNNECESSARY_ELEMENTS
    """
    
    # get_files()
    
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    indivisible_url = os.environ.get('INDIVISIBLE_GROUP_URL')
    # start at page 1
    us_postal = {}
    with open('etl/common/us_postal_codes.csv', 'r') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            us_postal[row['zip']] = row
    f.closed
    
    response = urllib.urlopen(indivisible_url)
    with open('data/indivisible.csv', 'w') as f:
        f.write(response.read().decode('utf-8').encode('ascii', 'ignore'))

    # read indivisble
    indivisible_groups = []
    with open('data/indivisible.csv', 'r') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            group = row
            zipcode = group['Zip.code']
            
            while len(zipcode) < 5:
                zipcode = '0' + zipcode
                
            if len(zipcode) > 5:
                zipcode = zipcode[:5]
        
            if not zipcode in us_postal:
                continue
            else:
                group['lat'] = us_postal[zipcode]['lat']
                group['lng'] = us_postal[zipcode]['lon']
            
            indivisible_groups.append(group)
            #endof row
        # f.closed
    
    return indivisible_groups


def translate_data(cleaned_data):
    """
    This is where we translate the data to the necessary information for the map
    """
    translated_data = []
    
    for data in cleaned_data:
        
        address = clean_venue(data)
        group_name = data['Group.Name'] if 'Group.Name' in data else None

        # the first one with a link wins!
        url = None
        for link in [data['website'], data['facebook'], data['twitter']]:
            if link == '' or link is None:
                continue
            url = link
            break
        
        if url is None:
            url = 'mailto:' + data['email']
        elif url is not None and url.startswith('@'):
            url = 'http://twitter.com/' + url
        elif url is not None and not url.startswith('http'):
            url = 'http://' + url
                    
        if 'lat' not in data:
            continue 
        
        twitter = data['twitter']
        if twitter is not None and twitter != '':
            twitter = 'http://twitter.com/'+twitter if twitter.startswith('@') else twitter
        
        event = {
            'title': data['Group.Name'] if 'Group.Name' in data else None, 
            'url': url,
            'supergroup' : SUPER_GROUP,
            'group': group_name,
            'event_type': EVENT_TYPE,
            'start_datetime': '',
            'venue': address,
            'lat': data['lat'],
            'lng': data['lng'],
            'facebook': data['facebook'] if data['facebook'] is not None else '',
            'twitter': twitter if twitter is not None else '',
            'phone': data['phone'] if data['phone'] is not None else '',
            'email': data['email'] if data['email'] is not None else ''
        }
        
        translated_data.append(event)

    return translated_data

def clean_venue(location):
    """
    We translate the venue information to a flat structure
    """
    venue = None
    address = None
    locality = location['City'] if 'City' in location else None
    region = location['State.Abbreviated'] if 'State.Abbreviated' in location else None
    postal_code = None
    
    return ' '.join(['' if i is None else i for i in [venue, address, locality, region, postal_code]])
    
    
def upload_data(to_upload):
    
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
