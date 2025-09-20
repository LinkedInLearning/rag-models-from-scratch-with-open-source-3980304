from docling.document_converter import DocumentConverter
# pip install accelerate


def convert_doc(source):
    converter = DocumentConverter()
    result = converter.convert(source)

    return result.document.export_to_dict()

pptx_source = "https://scholar.harvard.edu/files/torman_personal/files/samplepptx.pptx"
docx_source = "https://calibre-ebook.com/downloads/demos/demo.docx"
pdf_source = "https://pdfobject.com/pdf/sample.pdf"

result = convert_doc(docx_source)

for i in result["texts"]:
    print(i["orig"])
