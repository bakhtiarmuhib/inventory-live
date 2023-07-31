from fastapi.encoders import jsonable_encoder
from config.database import user_collection,organization_collection
from strawberry.scalars import JSON
from strawberry.types import Info
from bson.objectid import ObjectId
import strawberry
import datetime

from validation.validations import password_validator,email_check, phone_number_validator
from jwtAuthentication.jwtOuth2 import verify_password, create_access_token, create_refresh_token,get_hashed_password, get_current_user_info,encrypt_data,dencrypt_data
from models.userModel import UserCreateInput, UserUpdateInput, UserPasswordChangeInput, GetUserResponse
from jwtAuthentication.authorization import IsOrganizationAuthenticated, IsUserOrOrganizationAuthenticated,IsUserAuthenticated


# user login
@strawberry.mutation
async def userSingin(email:str,password:str) -> JSON:
    user = await user_collection.find_one({"email":email})
    
    if user is None:
        raise Exception("Incorrect email")
    if not verify_password(password, user['password']):
        raise Exception("Incorrect password")
    
    access=create_access_token(encrypt_data(user['_id'],'user'))
    refresh = create_refresh_token(encrypt_data(user['_id'],'user'))

    return {
        'token_type':'bearer',
        "access_token": access,
        "refresh_token": refresh
    }




# user register
@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def userRegister(userRoleId : str ,data : UserCreateInput, info:Info) -> GetUserResponse:

    fresh_email = email_check(data.email)
    new_password = password_validator(data.password)
    fresh_phone_number = phone_number_validator(data.phoneNumber)
    encrypted_password =get_hashed_password(new_password)

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    existing_organization = await organization_collection.find_one({ "$or" :[{"email": fresh_email},{"phone_number" : fresh_phone_number}]})
    if existing_organization:
        if existing_organization["email"] == fresh_email:
            raise Exception("Email already registered")
        elif existing_organization["phone_number"] == fresh_phone_number:
            raise Exception("Phone number already registered")
   

    
    existing_user = await user_collection.find_one({ "$or" :[{"email": fresh_email},{"phone_number" : fresh_phone_number}]})
    if existing_user:
        if existing_user["email"] == fresh_email:
            raise Exception("Email already registered")
        elif existing_user["phone_number"] == fresh_phone_number:
            raise Exception("Phone number already registered")

    new_user_data = jsonable_encoder(
        {
        "email": data.email,
        "password" : encrypted_password,
        "first_name" : data.firstName,
        "last_name" : data.lastName,
        "status" : "active",
        "organization_id": dencrypt_data_in_list[0],
        "user_role" : userRoleId,
        "phone_number": fresh_phone_number,
        "alternative_phone_number" : None,
        "present_address" : data.presentAddress,
        "permanent_address" :  None ,
        "nid_number": None,
        "nid_image" : None,
        "create_time" : datetime.datetime.now(),
        "last_update_time" : None,
        "profile_image": None
        })

    new_user = await user_collection.insert_one(new_user_data)
    data = await user_collection.find_one({"_id": new_user.inserted_id})
   

    return GetUserResponse(id=str(data["_id"]),email=data["email"],status=data["status"],firstName=data["first_name"],lastName=data["last_name"],organizationId=data["organization_id"],userRole=data["user_role"],phoneNumber= data["phone_number"],alternativePhoneNumber=data["alternative_phone_number"],presentAddress=data["present_address"],permanentAddress=data["permanent_address"],nidNumber=data["nid_number"],nidImage=data["nid_image"],createTime=data["create_time"],lastUpdateTime=data["last_update_time"],profileImage=data["profile_image"])



#user update
@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def userUpdate(data : UserUpdateInput,info:Info) -> JSON:
    
    fresh_phone_number = phone_number_validator(data.phone_number)
    if data.alternativePhoneNumber :
        fresh_alternative_phone_number = phone_number_validator(data.alternativePhoneNumber)
    # all phone number not chacked
    
    existing_phone = await user_collection.find_one({"phone_number": fresh_phone_number})
    if existing_phone:
        raise Exception("Phone number already registered")
    
    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    
    new_user_data = jsonable_encoder(
        {
        "email": data.email,
        "first_name" : data.firstName,
        "last_name" : data.lastName,
        "phone_number": fresh_phone_number,
        "alternative_phone_number" : fresh_alternative_phone_number,
        "present_address" : data.presentAddress,
        "permanent_address" :  data.presentAddress ,
        "nid_number": data.nidNumber,
      
        "last_update_time" : datetime.datetime.now()
        })
    
    get_user = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": new_user_data}

    await user_collection.update_one(get_user, newvalues)

    data = await user_collection.find_one({"_id":ObjectId(dencrypt_data_in_list[0])})

    return GetUserResponse(id=str(data["_id"]),email=data["email"],status=data["status"],firstName=data["first_name"],lastName=data["last_name"],organizationId=data["organization_id"],userRole=data["user_role"],phoneNumber= data["phone_number"],alternativePhoneNumber=data["alternative_phone_number"],presentAddress=data["present_address"],permanentAddress=data["permanent_address"],nidNumber=data["nid_number"],nidImage=data["nid_image"],createTime=data["create_time"],lastUpdateTime=data["last_update_time"],profileImage=data["profile_image"])


@strawberry.mutation(permission_classes=[IsUserAuthenticated])
async def userChangePassword(data : UserPasswordChangeInput, info:Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    get_user = await user_collection.find_one({"_id" : ObjectId(dencrypt_user_data_in_list[0])})

    if not verify_password(data.password,get_user["password"]):
        raise Exception("Current password does not match.")
    if verify_password(data.newPassword,get_user["password"]):
        raise Exception("You have used the old password as the new password.")
    new_password = password_validator(data.newPassword)
    if data.newPassword != data.retypePassword:
        raise Exception("Password does not match")
    
    hashed_password = get_hashed_password(new_password)
    
    find_user = { "_id": ObjectId(dencrypt_user_data_in_list[0])}
    newvalues = { "$set": {"password" : hashed_password}}

    await user_collection.update_one(find_user, newvalues)


    return {
        "message": "password change successful."
    }