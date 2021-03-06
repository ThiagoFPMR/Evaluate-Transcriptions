import os
import string
import argparse
from unidecode import unidecode
import difflib as dl
from jiwer import wer
from datetime import datetime
import matplotlib.pyplot as plt
from write_pdf import write_pdf
# Defines command line arguments to be accepted
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input_path', required=False,
 help = 'Path to the folder contaning the transcriptions to be compared.')
ap.add_argument('-t', '--truth_path', required=False,
 help = 'Path to the folder contaning the transcriptions to be used as reference.')
ap.add_argument('-o', '--output_path', required=False,
 help = 'Path to the folder where the output folders will be stored.')
args = vars(ap.parse_args())
# Defines the paths to the transcription files
if args['input_path'] != None:
    input_path = args['input_path']
else:
    input_path = 'transcriptions/generated'
if args['truth_path'] != None:
    truth_path = args['truth_path']
else:
    truth_path = 'transcriptions/original'
if args['output_path'] != None:
    output_path = args['output_path']
else:
    output_path = 'output'
 # Uses the current time to create a unique folder to store the output of the program
now = datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
comparsions_folder = f'{output_path}/{current_time}'
os.makedirs(comparsions_folder)
# Creates a vector to store Word Error Rate values for the different comparsions being made
wer_values = []
# Iterates over all transcription file pairs for comparsion
for i in range(len(os.listdir(truth_path))):
    # Stores the file paths of the files to be read in the variables below
    truth = f'{truth_path}/{os.listdir(truth_path)[i]}'
    input = f'{input_path}/{os.listdir(input_path)[i]}'
    # Opens the files and stores them into variables
    with open(truth) as file:
        og = unidecode(file.read().lower().translate(str.maketrans('', '', string.punctuation))).split()
    with open(input) as file:
        new = unidecode(file.read().lower().translate(str.maketrans('', '', string.punctuation))).split()
    # Calculates the series of operations necessary to turn 'new' into 'og
    seq_matcher = dl.SequenceMatcher(None, new, og)
    changelog = seq_matcher.get_opcodes()
    # Creates a pdf file comparing the two strings and the changes necessary to turn one into another
    write_pdf(new, og, changelog, f'{comparsions_folder}/{os.listdir(input_path)[i][:-4]}.pdf')
    # Stores the Word Error Rate into a vector
    wer_values.append(wer(' '.join(og), ' '.join(new)))
# Plots the Word Error Rates for the different transcript comparsions
# and saves the image of the plot locally in the comparsions folder
plt.style.use('default')
plt.title("WER")
plt.bar([c[:-4] for c in os.listdir(comparsions_folder)], wer_values, width=0.35, color='royalblue')
plt.xticks([label[:-4] for label in os.listdir(input_path)], rotation=90)
plt.tight_layout()
plt.savefig(f'{comparsions_folder}/wer.jpg')

