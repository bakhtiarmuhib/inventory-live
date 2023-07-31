import strawberry
from typing import Optional
from config.database import user_role_collection
from models.organizationModel import UserRoleResponse

from bson import ObjectId
from typing import List
from strawberry.types import Info

from jwtAuthentication.authorization import IsOrganizationAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data


    


@strawberry.field(permission_classes=[IsOrganizationAuthenticated])
async def getUerRole(info:Info, id : Optional[str] = None) -> List[UserRoleResponse]:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")
    
    if id != None:
        data = await user_role_collection.find_one({"_id":ObjectId(id), "organization_id" : dencrypt_data_in_list[0]})
        if data:
            return [UserRoleResponse(id=str(data["_id"]), roleName=data["roleName"],organizationId=data["organization_id"],roleCreateTime=data["role_create_time"],roleLastUpdateTime=data["role_last_update_time"])]
        else:
            raise Exception("No user role found in this id.")
    else:
        data = [UserRoleResponse(id=str(data["_id"]), roleName=data["roleName"],organizationId=data["organization_id"],roleCreateTime=data["role_create_time"],roleLastUpdateTime=data["role_last_update_time"]) async for data in user_role_collection.find({"organization_id" : dencrypt_data_in_list[0]})]
        if data:
            return data
        else:
            raise Exception("No user role found in database")
        
