from fastapi.encoders import jsonable_encoder
from config.database import organization_module_permission_collection
import strawberry
import datetime

from models.adminModel import OrganizationModulePermissionInput, OrganizationModulePermissionRespone
from jwtAuthentication.authorization import IsAdminAuthenticated




#Organization module permission
@strawberry.mutation(permission_classes=[IsAdminAuthenticated])
async def createOrganizationModulePermission(organizationId : str, moduleId : str , data : OrganizationModulePermissionInput) -> OrganizationModulePermissionRespone:
    
    find_exist_data = await organization_module_permission_collection.find_one( { "$or": [ { "modulePermissionName": data.modulePermissionName },  { "module_id": moduleId , "organization_id": organizationId }] })
    if find_exist_data != None:
        if data.modulePermissionName == find_exist_data["modulePermissionName"]:
            raise Exception("Operation name already exist in database.")
        if moduleId == find_exist_data["module_id"] and organizationId == find_exist_data["organization_id"] :
            raise Exception("Module permission already exist for this organization.")
    new_organization_module_permission_data = jsonable_encoder(
        {
        "modulePermissionName": data.modulePermissionName,
        "status" : True,
        "module_id" : moduleId,
        "organization_id" : organizationId,
        "module_permission_create_time" : datetime.datetime.now(),
        "module_permission_last_update_time" : None
        })
    new_organization_module_permission = await organization_module_permission_collection.insert_one(new_organization_module_permission_data)
    data = await organization_module_permission_collection.find_one({"_id": new_organization_module_permission.inserted_id})
    
    return OrganizationModulePermissionRespone(id=str(data["_id"]), modulePermissionName=data["modulePermissionName"],status=data["status"], moduleId = data["module_id"], organizationId = data["organization_id"], modulePermissionCreateTime = data["module_permission_create_time"], modulePermissionLastUpdateTime = data["module_permission_last_update_time"])

