import strawberry
from config.database import user_collection
from models.userModel import GetUserResponse
from bson import ObjectId
from typing import List
from strawberry.types import Info


from jwtAuthentication.authorization import IsUserAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info, dencrypt_data


@strawberry.field(permission_classes=[IsUserAuthenticated])
async def getUserProfile(info:Info) -> GetUserResponse:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")
    
    data = await user_collection.find_one({"_id":ObjectId(dencrypt_data_in_list[0])})
    if data:
        return GetUserResponse(id=str(data["_id"]),email=data["email"],status=data["status"],firstName=data["first_name"],lastName=data["last_name"],organizationId=data["organization_id"],userRole=data["user_role"],phoneNumber= data["phone_number"],alternativePhoneNumber=data["alternative_phone_number"],presentAddress=data["present_address"],permanentAddress=data["permanent_address"],nidNumber=data["nid_number"],nidImage=data["nid_image"],createTime=data["create_time"],lastUpdateTime=data["last_update_time"],profileImage=data["profile_image"])
    else:
        raise Exception("No organization found in this id.")
    