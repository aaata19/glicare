import random
import sys
import os
import datetime
import barcode
from barcode.writer import ImageWriter
from barcode import EAN13
from barcode import generate
from barcode.writer import SVGWriter
from fpdf import FPDF
from pdf2image import convert_from_path

def generareAdeverinta(nume, prenume, cnp, data_nasterii,adresa, ocupatie, motiv, loc, medic, clinica):
    diagnostic = "diabet tip 1"
    # data emiterii adeverintei
    data = datetime.datetime.now().strftime("%d-%m-%Y")

    # generare cod de bare
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    ean = EAN13(random_number, writer=ImageWriter())
    filename = ean.save('ean13')


    # creare PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.cell(200, 10, txt="ADEVERINTA MEDICALA", ln=True, align="C")
    pdf.cell(200, 10, txt=" ", ln=True, align="L")
    text = f"Se adevereste ca {nume} {prenume}, sexul F, CNP {cnp}, Nascut/a la data de {data_nasterii} Cu domiciliul in {adresa}, avand ocupatia de {ocupatie}"
    pdf.multi_cell(200, 10, txt=text, align='C')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    text = f"Este suferind de Diabet Tip 1 si se recomanda {motiv}"
    pdf.multi_cell(200, 10, txt=text, align='L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    text = f"S-a eliberat pentru a-i servi la {loc}"
    pdf.multi_cell(200, 10, txt=text, align='L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.cell(200, 10, txt="Numele medicului", ln=True, align="L")
    pdf.cell(200, 10, txt=medic, ln=True, align="L")
    pdf.cell(200, 10, txt="Numele unitatii medicale", ln=True, align="L")
    pdf.cell(200, 10, txt=clinica, ln=True, align="L")
    pdf.cell(200, 10, txt="Data emiterii adeverintei", ln=True, align="L")
    pdf.cell(200, 10, txt=data, ln=True, align="L")
    pdf.cell(200, 10, txt="Semnatura medicului", ln=True, align="L")
    pdf.image(filename, x=0, y=0, w=50)
    pdf_file = "adeverinta_medicala.pdf"
    pdf.output(pdf_file)

    # Convert the PDF to a PNG
    images = convert_from_path(pdf_file)
    png_file = pdf_file.replace('.pdf', '.png')
    images[0].save(png_file, 'PNG')

    with open(png_file, 'rb') as f:
        blob = f.read()

    os.remove(png_file)

    return blob