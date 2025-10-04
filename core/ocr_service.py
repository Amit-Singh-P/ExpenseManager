import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from datetime import datetime

def extract_text_from_image(image_path):
    """Extract text from receipt image using OCR"""
    try:
        # Read image
        img = cv2.imread(image_path)
        
        # Preprocess image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Extract text
        text = pytesseract.image_to_string(Image.fromarray(thresh))
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def parse_receipt_data(text):
    """Parse receipt text and extract relevant information"""
    data = {
        'amount': None,
        'date': None,
        'merchant': None,
        'description': text[:200] if text else ""
    }
    
    # Extract amount (looking for currency symbols and numbers)
    amount_pattern = r'[\$£€¥₹]\s*(\d+[.,]\d{2})|(\d+[.,]\d{2})\s*[\$£€¥₹]'
    amount_matches = re.findall(amount_pattern, text)
    if amount_matches:
        amount_str = ''.join(amount_matches[0]).replace(',', '.')
        try:
            data['amount'] = float(re.findall(r'\d+\.\d{2}', amount_str)[0])
        except:
            pass
    
    # Extract date
    date_patterns = [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            try:
                date_str = date_match.group()
                for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
                    try:
                        data['date'] = datetime.strptime(date_str, fmt).date()
                        break
                    except:
                        continue
            except:
                pass
            if data['date']:
                break
    
    # Extract merchant name (usually at the top of the receipt)
    lines = text.split('\n')
    for line in lines[:5]:
        if len(line.strip()) > 3 and not any(char.isdigit() for char in line):
            data['merchant'] = line.strip()
            break
    
    return data