import PyPDF2

pdf_file = PyPDF2.PdfFileReader(open("CompTIA Security.pdf"))
doc_info = pdf_file.getDocumentInfo()
for info in doc_info:
    print("[+] " + info)
