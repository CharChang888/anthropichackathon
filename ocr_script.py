from PIL import Image
import pytesseract
import cv2
import re
import csv

# load the image
image_path = "testReceipt2.png"
image = cv2.imread(image_path)

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform OCR
text = pytesseract.image_to_string(gray)

# save or print output
print("OCR output")
print(text)

lines = text.split('\n')
items = []

for line in lines:
    # Skip empty lines
    if not line.strip():
        continue
        
    # Skip lines that look like addresses (contain typical address keywords or patterns)
    address_keywords = ['street', 'st', 'ave', 'avenue', 'rd', 'road', 'lane', 'ln', 'blvd', 'suite']
    if any(keyword.lower() in line.lower() for keyword in address_keywords):
        continue
        
    # Skip lines with typical header/footer content
    skip_keywords = ['tel:', 'phone:', 'thank you', 'receipt', 'order', 'subtotal', 'total', 'tax', 
                    'cash', 'change', 'credit card', 'debit', 'balance', 'date:', 'time:', 'visa']
    if any(keyword.lower() in line.lower() for keyword in skip_keywords):
        continue

    # Try to match items with different formats:
    # Format 1: Item with quantity and price (e.g., "Banana 2 @ $1.99")
    # Format 2: Item with just price (e.g., "Bread $3.99")
    match = re.search(r"^([a-zA-Z][a-zA-Z\s\-&]+)\s+(?:([\d\.]+)\s*[@x]?\s*)?\$?([\d\.]+)", line.strip())
    if match:
        item = match.group(1).strip()
        # Additional validation: item should be reasonable length and not too short
        if 2 <= len(item) <= 50:  # adjust these numbers based on your needs
            try:
                # If quantity is not present, default to 1
                quantity = float(match.group(2)) if match.group(2) else 1.0
                price = float(match.group(3))
                # Additional validation: prices and quantities should be reasonable
                if 0 < quantity < 100 and 0 < price < 1000:  # adjust these ranges based on your needs
                    items.append({
                        "item": item,
                        "quantity": quantity,
                        "unit_price": price,
                        "total": quantity * price
                    })
            except ValueError:
                # Skip if number conversion fails
                continue

with open("receipt_items.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["item", "quantity", "unit_price", "total"])
    writer.writeheader()
    writer.writerows(items)

# Display results
for item in items:
    print(item)

print("CSV file has been created successfully.")