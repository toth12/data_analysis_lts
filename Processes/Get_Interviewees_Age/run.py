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
    'number': '100',
    'letter': 'd',
    'label': 'interviewee_year_of_birth'
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
    

    
    parsed['interviewee_year_of_birth']=clean_interviewee_year_of_birth(parsed['interviewee_year_of_birth'])
    
    
    
    # add the parsed record to the list of parsed records
    parsed_records.append(parsed)
  return parsed_records


def clean_gender(gender):
  '''
  @args:
    {arr} gender: a list of urls, one them is the gender attribute of interviews
  @returns:
    {arr} 'M' or 'F' or 
  '''

  #check if multiple gender info is present, in this case this is a couple

  gender_urls={'F':'http://id.loc.gov/authorities/subjects/sh85147274','M':'http://id.loc.gov/authorities/subjects/sh85083510'}
  
  if (gender_urls['F'] in gender) and (gender_urls['M'] in gender):
    gender =''
  elif (gender_urls['F'] in gender):
    gender='female'
  elif (gender_urls['M'] in gender):
    gender = 'male'
  else:
    gender =''
   
  return gender

def clean_year(recording_year):
  '''
  @args:
    {arr} recording_year: a string representing the year when the interview was recorded
  @returns:
    {arr} string representation of the year without the dot at the end
  '''
  
  return int(recording_year[0:4])

def clean_camp_names(camp_names):
  '''
  @args:
    {arr} camp_names: a list of strings
  @returns:
    {arr} a list of strings
  '''

  if len(camp_names)>0:
    result=[]
    for element in camp_names:
      if '(Concentration camp)' in element:
        result.append(element.split('(Concentration camp)')[0].strip())
    return result
  else:
    return camp_names


def clean_provenance(provenance):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  return provenance.strip().rstrip(',')


def clean_ghetto_names(ghetto_names):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  
  if len(ghetto_names)>0:
    result=[]
    for element in ghetto_names:
      if 'ghetto' in element:
        
        result.append(element.split('ghetto.')[0].strip())
    return result
  else:
    return ghetto_names

def clean_interviewee_year_of_birth(interviewee_year_of_birth):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  interviewee_year_of_birth_cleaned=[]
  try:
	  if interviewee_year_of_birth!='':
	  	
	  	interviewee_year_of_birth_cleaned.append(interviewee_year_of_birth.split('-')[0])
	  	return interviewee_year_of_birth_cleaned
	  else:
	  	return None
  except:
   	pdb.set_trace()


def format_marc():
  '''
  Return a list of dictionaries, where each dict represents a
  testimony and possesses the required keys
  '''
  marc_json = get_marc_json()

  marc_json_nested = nest_marc_json(marc_json)
  #ez kell
  marc_json_flat = flatten_marc_json(marc_json_nested)
  
  return marc_json_flat

def create_csv_data(records):
	csv_ready_records=[]
	for record in records:
		print (record)
		if record['interviewee_year_of_birth'] is not None:
			for element in record['interviewee_year_of_birth']:
				if len(element) ==4:
					csv_ready_records.append({"testimony_id":record['testimony_id'],"interviewee_year_of_birth":int(element)})
				else:
					csv_ready_records.append({"testimony_id":record['testimony_id'],"interviewee_year_of_birth":None})
		else:
			csv_ready_records.append({"testimony_id":record['testimony_id'],"interviewee_year_of_birth":None})
	return csv_ready_records


def myround(x, base=5):
    return base * round(x/base)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
##	
# Main
##

def main():
  #Process Fortunoff vocabulary

  print ("Extracting the age of Fortunoff interviewee began")
  

  # process records
  records = format_marc()
  records=create_csv_data(records)
 
  write_to_csv(records,constants.INTERVIEWEES_YEAR_OF_BIRTH+"fortunoff_interviewees_year_of_birth.csv")
  
  



	

	