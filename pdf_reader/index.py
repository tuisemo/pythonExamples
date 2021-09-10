import pdfplumber

with pdfplumber.open("./poem.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    print(text)