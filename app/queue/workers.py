from ..db.collections.files import files_collection
from bson import ObjectId

# updating status now we are actually processing the file with id that created by mongo and picked from queue in FIFO manner
async def process_file(id : str):
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set":{
                "status":"Processing"
            }
        }
    )

