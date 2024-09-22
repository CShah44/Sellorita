import requests
import dotenv
import os
import io

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
            "cfg_scale": 2.5,
            "motion_bucket_id": 200
        },
    )

    generated_id = response.json().get('id')

    print(response.json())

    return generated_id

def generate_video_ad(image):

    generation_id = get_video_id(image)

    print(len(generation_id))

    response = requests.request(
        "GET",
        f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
        headers={
            'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer {STABLITY_API_KEY}"
        },
    )

    if response.status_code == 202:
        print("Generation in-progress, try again in 10 seconds.")
    elif response.status_code == 200:
        print("Generation complete!")
        return response.content
    else:
        print(response.json())
        raise Exception(str(response.json()))

