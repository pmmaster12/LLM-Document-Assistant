from ..db.collections.files import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import os
from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

async def process_file(id: str, file_path: str):
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "Processing"}}
    )

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "Converting to Images"}}
    )

    # Step 1: Convert PDF to list of images
    pages = convert_from_path(file_path)
    images = []

    # Save each page as an image file
    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "Extracted images from Document and Saved to Disk"}}
    )

    images_base64 = [encode_image(img) for img in images]

    # CORRECTED: Use proper OpenAI-compatible API structure
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",  # Use correct Gemini model name
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Based on the resume below, roast this resume"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{images_base64[0]}"
                        }
                    }
                ]
            }
        ]
    )

    # Extract the response text
    result_text = response.choices[0].message.content

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "processed",
                "result": result_text
            }
        }
    )