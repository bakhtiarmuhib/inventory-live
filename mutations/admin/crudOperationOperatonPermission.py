from fastapi.encoders import jsonable_encoder
from config.database import crud_operation_collection
from strawberry.types import Info
from bson.objectid import ObjectId
import strawberry
import datetime

from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data
from models.adminModel import CrudOperationCreateInput,CrudOperationResponse
from jwtAuthentication.authorization import IsAdminAuthenticated




#Create crud operation
@strawberry.mutation(permission_classes=[IsAdminAuthenticated])
async def CreateCrudOperation( data : CrudOperationCreateInput) -> CrudOperationResponse:
    find_exist_data = await crud_operation_collection.find_one({"operationName": data.operationName})
    if find_exist_data:
        raise Exception("Operation name already exist in database.")
    new_crud_data = jsonable_encoder(
        {
        "operationName": data.operationName,
        "operation_create_time" : datetime.datetime.now(),
        "operation_last_update_time" : None
        })
    new_operation = await crud_operation_collection.insert_one(new_crud_data)
    data = await crud_operation_collection.find_one({"_id": new_operation.inserted_id})
    
    return CrudOperationResponse(id=str(data["_id"]), operationName=data["operationName"],operationCreateTime=data["operation_create_time"], operationLastUpdateTime = data["operation_last_update_time"])



@strawberry.mutation(permission_classes=[IsAdminAuthenticated])
async def updateCrudOperation(id :str, data : CrudOperationCreateInput) -> CrudOperationResponse:
    find_exist_data = await crud_operation_collection.find_one({"operationName": data.operationName})
    if find_exist_data:
        raise Exception("Operation name already exist in database.")
    new_crud_data = jsonable_encoder(
        {
        "operationName": data.operationName,
        "operation_last_update_time" : datetime.datetime.now()
        })
    get_crud = await crud_operation_collection.find_one({ "_id": ObjectId(id)})
    if not get_crud:
        raise Exception("Operation not found in database")
    newvalues = { "$set": new_crud_data}

    await crud_operation_collection.update_one({ "_id": ObjectId(id)}, newvalues)

    data = await crud_operation_collection.find_one({"_id":ObjectId(id)})

    return CrudOperationResponse(id=str(data["_id"]), operationName=data["operationName"],operationCreateTime=data["operation_create_time"], operationLastUpdateTime = data["operation_last_update_time"])