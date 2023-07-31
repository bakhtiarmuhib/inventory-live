import strawberry
from config.database import organization_collection
from models.organizationModel import OrganizationGetResponse
from bson import ObjectId
from typing import List
from strawberry.types import Info


from jwtAuthentication.authorization import IsOrganizationAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info, dencrypt_data


@strawberry.field(permission_classes=[IsOrganizationAuthenticated])
async def getOrganizationprofile(info:Info) -> OrganizationGetResponse:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")
    
    data = await organization_collection.find_one({"_id":ObjectId(dencrypt_data_in_list[0])})
    if data:
        return OrganizationGetResponse(id=str(data["_id"]), email=data["email"],status=data["status"], organizationName = data["organization_name"], phoneNumber=data["phone_number"], alternativePhoneNumber=data["alternative_phone_number"], organizationLogo = data["organization_logo"], organizationAddress = data["organization_address"], tradeLicenseNumber=data["trade_license_number"], tradeLcenseImage=data["trade_lcense_image"], createTime = data["create_time"], lastUpdateTime = data['last_update_time'])
    else:
        raise Exception("No organization found in this id.")
    
    