# data_analysis_lts
Let them speak is a project that prepares a data edition of Holocaust testimonies. This repository contains the code to analyze testimonies featuring in this project quantitatively.
Precisely, the repository contains code to pre-process the data set underlying the Let them speak project, and jupyther notebooks to analyze data.

The current website of the project: https://lts.fortunoff.library.yale.edu/

## Requirements to run code in this repository
- Mongo database belonging to the Let them speak project
- Blacklab Corpus Engine empowering the Let them speak project
- jupyther notebook installed
- python3
- Data folder archived by @toth12


## How to run code in this repository

1. First install the requirements:

`pip install -r requirements.txt`

2. Run code to pre-process data

`python DataProcessing/calculate_token_numbers.py`

`python DataProcessing/process_Fortunoff_metadata.py`

`python DataProcessing/process_USC_metadata.py`

3. Run the notebooks

`cd Notebooks/`

`jupyter notebook`





