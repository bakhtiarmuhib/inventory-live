import strawberry
from typing import Optional
from config.database import organization_module_permission_collection
from models.adminModel import OrganizationModulePermissionRespone
from bson import ObjectId
from typing import List


from jwtAuthentication.authorization import IsAdminAuthenticated



@strawberry.field(permission_classes=[IsAdminAuthenticated])
async def getOrganizationModulePermission(id : Optional[str] = None, organizationId : Optional[str] = None) -> List[OrganizationModulePermissionRespone]:
    
    if id != None:
        data = await organization_module_permission_collection.find_one({"_id":ObjectId(id)})
        if data:
            return [OrganizationModulePermissionRespone(id=str(data["_id"]), modulePermissionName=data["modulePermissionName"],status=data["status"], moduleId = data["module_id"], organizationId = data["organization_id"], modulePermissionCreateTime = data["module_permission_create_time"], modulePermissionLastUpdateTime = data["module_permission_last_update_time"])]
        else:
            raise Exception("No module permission found in this id.")
    elif organizationId != None:
        data = [OrganizationModulePermissionRespone(id=str(data["_id"]), modulePermissionName=data["modulePermissionName"],status=data["status"], moduleId = data["module_id"], organizationId = data["organization_id"], modulePermissionCreateTime = data["module_permission_create_time"], modulePermissionLastUpdateTime = data["module_permission_last_update_time"]) async for data in organization_module_permission_collection.find({"organization_id" : organizationId})]
        if data:
            return data
        else:
            raise Exception("No module permission for this organization")
    else:
        data = [OrganizationModulePermissionRespone(id=str(data["_id"]), modulePermissionName=data["modulePermissionName"],status=data["status"], moduleId = data["module_id"], organizationId = data["organization_id"], modulePermissionCreateTime = data["module_permission_create_time"], modulePermissionLastUpdateTime = data["module_permission_last_update_time"]) async for data in organization_module_permission_collection.find()]
        if data:
            return data
        else:
            raise Exception("No module permission found in database")