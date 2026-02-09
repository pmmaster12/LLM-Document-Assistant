from ..db.collections.files import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import os
from openai import OpenAI
import base64
# updating status now we are actually processing the file with id that created by mongo and picked from queue in FIFO manner
async def process_file(id : str, file_path: str):
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set":{
                "status":"Processing"
            }
        }
    )

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set":{
                "status":"Converting to Images"
            }
        }
    )

    # step1: convert pdf to list of images
    pages = convert_from_path(file_path)

    # Save each page as an image file
    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path),exist_ok=True)
        page.save(image_save_path,'JPEG')

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set":{
                "status":"Extracted images from Document and Saved to Disk"
            }
        }
    )








