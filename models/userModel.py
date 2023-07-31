import strawberry
from typing import Optional


@strawberry.input
class UserCreateInput:
    email: str 
    password : str
    firstName: str
    lastName: str
    phoneNumber : str
    presentAddress : str


@strawberry.input
class UserUpdateInput:
    firstName : str
    lastName : str
    phoneNumber: str
    alternativePhoneNumber : Optional[str] = None
    presentAddress : str
    permanentAddress : Optional[str] = None
    nidNumber: Optional[str] = None
    

@strawberry.type
class GetUserResponse:
    id: str
    email: str
    firstName : str
    lastName : str
    organizationId: str
    status : str
    userRole : str
    phoneNumber: str
    alternativePhoneNumber : Optional[str] 
    presentAddress : str
    permanentAddress : Optional[str] 
    nidNumber: Optional[str] 
    nidImage : Optional[str] 
    createTime : str
    lastUpdateTime : Optional[str] 
    profileImage : Optional[str] 


# admin change password
@strawberry.input
class UserPasswordChangeInput:
    password: str
    newPassword : str
    retypePassword : str

