from  PyPDF2 import PdfFileReader

path = "/Users/minsu.kim/Documents/test.pdf"
with open(path, 'rb') as f:
    pdf=PdfFileReader(f)
    print (pdf.getNumPages())