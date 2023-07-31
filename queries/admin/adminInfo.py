import strawberry
from typing import Optional
from config.database import admin_collection
from models.adminModel import AdminResponse

from bson import ObjectId
from typing import List


from jwtAuthentication.authorization import IsAdminAuthenticated



    


@strawberry.field(permission_classes=[IsAdminAuthenticated])
async def getAdmin(id : Optional[str] = None) -> List[AdminResponse]:
    
    if id != None:
        data = await admin_collection.find_one({"_id":ObjectId(id)})
        if data:
            return [AdminResponse(id=str(data["_id"]), email=data["email"],status=data["status"])]
        else:
            raise Exception("No admin found in this id.")
    else:
        data = [AdminResponse(id=str(admin["_id"]), email=admin["email"],status=admin["status"]) async for admin in admin_collection.find()]
        if data:
            return data
        else:
            raise Exception("No admin found in database")
    
    





   