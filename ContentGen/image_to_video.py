import requests
import dotenv
import os
import io
import time

dotenv.load_dotenv()

STABLITY_API_KEY = os.getenv("STABILITY_API_KEY")

def get_video_id(image):
    # Resize the image to 768x768
    resized_image = image.resize((768, 768))

    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    response = requests.post(
        f"https://api.stability.ai/v2beta/image-to-video",
        headers={
            "authorization": f"Bearer {STABLITY_API_KEY}"
        },
        files={
            "image": ("image.jpg", img_byte_arr, "image/jpeg")
        },
        data={
            "seed": 0,
            "cfg_scale": 3.5,
            "motion_bucket_id": 150
        },
    )

    generated_id = response.json().get('id')

    return generated_id

def generate_video_ad(image):
    generation_id = get_video_id(image)
    
    max_attempts = 30  # Adjust this based on expected generation time
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.request(
            "GET",
            f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
            headers={
                'accept': "video/*",
                'authorization': f"Bearer {STABLITY_API_KEY}"
            },
        )
        
        if response.status_code == 200:
            return response.content
        elif response.status_code == 202:
            time.sleep(10)  # Wait for 10 seconds before next attempt
            attempt += 1
        else:
            raise Exception(str(response.json()))
    
    raise Exception("Video generation timed out")

