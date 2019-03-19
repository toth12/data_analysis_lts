import constants
from Utilities import folia
from Utilities import text_utils
import glob
import pdb
from pke import compute_document_frequency
from string import punctuation
import pke
import string





def main():

	#process the document frequency of the reference corpus
	

	"""Compute Document Frequency (DF) counts from a collection of documents.

	N-grams up to 3-grams are extracted and converted to their n-stems forms.
	Those containing a token that occurs in a stoplist are filtered out.
	Output file is in compressed (gzip) tab-separated-values format (tsv.gz).
	"""

	# stoplist for filtering n-grams
	stoplist=list(punctuation)

	# compute df counts and store as n-stem -> weight values
	compute_document_frequency(input_dir='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/data/inputs/fortunoff/transcripts/',
	                           output_file='/Users/gmt28/Documents/Workspace/data_analysis_lts/Processes/Extract_Keywords/output.tsv.gz',
	                           extension='txt',           # input file extension
	                           language='en',                # language of files
	                           normalization=None,    # use porter stemmer
	                           stoplist=stoplist,
	                           n=1)

	pdb.set_trace()
	"""Keyphrase extraction using TfIdf and newly computed DF counts."""

	# initialize TfIdf model
	extractor = pke.unsupervised.TfIdf()


	# load the DF counts from file
	df_counts = pke.load_document_frequency_file(input_file='/Users/gmt28/Documents/Workspace/data_analysis_lts/Processes/Extract_Keywords/output.tsv.gz')

	

	# load the content of the document
	extractor.load_document(input='/Users/gmt28/Documents/Workspace/data_analysis_lts/Processes/Extract_Keywords/text.txt',
                        normalization=None,language='en')

	

	# keyphrase candidate selection
	extractor.candidate_selection(n=1, stoplist=list(string.punctuation))

	# candidate weighting with the provided DF counts
	extractor.candidate_weighting(df=df_counts)

	# N-best selection, keyphrases contains the 10 highest scored candidates as
	# (keyphrase, score) tuples
	keyphrases = extractor.get_n_best(n=15)
	print (keyphrases)
	pdb.set_trace()

	