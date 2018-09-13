import requests, time,datetime
from .types import esri_types


import json, sys

version = int(sys.version[0])
if version ==3:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
else:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

class GetData():

    def __init__(self, url, params={}):
        
        self.url = url
        self.params = params

    def get_request(self):

        r = requests.get(self.url,params = self.params)

        self.data = r.json() 
        # try:
        #   self.data = r.json() 
        # except:
        #   self.data ={}

    def get_request_urllib(self):

        data = urlencode(self.params)
        data = data.encode('ascii') # data should be bytes
        req = Request(self.url, data)
        response = urlopen(req)
        rdata = response.read()
        self.data = json.loads(rdata)
           

    def create_fields(self, precision=5):

        self.fields = []

        for field in self.data['fields']:
            if len(field['name'])>10:
                name = field['name'][:10]
            else:
                name = field['name']
            if version ==2:
                field_details = [name.encode('utf-8'),esri_types[field['type']]]
            else:
                field_details = [name,esri_types[field['type']]]                
            if 'length' in field.keys():
                if esri_types[field['type']] =='C':
                    field_details.append(int(field['length']))
            if esri_types[field['type']] =='F':
                field_details.append(precision)
            self.fields.append(field_details)



class ProcessData():
    def __init__(self,data, fields):
        self.data = data
        self.fields = fields

    def create_geometries(self):
        self.geometries = [row['geometry'] for row in self.data['features']]

    def create_attributes(self):
        self.attributes = []

        for row in self.data['features']:
            newrow = []
            for count,key in enumerate(row['attributes']):
                if self.fields[count][1]=='D':
                    if row['attributes'][key] != None:
                        try:
                            date = datetime.datetime.utcfromtimestamp(abs(float(row['attributes'][key]))/1000.)
                        except:
                            print(float(row['attributes'][key]))
                            date= None
                        #date = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(row['attributes'][key]/1000.))
                        #print(date1, date)
                        newrow.append(date)
                    else:
                        newrow.append(row['attributes'][key])
                else:
                    newrow.append(row['attributes'][key])
            self.attributes.append(newrow)

