import os
from compare_transcriptions import compare_transcriptions

with open('transcriptions/original/Dupla 1 Sala 1 (1).txt') as file:
    og = file.read().split()
with open('transcriptions/generated/Gravação (2).txt') as file:
    new = file.read().split()

changelog = []
compare_transcriptions(og, new, changelog)

from fpdf import FPDF

def write_pdf_comparsion(new, changelog, pdf_path=None):
    """
    A function.
    """
     # Creates the FPDF object to register the changes in changelog
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    # Defines the vertical spacing to be used
    v_spacing = 7

    next_change = 0
    i = 0
    while i < len(new):
        if next_change < len(changelog):
            print(i, 'bruh')
            if i == changelog[next_change][0]:
                if changelog[next_change][1] == 'deleted':
                    pdf.set_text_color(235, 65, 52)
                    pdf.write(v_spacing, new[i] + ' ')
                    print(new[i], 'deletion')
                    i += 1
                elif changelog[next_change][1] == 'inserted':
                    pdf.set_text_color(69, 235, 47)
                    pdf.write(v_spacing, changelog[next_change][2] + ' ')
                    print(new[i], 'insertion')

                else:
                    pdf.set_text_color(235, 65, 52)
                    pdf.write(v_spacing, new[i] + ' ')
                    pdf.set_text_color(69, 235, 47)
                    pdf.write(v_spacing, changelog[next_change][2] + ' ')
                    i += 1
                next_change += 1
                print(new[i], 'continue')
                continue
        pdf.set_text_color(0, 0, 0)
        pdf.write(v_spacing, new[i] + ' ')
        i += 1
    # Creates the pdf contaning the comparsion between the input and truth sentences        
    if pdf_path != None:
        pdf.output(pdf_path)

from datetime import datetime
now = datetime.now()
current_time = now.strftime('%Y-%m-%d-%H-%M-%S')
comparsions_folder = f'output/comparsions/{current_time}'
os.makedirs(comparsions_folder)

write_pdf_comparsion(new, changelog, f'{comparsions_folder}/yeet.pdf')
print(changelog)