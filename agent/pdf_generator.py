import os
from fpdf import FPDF 

# def generate_pdf(employee_name, offer_letter_text):

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)

#     for line in offer_letter_text.split("\n"):
#         pdf.multi_cell(0, 10, line)

#     output_dir = "output/generated_letters"
#     os.makedirs(output_dir, exist_ok=True)
#     file_path = os.path.join(output_dir, f"{employee_name.replace(' ', '_')}_Offer_Letter.pdf")
    
#     pdf.output(file_path)
    
#     return file_path

import pdfkit

def generate_pdf(employee_name, html_string):
    output_dir = "output/generated_letters"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{employee_name.replace(' ', '_')}_Offer_Letter.pdf")

    options = {
        "enable-local-file-access": None,
        "encoding": "UTF-8"
    }

    pdfkit.from_string(html_string, file_path, options=options)
    return file_path

