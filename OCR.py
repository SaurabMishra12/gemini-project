import fitz
import pytesseract
from PIL import Image
from fpdf import FPDF


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        all_text.append(text)

    return all_text


text_data = extract_text_from_pdf("IIT-JEE-Formula-PCM-NoLogo.pdf")




def save_text_to_pdf(text_data, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for text in text_data:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)

    pdf.output(output_pdf)


save_text_to_pdf(text_data, "IIT JEE Formulae combined PCM.pdf")
