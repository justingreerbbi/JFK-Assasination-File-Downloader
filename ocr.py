import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import os
import sqlite3

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('extracted_texts.db')
cursor = conn.cursor()

# Create a new table to store the file names and extracted text
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

# Function to save extracted text to the database
def save_to_db(filename, content):
    cursor.execute('''
    INSERT INTO documents (filename, content)
    VALUES (?, ?)
    ''', (filename, content))
    conn.commit()

# Close the database connection when done
def close_db():
    conn.close()

def pdf_to_text(pdf_path):
    text_output = []

    # Open the PDF
    pdf_doc = fitz.open(pdf_path)
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)

        # Render page to image
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")

        # Convert to PIL Image
        image = Image.open(io.BytesIO(img_data))

        # OCR the image
        text = pytesseract.image_to_string(image)
        text_output.append(f"--- Page {page_num + 1} ---\n{text.strip()}\n")

    pdf_doc.close()
    return "\n".join(text_output)

# Example usage
if __name__ == "__main__":
    downloads_dir = "downloads"
    for filename in os.listdir(downloads_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(downloads_dir, filename)
            extracted_text = pdf_to_text(pdf_path)
            save_to_db(filename, extracted_text)
            print(f"Extracted text from {filename}:\n{extracted_text}\n")