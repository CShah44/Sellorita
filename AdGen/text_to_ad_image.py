import requests
import dotenv
import os
import io
from PIL import Image
import torch
from diffusers import StableDiffusionImg2ImgPipeline

dotenv.load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

# product_details is of format { product_name: "", product_description: "" }
# brand_details is of format { brand_name: "", about_brand: "" }
# type_of_ad is like "social media campaign" or "billboard" or "print" or "sale offer"
# target_audience is like "kids" or "teens" or "adults" or "seniors"
# kandinsky-community/kandinsky-2-2-decoder
def get_image(brand_details, product_details, type_of_ad, target_audience):
	
    prompt = f"You are an expert marketing assistant that is proficient in creating engaging promotional advertisements. Create a promotional advertisment for the brand name, {brand_details['brand_name']}. Here are some details about the brand: ${brand_details["about_brand"]}. Create an ad for their new product, {product_details['product_name']}. Here is the product description: {product_details["product_description"]} . The advertisement is for {type_of_ad}. The advertisement is targeted for {target_audience}. The ad should be creative, engaging and should catch the attention of the audience"

    image_bytes = query({ "inputs": prompt })

    # Convert image bytes to a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    #todo testing only 
    model_id = "stabilityai/stable-diffusion-xl-refiner-1.0"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)

    init_image = Image.open("path_to_your_initial_image.jpg").convert("RGB")
    prompt = "A beautiful landscape painting"

    result = pipe(prompt=prompt, init_image=init_image, strength=0.75, guidance_scale=7.5)
    result.images[0].save("output_image.png")

    return 