import strawberry
from typing import Optional
from config.database import user_role_features_permission_collection
from models.organizationModel import UserRoleFeaturePermissionResponse

from bson import ObjectId
from typing import List
from strawberry.types import Info

from jwtAuthentication.authorization import IsOrganizationAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data


    


@strawberry.field(permission_classes=[IsOrganizationAuthenticated])
async def getUerRoleFeaturePermission(info:Info, id : Optional[str] = None) -> List[UserRoleFeaturePermissionResponse]:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")
    
    if id != None:
        data = await user_role_features_permission_collection.find_one({"_id":ObjectId(id), "organization_id" : dencrypt_data_in_list[0]})
        if data:
            return [UserRoleFeaturePermissionResponse(id=str(data["_id"]), featurePermissionName=data["feature_permission_name"],userRole=data["user_role"],organization=data["organization"],crudOperationPermission=data["crud_operation_permission"], featureId=data["feature_id"], featurePermissionCreateTime = data["feature_permission_create_time"],featurePermissionLastUpdateTime=data["feature_permission_last_update_time"])]
        else:
            raise Exception("No feature permission found in this id.")
    else:
        data = [UserRoleFeaturePermissionResponse(id=str(data["_id"]), featurePermissionName=data["feature_permission_name"],userRole=data["user_role"],organization=data["organization"],crudOperationPermission=data["crud_operation_permission"], featureId=data["feature_id"], featurePermissionCreateTime = data["feature_permission_create_time"],featurePermissionLastUpdateTime=data["feature_permission_last_update_time"]) async for data in user_role_features_permission_collection.find({"organization_id" : dencrypt_data_in_list[0]})]
        if data:
            return data
        else:
            raise Exception("No feature permission found.")
        

