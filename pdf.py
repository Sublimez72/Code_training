import PyPDF2 as pdf


path = ""


with open(path, "rb") as file:
    reader = pdf.PdfFileReader(file)
    page_1 = reader.getPage(0)
    pdf_text = page_1.extractText()
    print(pdf_text)

    print(reader.numPages)
