import os
import PyPDF2
from tkinter import filedialog

def split_pdf(input_pdf_path, pages_per_file):
    # Open the input PDF file
    input_pdf = PyPDF2.PdfReader(input_pdf_path)
    
    # Calculate the number of files needed
    total_pages = len(input_pdf.pages)
    num_files = total_pages // pages_per_file + (1 if total_pages % pages_per_file > 0 else 0)
    
    # Create output directory
    output_dir = os.path.splitext(input_pdf_path)[0] + "_splits"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split the PDF
    for i in range(num_files):
        output_pdf_path = os.path.join(output_dir, f"split_{i+1}.pdf")
        output_pdf = PyPDF2.PdfWriter()
        
        # Calculate the range of pages for the current split
        start_page = i * pages_per_file
        end_page = min(start_page + pages_per_file, total_pages)
        
        # Add pages to the output PDF
        for page_number in range(start_page, end_page):
            output_pdf.add_page(input_pdf.pages[page_number])
        
        # Save the output PDF
        with open(output_pdf_path, "wb") as output_pdf_file:
            output_pdf.write(output_pdf_file)
        
        print(f"Created: {output_pdf_path}")

# Example usage
input_pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")]) # Change this to the path of your PDF
pages_per_file = 30
split_pdf(input_pdf_path, pages_per_file)
