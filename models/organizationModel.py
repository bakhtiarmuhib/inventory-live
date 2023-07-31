import strawberry
from typing import Optional,List



# organization models
@strawberry.input
class OrganizationInput:
    email: str 
    password : str
    organizationName: str
    phoneNumber : str


@strawberry.input
class OrganizationUpdateInput:
    organization_name: str
    phone_number : str
    alternative_phone_number: Optional[str] = None
    
    organization_address : Optional[str] = None 
    trade_license_number: Optional[str] = None 
   


# user role models
@strawberry.input
class UserRoleCreateInput:
    roleName: str
    

# user role feature permission models
@strawberry.input
class UserRoleFeaturePermissionCreateInput:
    featurePermissionName: str
    

# user role feature permission update
@strawberry.input
class UserRoleFeaturePermissionUpdate:
    featurePermissionName : str
    featureId: str
    roleId : str
    crudOperation : List[str]


# organization change password
@strawberry.input
class OrganizationPasswordChangeInput:
    password: str
    newPassword : str
    retypePassword : str


@strawberry.type
class UserRoleFeaturePermissionResponse:
    id : str
    featurePermissionName : str
    userRole : str
    organization : str
    featureId : str
    crudOperationPermission : List[str]
    featurePermissionCreateTime : str
    featurePermissionLastUpdateTime : Optional[str]



@strawberry.type
class UserRoleResponse:
    id: str
    roleName: str
    organizationId: str
    roleCreateTime : str
    roleLastUpdateTime :  Optional[str] 



@strawberry.type
class OrganizationGetResponse:
    id: str
    email: str
    organizationName: str
    status : str
    phoneNumber: str
    alternativePhoneNumber: Optional[str] 
    organizationLogo: Optional[str] 
    organizationAddress : Optional[str] 
    tradeLicenseNumber: Optional[str] 
    tradeLcenseImage : Optional[str] 
    createTime : str
    lastUpdateTime : Optional[str] 


