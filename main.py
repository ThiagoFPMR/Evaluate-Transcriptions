import os
import difflib as dl
from datetime import datetime
from write_pdf import write_pdf

with open('transcriptions/original/Dupla 1 Sala 1 (1).txt') as file:
    og = file.read().split()
with open('transcriptions/generated/Gravação (2).txt') as file:
    new = file.read().split()
# Uses the current time to create a unique folder to store the output of the program
now = datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
comparsions_folder = f'output/comparsions/{current_time}'
os.makedirs(comparsions_folder)
# Calculates the series of operations necessary to turn 'new' into 'og
seq_matcher = dl.SequenceMatcher(None, new, og)
changelog = seq_matcher.get_opcodes()
# Creates a pdf file comparing the two strings and the changes necessary to turn one into another
write_pdf(new, og, changelog, f'{comparsions_folder}/test.pdf')
print(changelog)
print(len(changelog))

