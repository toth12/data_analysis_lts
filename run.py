from Processes.Analyze_Vocabulary.run import main as analyze_vocabulary
from Processes.Extract_Keywords.run import main as extract_keywords
from Processes.Get_Interviewees_Age.run import main as get_interwiees_age
from Processes.Get_Recording_Year.run import main as get_recording_year



def process_data():
	
	get_interwiees_age()
	#extract_keywords()
	#get_recording_year()


if __name__ == '__main__':
	process_data()