import os
import time
import pytesseract
from pdf2image import convert_from_path

# Define Poppler path (update if needed)
POPPLER_PATH = r"/usr/bin"

# Define PDF and output directories
BASE_DIRECTORY = os.getcwd()
PDF_DIRECTORY = os.path.join(BASE_DIRECTORY, "pdf")
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "converted_texts")

# Ensure output directory exists
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Get all PDF files in the directory
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]

# Start processing
if not pdf_files:
    print("No PDF files found in the directory.")
else:
    print(f"Found {len(pdf_files)} PDF files. Starting conversion...\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_DIRECTORY, pdf_file)
    output_txt_path = os.path.join(OUTPUT_DIRECTORY, f"{os.path.splitext(pdf_file)[0]}.txt")

    # Skip if already converted
    if os.path.exists(output_txt_path):
        print(f"⏭️ Skipping {pdf_file} (already converted).")
        continue

    print(f"Processing: {pdf_file}")

    try:
        # Convert PDF pages to images (one page at a time)
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        print(f"  → Found {len(images)} pages.\n")

        # Open output text file
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            for i, image in enumerate(images, start=1):
                print(f"    → Processing page {i}/{len(images)}...")

                # Extract text from the current page
                text = pytesseract.image_to_string(image)

                # Write to output file
                txt_file.write(f"\n--- Page {i} ---\n{text}\n")

                # Print progress for each line of text
                for line in text.split("\n"):
                    if line.strip():  # Ignore empty lines
                        print(f"    → Page {i}: {line.strip()}")

                # Simulate a short delay for better tracking (remove if not needed)
                time.sleep(0.3)

        print(f"\n✅ Finished processing {pdf_file}. Output saved to: {output_txt_path}\n")

    except Exception as e:
        print(f"❌ Error processing {pdf_file}: {e}")

print("\n🎉 All PDFs processed successfully!")
