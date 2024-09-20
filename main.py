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

image_bytes = query({
	"inputs": "Astronaut riding a horse",
})


# Convert image bytes to a PIL Image object
image = Image.open(io.BytesIO(image_bytes))

# Display the image
image.show()
