import os
path = os.path.abspath(os.getcwd())
import sys; sys.path.insert(0, path)
import pandas as pd
import os
from tqdm.notebook import tqdm
import constants
import spacy
import pycountry
from Utilities import mongo_helper
from Utilities import blacklab
import pdb

def get_token_counts(testimony_id):
    #result = blacklab.iterable_results('[]',lemma=False,path_to_phrase_model=None,window=0,document_ids=[testimony_id])
    #tokens = [element for element in result]
    #return (len(tokens))
    return 1

db = "lts"
testimonies = mongo_helper.query(db,"testimonies",{},{'structured_transcript':0,'html_transcript':0,'_id':0})
df_testimonies = pd.DataFrame(testimonies)
df_testimonies =df_testimonies[df_testimonies['status']=="transcript_processed"]
df_testimonies['word_count'] = df_testimonies.testimony_id.apply(get_token_counts)

df_testimonies.to_csv(constants.OUTPUT_FOLDER+'word_counts.csv')
