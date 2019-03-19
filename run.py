from Processes.Analyze_Vocabulary.run import main as analyze_vocabulary
from Processes.Extract_Keywords.run import main as extract_keywords

def process_data():
	extract_keywords()


if __name__ == '__main__':
	process_data()