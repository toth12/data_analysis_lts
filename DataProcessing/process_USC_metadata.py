import os
path = os.path.abspath(os.getcwd())
import sys; sys.path.insert(0, path)
from Utilities import mongo_helper
import constants
import pdb
import pandas as pd
from Utilities import text
import xmltodict
import xml.etree.ElementTree as ET
from tqdm import tqdm



collection = "USC"
db = "lts"
xml_path = constants.INPUT_FOLDER_USC_METADATA
testimonies = mongo_helper.query(db,"testimonies",{'collection':collection},{'structured_transcript':0,'html_transcript':0,'_id':0})
df_testimonies = pd.DataFrame(testimonies)
df_testimonies =df_testimonies[df_testimonies['status']=="transcript_processed"]
result = []
for i,intcode in tqdm(enumerate(df_testimonies.IntCode.to_list())):
    try:
        filename = 'intcode-'+str(intcode)+'.xml'
        path = xml_path+filename
        xml_data = text.read(path, 'utf8')
        root = ET.fromstring(xml_data)
        
        # Get the interview data
        try:
            interview_country = root.findall(".//reference[@modifier='Country of Interview']")[0].text
        except:
            interview_country = ''
        # Get the interview length
        try:
            interview_length = root.findall(".//reference[@modifier='Length of Interview']")[0].text
        except:
            interview_length = ''
        try:
            country_of_birth = root.findall(".//response[@questionlabel='Country of Birth']")[0].text
        except:
            country_of_birth = ''
        # Get the year of birth
        try:
            year_of_birth = root.findall(".//created[@modifier='Interviewee Date of Birth']")[0].text.split('/')[0]
        except:
            year_of_birth = ''
        result.append({'IntCode':intcode,'interviewee_year_of_birth':year_of_birth,'birth_place_countries':country_of_birth,'interview_length':interview_length,'interview_location':interview_country})
    except:
        print (intcode)
    

df_result = pd.DataFrame(result)
df_result.to_csv(constants.OUTPUT_FOLDER+'usc_metadata.csv')


    