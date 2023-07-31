import strawberry
from typing import Optional
from config.database import crud_operation_collection
from models.adminModel import CrudOperationResponse
from bson import ObjectId
from typing import List


from jwtAuthentication.authorization import IsAdminAuthenticated



@strawberry.field(permission_classes=[IsAdminAuthenticated])
async def getCrudOperation(id : Optional[str] = None) -> List[CrudOperationResponse]:
    
    if id != None:
        data = await crud_operation_collection.find_one({"_id":ObjectId(id)})
        if data:
            return [CrudOperationResponse(id=str(data["_id"]), operationName=data["operationName"],operationCreateTime=data["operation_create_time"], operationLastUpdateTime = data["operation_last_update_time"])]
        else:
            raise Exception("No crud operation found in this id.")
    else:
        data = [CrudOperationResponse(id=str(data["_id"]), operationName=data["operationName"],operationCreateTime=data["operation_create_time"], operationLastUpdateTime = data["operation_last_update_time"]) async for data in crud_operation_collection.find()]
        if data:
            return data
        else:
            raise Exception("No crud operation  found in database")