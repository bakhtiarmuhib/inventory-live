from fastapi.encoders import jsonable_encoder
from config.database import user_role_features_permission_collection
from strawberry.scalars import JSON
from strawberry.types import Info
from typing import List,Optional
from bson.objectid import ObjectId
import strawberry
import datetime

from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data
from models.organizationModel import UserRoleFeaturePermissionCreateInput,UserRoleFeaturePermissionUpdate, UserRoleFeaturePermissionResponse
from jwtAuthentication.authorization import IsOrganizationAuthenticated




#Create User Role
@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def CreateUserRoleFeaturesPermission(featureId:str, roleId : str, crudOperation : List[str] , data : UserRoleFeaturePermissionCreateInput, info:Info) -> UserRoleFeaturePermissionResponse:
    
    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    new_role_permission_data = jsonable_encoder(
        {
        "feature_permission_name": data.featurePermissionName,
        "user_role": roleId,
        "organization" : dencrypt_user_data_in_list[0],
        "feature_id" : featureId,
        "crud_operation_permission" : crudOperation,
        "feature_permission_create_time" : datetime.datetime.now(),
        "feature_permission_last_update_time" : None
        })
    new_role_permission = await user_role_features_permission_collection.insert_one(new_role_permission_data)
    data = await user_role_features_permission_collection.find_one({"_id": new_role_permission.inserted_id})
    
    return UserRoleFeaturePermissionResponse(id=str(data["_id"]), featurePermissionName=data["feature_permission_name"],userRole=data["user_role"],organization=data["organization"],crudOperationPermission=data["crud_operation_permission"], featureId=data["feature_id"], featurePermissionCreateTime = data["feature_permission_create_time"],featurePermissionLastUpdateTime=data["feature_permission_last_update_time"])



# @strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
# async def updateUserRoleFeaturePermission(info : Info,data = UserRoleFeaturePermissionUpdate) -> JSON:
    
#     user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
#     decoded_user_data = dencrypt_data(user_data['data'])
#     dencrypt_user_data_in_list = decoded_user_data.split(",")

#     new_feature_permission_data = jsonable_encoder(
#         {
#         "feature_permission_name": data.featurePermissionName,
#         "user_role": data.roleId,
#         "feature_id" : data.featureId,
#         "crud_operation_permission" : data.crudOperation
#         })
    
#     get_role_feature_permission = user_role_features_permission_collection.find_one({ "_id": ObjectId(id),"organization" : dencrypt_user_data_in_list[0]})
#     if not get_role_feature_permission:
#         raise Exception("Role permission not found in database")
#     newvalues = { "$set": new_feature_permission_data}

#     await user_role_features_permission_collection.update_one({ "_id": ObjectId(id),"organization" : dencrypt_user_data_in_list[0]}, newvalues)

#     collect_updated_role_permission = await user_role_features_permission_collection.find_one({"_id":ObjectId(id)})

#     return user_role_feature_permission_response(collect_updated_role_permission)
    