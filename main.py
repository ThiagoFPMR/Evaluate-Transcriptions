import os
import string
import difflib as dl
from jiwer import wer
from datetime import datetime
import matplotlib.pyplot as plt
from write_pdf import write_pdf
# Defines the paths to the transcription files
truth_path = 'transcriptions/original'
input_path = 'transcriptions/generated'
# Uses the current time to create a unique folder to store the output of the program
now = datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
comparsions_folder = f'output/comparsions/{current_time}'
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
        og = file.read().lower().translate(str.maketrans('', '', string.punctuation)).split()
    with open(input) as file:
        new = file.read().lower().translate(str.maketrans('', '', string.punctuation)).split()
    # Calculates the series of operations necessary to turn 'new' into 'og
    seq_matcher = dl.SequenceMatcher(None, new, og)
    changelog = seq_matcher.get_opcodes()
    # Creates a pdf file comparing the two strings and the changes necessary to turn one into another
    write_pdf(new, og, changelog, f'{comparsions_folder}/{os.listdir(truth_path)[i][:-4]}.pdf')
    # Stores the Word Error Rate into a vector
    wer_values.append(wer(' '.join(og), ' '.join(new)))
# Plots the Word Error Rates for the different transcript comparsions
# and saves the image of the plot locally in the comparsions folder
plt.style.use('fivethirtyeight')
fig, axs = plt.subplots()
fig.tight_layout(pad=2)
axs.set_title("WER")
axs.bar([c[:-4] for c in os.listdir(comparsions_folder)], wer_values)
plt.savefig(f'{comparsions_folder}/wer.jpg')

