from fpdf import FPDF

def write_pdf (new, og, changelog, pdf_path):
    """
    A function that takes as input two strings and a changelog containing a series of change tuples.
    The function writes the comparsion between the strings as a pdf, saving it to the specified path.

    This function does not return anything.

    Parameters
    -------------
    new : iterable
        The string that is being compared to another one

    og : iterable
        The string that serves as reference for the comparsion
    
    changelog : iterable of iterables
        An iterable of iterables containing the changes made to the string

    pdf_path : str
        Contains the path at which the pdf file comparing both sentences will be stored.
    """
    # Creates the FPDF object to register the changes in changelog
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    # Defines the vertical spacing to be used
    v_spacing = 7
    # Iterates over the steps in the changelog and writes the comparsion between the two strings
    # into the FPDF object
    for step in changelog:
        # Writes the text in the interval of the current step in black
        # if it's 'equal'
        if step[0] == 'equal':
            pdf.set_text_color(0, 0, 0)
            for i in range(step[1], step[2]):
                pdf.write(v_spacing, new[i] + ' ')
        # Writes the text being added from 'og' in green
        elif step[0] == 'insert':
            pdf.set_text_color(69, 235, 47)
            for i in range(step[3], step[4]):
                pdf.write(v_spacing, og[i] + ' ')
        # Writes the text being deleted from 'new' in red
        elif step[0] == 'delete':
            pdf.set_text_color(235, 65, 52)
            for i in range(step[3], step[4]):
                pdf.write(v_spacing, og[i] + ' ')
        # Writes the replaced text in red and the replacement text in green
        elif step[0] == 'replace':
            # Writes the segment of the 'new' string being replaced in red
            pdf.set_text_color(235, 65, 52)
            for i in range(step[1], step[2]):
                pdf.write(v_spacing, new[i] + ' ')
            # Writes the replacement segment from the 'og' string in green
            pdf.set_text_color(69, 235, 47)
            for i in range(step[3], step[4]):
                pdf.write(v_spacing, og[i] + ' ')
    # Creates the pdf contaning the changed string     
    pdf.output(pdf_path)