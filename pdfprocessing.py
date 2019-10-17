from  PyPDF2 import PdfFileReader
import os, fnmatch

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def getpdfnumpages(path):
    #path = "/Users/minsu.kim/Documents/test.pdf"
    paths = find('*.pdf', path)
    sum = 0
    for path in paths:
        with open(path, 'rb') as f:
            pdf=PdfFileReader(f)
            info = pdf.getDocumentInfo()
            #print(info)
            print (sum, pdf.getNumPages())
            sum += pdf.getNumPages()
    return sum
if __name__ == '__main__':
    result=getpdfnumpages('/Users/minsu.kim/Desktop/PDF')
    print(result)
