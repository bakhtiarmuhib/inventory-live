from fastapi.encoders import jsonable_encoder
from config.database import user_role_collection
from strawberry.scalars import JSON
from strawberry.types import Info
from bson.objectid import ObjectId
import strawberry
import datetime

from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data
from models.organizationModel import UserRoleCreateInput,UserRoleResponse
from jwtAuthentication.authorization import IsOrganizationAuthenticated




#Create User Role
@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def CreateUserRole(data : UserRoleCreateInput, info:Info) -> UserRoleResponse:
    
    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    new_role_data = jsonable_encoder(
        {
        "roleName": data.roleName,
        "organization_id": dencrypt_user_data_in_list[0],
        "status" : "active",
        "role_create_time" : datetime.datetime.now(),
        "role_last_update_time" : None
        })
    exist_role = await user_role_collection.find_one({"roleName":data.roleName,"organization_id" : dencrypt_user_data_in_list[0]})
    if exist_role:
        raise Exception("role already exist")
    new_role = await user_role_collection.insert_one(new_role_data)
    data = await user_role_collection.find_one({"_id": new_role.inserted_id})
    
    return UserRoleResponse(id=str(data["_id"]), roleName=data["roleName"],organizationId=data["organization_id"],roleCreateTime=data["role_create_time"],roleLastUpdateTime=data["role_last_update_time"])



@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def updateUserRole(id :str, data : UserRoleCreateInput, info:Info) -> UserRoleResponse:
    
    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    new_role_data = jsonable_encoder(
        {
        "roleName": data.roleName,
        "role_last_update_time" : datetime.datetime.now()
        })
    
    
    
    get_role = await user_role_collection.find_one({ "$or": [{ "_id": ObjectId(id),"organization_id" : dencrypt_user_data_in_list[0]}, {"roleName":data.roleName,"organization_id" : dencrypt_user_data_in_list[0]} ]})
    
    if not get_role:
        raise Exception("Role not found in database")
    
    if data.roleName == get_role["roleName"]:
        raise Exception("Role name allready exist.")
    
    newvalues = { "$set": new_role_data}

    await user_role_collection.update_one({ "_id": ObjectId(id),"organization_id" : dencrypt_user_data_in_list[0]}, newvalues)

    data = await user_role_collection.find_one({"_id":ObjectId(id)})

    return UserRoleResponse(id=str(data["_id"]), roleName=data["roleName"],organizationId=data["organization_id"],roleCreateTime=data["role_create_time"],roleLastUpdateTime=data["role_last_update_time"])



# @strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
# async def deleteUserRole(id :str, info:Info) -> JSON:
    
#     user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
#     decoded_user_data = dencrypt_data(user_data['data'])
#     dencrypt_user_data_in_list = decoded_user_data.split(",")

#     get_role = { "_id": ObjectId(id),"organization_id" : dencrypt_user_data_in_list[0]}
#     if not get_role:
#         raise Exception("Role not found in database")
    
#     user_role_collection.(get_role, newvalues)

#     collect_updated_role = await user_role_collection.find_one({"_id":ObjectId(id)})

#     return user_role_create_response(collect_updated_role)