import constants
from Utilities.text_utils import read,transform_fields_with_non_latin_characters_to_latin, write_to_csv
from Utilities.marc import get_marc_fields
from collections import defaultdict, Counter
from glob import glob
import codecs
import os
import xmltodict
import sys
import json
import constants
import pdb
import math


##
# Globals
##



# inputs and global config
INPUT_DATA='fortunoff-marc.xml'
marc_xml_path = constants.INPUT_FOLDER_FORTUNOFF_METADATA+'fortunoff-marc.xml' # path to metadata xml
max_records = 182# max records to process (int|None)
#complete number of records: 4390


# marc fields to process
fields = [
  {
    'number': '090',
    'letter': 'b',
    'label': 'testimony_id',
  },
  
  {
    'number': '260',
    'letter': 'c',
    'label': 'recording_year'
  }
]

##
# Testimony Metadata Functions
##

def get_marc_json():
  '''
  Parse MarcXML from UC Riverside and return a list
  of JSON records from that XML file
  '''
  records = []
  # marcxml was delivered from UC Riverside
  f = read(marc_xml_path, 'utf8')
  for idx, i in enumerate(f.split('<marc:record>')[1:]):
    if max_records and idx > max_records:
      continue
    xml = '<record>' + i.split('</marc:record>')[0] + '</record>'
    records.append(xmltodict.parse(xml))
 
  return records


def get_field(d):
  '''
  Given a dict `d`, find the MARC code within that
  d and return that code and its value
  @args:
    {obj} d: an object with MARC XML
  @returns:
    {obj} an object with the code and value from d
  '''
  if '@code' in list(d.keys()) and '#text' in list(d.keys()):
    return {
      'code': d['@code'],
      'text': d['#text'],
    }
  return None


def nest_marc_json(arr):
  '''
  Format the JSON parsed from MarcXML
  @args:
    {arr} arr: a list of json records
  @returns:
    {arr} a formatted list of json records
  '''
  records = []
  for idx, i in enumerate(arr):
    record_json = defaultdict(lambda: defaultdict(list))
    record = i['record']

    # 001 = estc_id, 009 = estc internal id
    for j in record['marc:controlfield']:
      tag = j['@tag']
      if tag in ['001', '009']:
        record_json[tag] = j['#text']

    # get record metadata from datafields
    for c, j in enumerate(record['marc:datafield']):
      tag = record['marc:datafield'][c]['@tag']
      if 'marc:subfield' in list(record['marc:datafield'][c].keys()):
        subfield = record['marc:datafield'][c]['marc:subfield']

        # some subfields are arrays of objects, others are objects
        if not isinstance(subfield, list):
          subfield = [subfield]

        for subfield_dict in subfield:
          field = get_field(subfield_dict)
          if field:
            record_json[tag][field['code']].append(field['text'])
          else:
            pass

    parsed = to_dict(record_json)
    records.append(parsed)
  return records


def to_dict(d):
  '''
  Convert a nested defaultdict to a dictionary
  @args:
    {defaultdict} d: a nested defaultdict
  @returns:
    {dict} a plain nested dictionary
  '''
  if isinstance(d, defaultdict):
    d = {k: to_dict(v) for k, v in d.items()}
  return d


def flatten_marc_json(records):
  '''
  Convert a list of documents in nested Marc JSON to
  a list of documents in flat JSON with app-specific
  keys
  '''
  parsed_records = []
  for i, record in enumerate(records):
    
    parsed = get_marc_fields(record, fields)
    

    
    parsed['recording_year']=clean_year(parsed['recording_year'])
    
    
    
    # add the parsed record to the list of parsed records
    parsed_records.append(parsed)
  return parsed_records




def clean_year(recording_year):
  '''
  @args:
    {arr} recording_year: a string representing the year when the interview was recorded
  @returns:
    {arr} string representation of the year without the dot at the end
  '''
  
  if recording_year=='':
    return None
  else:
    try:
      return int(recording_year[0:4])
    except:
      return None


def format_marc():
  '''
  Return a list of dictionaries, where each dict represents a
  testimony and possesses the required keys
  '''
  marc_json = get_marc_json()

  marc_json_nested = nest_marc_json(marc_json)

  marc_json_flat = flatten_marc_json(marc_json_nested)
  
  return marc_json_flat


##	
# Main
##

def main():
  #Process Fortunoff vocabulary

  print ("Extracting the year of recording of Fortunoff interviews began")
  

  # process records
  records = format_marc()
  
 
  write_to_csv(records,constants.FORTUNOFF_RECORDING_YEARS+"fortunoff_recording_years.csv")
  
  



	

	