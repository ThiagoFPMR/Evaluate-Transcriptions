import os
import difflib as dl
from datetime import datetime
from write_pdf import write_pdf
# Defines the paths to the transcription files
truth_path = 'transcriptions/original'
input_path = 'transcriptions/generated'
# Uses the current time to create a unique folder to store the output of the program
now = datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
comparsions_folder = f'output/comparsions/{current_time}'
os.makedirs(comparsions_folder)
# Iterates over all transcription file pairs for comparsion
for i in range(len(os.listdir(truth_path))):
    # Stores the file paths of the files to be read in the variables below
    truth = f'{truth_path}/{os.listdir(truth_path)[i]}'
    input = f'{input_path}/{os.listdir(input_path)[i]}'
    # Opens the files and stores them into variables
    with open(truth) as file:
        og = file.read().split()
    with open(input) as file:
        new = file.read().split()
    # Calculates the series of operations necessary to turn 'new' into 'og
    seq_matcher = dl.SequenceMatcher(None, new, og)
    changelog = seq_matcher.get_opcodes()
    # Creates a pdf file comparing the two strings and the changes necessary to turn one into another
    write_pdf(new, og, changelog, f'{comparsions_folder}/{os.listdir(truth_path)[i][:-4]}.pdf')

