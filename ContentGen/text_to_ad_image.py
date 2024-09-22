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

def get_image(brand_details, product_details, type_of_ad, target_audience):
	
    prompt = f"You are an expert marketing assistant that is proficient in creating engaging promotional advertisements. Create a promotional advertisment for the brand name, {brand_details['brand_name']}. Here are some details about the brand: ${brand_details["about_brand"]}. Create an ad for their new product, {product_details['product_name']}. Here is the product description: {product_details["product_description"]} . The advertisement is for {type_of_ad}. The advertisement is targeted for {target_audience}. The ad should be creative, engaging and should catch the attention of the audience"

    image_bytes = query({ "inputs": prompt })

    # Convert image bytes to a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    return image

def get_image_from_prompt(prompt):
    image_bytes = query({ "inputs": prompt })

    # Convert image bytes to a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    return image
      