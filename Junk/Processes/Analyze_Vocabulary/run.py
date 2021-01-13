import constants
from Utilities import folia
from Utilities import text_utils
import glob
import pdb





def main():

	#Process Fortunoff vocabulary

	print ("Processing of the vocabulary of Fortunoff data began")

	#get all Fortunoff file names
	fortunoff_files=glob.glob(constants.INPUT_FOLDER_FORTUNOFF_FOLIA+"*.*")
	#get their count
	get_word_count(fortunoff_files,output_file=constants.WORDCOUNTS+'wordcount_fortunoff.csv')

	print ("Processing of the vocabulary of Fortunoff data accomplished")


def get_word_count(folia_files,output_file):
	counts=[]
	
	#iterate through all files
	for file in folia_files:
		
		#count each file
		count=folia.get_counts(file)

		#get the shelfmark and add to result
		shelfmark=file.split('/')[-1].split('.')[0]
		count['shelfmark']=shelfmark

		#append it to the list
		counts.append(count)
		

		#Write results into CSV
		text_utils.write_to_csv(counts,constants.WORDCOUNTS+'wordcount_fortunoff.csv')


	
	