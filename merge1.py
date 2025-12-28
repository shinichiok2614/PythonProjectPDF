# pip install pypdf
from pypdf import PdfReader, PdfWriter

pdf_files = [
    "nkls12.pdf",
    "nkls3.pdf",
    "nkls4114.pdf"
]

writer = PdfWriter()

for pdf in pdf_files:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

output_file = "merge_output.pdf"
with open(output_file, "wb") as f:
    writer.write(f)

print("Đã ghép xong:", output_file)
