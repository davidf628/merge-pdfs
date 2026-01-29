from pypdf import PdfReader, PdfWriter
import os
import argparse
import logging

# Suppress nonsense warnings
logging.getLogger("pypdf").setLevel(logging.ERROR)

def merge_pdfs_simplex(output_filename):
    writer = PdfWriter()
    total_pages = 0

    pdf_files = sorted(
        f for f in os.listdir(".")
        if f.lower().endswith(".pdf") and f != output_filename
    )

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)

        # If current page count is odd, insert a blank page
        if total_pages % 2 == 1:
            last_page = writer.pages[-1]
            writer.add_blank_page(
                width=last_page.mediabox.width,
                height=last_page.mediabox.height
            )
            total_pages += 1

        # Append pages from the current PDF
        for page in reader.pages:
            writer.add_page(page)

        total_pages += num_pages

    with open(output_filename, "wb") as f:
        writer.write(f)

    print(f"Merged {len(pdf_files)} PDFs into '{output_filename}'")

def main():
    parser = argparse.ArgumentParser(
        description="Merge PDFs so each document starts on a front (odd-numbered) page."
    )
    parser.add_argument(
        "-o", "--output",
        default="merged.pdf",
        help="Name of the output PDF file (default: merged.pdf)"
    )

    args = parser.parse_args()
    merge_pdfs_simplex(args.output)

if __name__ == "__main__":
    main()