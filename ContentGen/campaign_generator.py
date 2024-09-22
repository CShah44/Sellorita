import requests
import dotenv
import os
from PIL import Image
from pydantic import BaseModel
import google.generativeai as genai
import json
from .text_to_ad_image import get_image_from_prompt

dotenv.load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
api_key = os.getenv("GEMINI_API_KEY")


API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

genai.configure(api_key=api_key)

class Post(BaseModel):
    prompt: str
    caption: str

model = genai.GenerativeModel("gemini-1.5-flash", generation_config={
    "response_mime_type": "application/json",
})

def get_all_image(posts):
    image_urls = []
    for post in posts:
        image_urls.append(get_image_from_prompt(post.get("image_prompt")))

    return image_urls

def generate_campaign(data):
    # Extract the necessary information from the data
    brand_name = data.get('brand_name')
    product_name = data.get('product_name')
    brand_description = data.get('brand_description')
    product_description = data.get('product_description')
    target_audience = data.get('target_audience')
    no_of_posts = min(int(data.get('no_of_posts', 1)), 4)  # Ensure max 4 posts
    additional_design_details = data.get('additional_design_details')

    new_prompt = f"""Generate a series of {no_of_posts} social media posts for a promotional advertisement campaign. Each post should include an image prompt for generation and a caption.

    Brand: {brand_name}
    Brand Description: {brand_description}
    Product: {product_name}
    Product Description: {product_description}
    Target Audience: {target_audience}
    Additional Design Details: {additional_design_details}

    Create engaging and creative posts that will catch the attention of the target audience. Each post should effectively promote the product while aligning with the brand's identity.

    Respond with a JSON array of post objects, where each object has the following structure:
    {{
        "image_prompt": "Detailed prompt for image generation",
        "caption": "Engaging caption for the social media post"
    }}

    Ensure that the response contains exactly {no_of_posts} post objects."""

    response = model.generate_content(new_prompt)

    posts = json.loads(response.text)
    
    image_urls = get_all_image(posts)

    captions = [post.get("caption") for post in posts]

    return image_urls, captions
