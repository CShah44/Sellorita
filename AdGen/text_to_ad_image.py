import requests
import dotenv
import os
import io
from PIL import Image

dotenv.load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

# product_details is of format { product_name: "", product_description: "" }
# brand_details is of format { brand_name: "", brand_vision: "", about_brand: "" }
# user_description is like how the user would like the advertisement should be - engaging, unique, creative, etc
# type_of_ad is like "social media campaign" or "billboard" or "print" or "sale offer"

def get_image(brand_details, product_details, user_description, type_of_ad):
	
    prompt = ""

    image_bytes = query({ "inputs": prompt })

    # Convert image bytes to a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    # Save the image to a temporary file
    temp_file = io.BytesIO()
    image.save(temp_file, format='PNG')
    temp_file.seek(0)
    
    return temp_file
    

   