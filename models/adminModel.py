import strawberry
from typing import Optional

# crud operation
@strawberry.input
class CrudOperationCreateInput:
    operationName: str
    

@strawberry.type
class CrudOperationResponse:
    id: str
    operationName : str
    operationCreateTime : str
    operationLastUpdateTime : Optional[str]

# organization module permission

@strawberry.input
class OrganizationModulePermissionInput:
    modulePermissionName: str
    

@strawberry.type
class OrganizationModulePermissionRespone:
    id: str
    modulePermissionName: str
    status : str
    moduleId : str
    organizationId : str
    modulePermissionCreateTime : str
    modulePermissionLastUpdateTime : Optional[str]

# admin change password
@strawberry.input
class AdminPasswordChangeInput:
    password: str
    newPassword : str
    retypePassword : str
    

# admin response     
@strawberry.type
class AdminResponse:
    id : str
    email : str
    status : str



