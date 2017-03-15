from etl.indivisible import group_meeting as indivisible_groupmtg
from etl.indivisible import action as indivisible_action
from etl.indivisible import group as indivisible_group

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import boto
import os
import json
import gzip    

def run():
    indiv_groups = indivisible_group.grab_data()
    indiv_groupmtg = indivisible_groupmtg.grab_data()
    indiv_action = indivisible_action.grab_data()
    
    data = indiv_groupmtg + indiv_action + indiv_groups
    content = 'window.INDIVISIBLE_EVENTS=' +json.dumps(data)
    
    # Locally Store Data
    with gzip.open('data/indivisible-data.js.gz', 'wb') as f:
        f.write(str(content).encode('utf-8'))
        
    with open('data/indivisible.json', 'w') as f:
        f.write(content)
    
    # START 
    aws_host = os.environ.get('AWS_HOST')
    conn = S3Connection(host=aws_host)
    
    bucket = conn.get_bucket('pplsmap-data')
    key = bucket.get_key('output/indivisible.js.gz')
    key_raw = bucket.get_key('raw/indivisible.json')
    
    # Retrieve Keys
    if key is None: 
        print("Creating New Bucket")
        key = bucket.new_key('output/indivisible.js.gz')
        
    if key_raw is None:
        print("Creating New Raw File")
        key_raw = bucket.new_key('raw/indivisible.json')
    
    # Upload data to S3
    print("Uploading RAW to S3")
    key_raw.set_contents_from_filename('data/indivisible.json')
    key_raw.set_acl('public-read')
    
    print("Uploading GZIP to S3")
    key.set_metadata('Content-Type', 'text/plain')
    key.set_metadata('Content-Encoding', 'gzip')
    key.set_contents_from_filename('data/indivisible-data.js.gz')
    key.set_acl('public-read')
    
    # Cloudfront Invalidation requests
    print("Invalidating Indivisible Output")
    cloudfront = boto.connect_cloudfront()
    paths = ['/output/*']
    inval_req = cloudfront.create_invalidation_request(u'EXFHJXIFH495H', paths)

    #Delete all files
    os.remove("data/indivisible-data.js.gz")
    os.remove("data/indivisible.json")
    os.remove("data/indivisible.csv")

# Retrieve all data
def queue():
    run()
