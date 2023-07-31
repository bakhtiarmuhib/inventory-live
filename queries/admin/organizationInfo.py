import strawberry
from typing import Optional
from config.database import organization_collection
from models.organizationModel import OrganizationGetResponse
from strawberry.scalars import JSON
from bson import ObjectId
from typing import List


from jwtAuthentication.authorization import IsAdminAuthenticated



@strawberry.field(permission_classes=[IsAdminAuthenticated])
async def getOrganization(id : Optional[str] = None) -> List[OrganizationGetResponse]:
    
    if id != None:
        data = await organization_collection.find_one({"_id":ObjectId(id)})
        if data:
            return [OrganizationGetResponse(id=str(data["_id"]), email=data["email"],status=data["status"], organizationName = data["organization_name"], phoneNumber=data["phone_number"], alternativePhoneNumber=data["alternative_phone_number"], organizationLogo = data["organization_logo"], organizationAddress = data["organization_address"], tradeLicenseNumber=data["trade_license_number"], tradeLcenseImage=data["trade_lcense_image"], createTime = data["create_time"], lastUpdateTime = data['last_update_time'])]
        else:
            raise Exception("No organization found in this id.")
    else:
        data = [OrganizationGetResponse(id=str(data["_id"]), email=data["email"],status=data["status"], organizationName = data["organization_name"], phoneNumber=data["phone_number"], alternativePhoneNumber=data["alternative_phone_number"], organizationLogo = data["organization_logo"], organizationAddress = data["organization_address"], tradeLicenseNumber=data["trade_license_number"], tradeLcenseImage=data["trade_lcense_image"], createTime = data["create_time"], lastUpdateTime = data['last_update_time']) async for data in organization_collection.find()]
        if data:
            return data
        else:
            raise Exception("No organization found in database")
        