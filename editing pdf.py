import fitz  # PyMuPDF


def remove_logo(pdf_path, output_path, logo_rect):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        # Fill the logo area with white
        page.draw_rect(logo_rect, color=(1, 1, 1), fill=True)

    doc.save(output_path)


# Example coordinates (x0, y0, x1, y1) for the logo
logo_rect = fitz.Rect(450, 20, 550, 80)
remove_logo("/mnt/data/iitjee_formulae.pdf", "IIT-JEE-Formula-PCM-NoLogo.pdf", logo_rect)
