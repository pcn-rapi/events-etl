# encoding=utf8

from etl.peoplepower import launch as peoplepower_launch

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import boto
import os
import json
import gzip    

def run():
    data = peoplepower_launch.grab_data()
    raw = json.dumps(data)
    content = 'window.PEOPLEPOWER_EVENTS=' + json.dumps(data)
    
    # Locally Store Data
    with gzip.open('data/peoplepower.js.gz', 'wb') as f:
        f.write(str(content))
        
    with open('data/peoplepower.json', 'w') as f:
        f.write(raw)
    
    # START 
    aws_host = os.environ.get('AWS_HOST')
    conn = S3Connection(host=aws_host)
    
    bucket = conn.get_bucket('pplsmap-data')
    key = bucket.get_key('output/peoplepower.js.gz')
    key_raw = bucket.get_key('raw/peoplepower.json')
    
    # Retrieve Keys
    if key is None: 
        print("Creating New Bucket")
        key = bucket.new_key('output/peoplepower.js.gz')
        
    if key_raw is None:
        print("Creating New Raw File")
        key_raw = bucket.new_key('raw/peoplepower.json')
    
    # Upload data to S3
    print("Uploading RAW to S3")
    key_raw.set_contents_from_filename('data/peoplepower.json')
    key_raw.set_acl('public-read')
    
    print("Uploading GZIP to S3")
    key.set_metadata('Content-Type', 'text/plain')
    key.set_metadata('Content-Encoding', 'gzip')
    key.set_contents_from_filename('data/peoplepower.js.gz')
    key.set_acl('public-read')
    
    # Cloudfront Invalidation requests
    print("Invalidating Output")
    cloudfront = boto.connect_cloudfront()
    paths = ['/output/*']
    inval_req = cloudfront.create_invalidation_request(u'EXFHJXIFH495H', paths)

    os.remove("data/peoplepower.js.gz")
    os.remove("data/peoplepower.json")


# Retrieve all data
