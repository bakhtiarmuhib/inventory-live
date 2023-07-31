from fastapi.encoders import jsonable_encoder
from config.database import organization_collection,user_collection
from strawberry.scalars import JSON
from strawberry.types import Info
from bson.objectid import ObjectId
from strawberry.file_uploads import Upload
from typing import Optional
import strawberry
import datetime

from validation.validations import password_validator,email_check, phone_number_validator
from validation.emailValidation import mail_sender
from jwtAuthentication.jwtOuth2 import verify_password, create_access_token, create_refresh_token,get_hashed_password, get_current_user_info,encrypt_data,decodeJWT,dencrypt_data
from models.organizationModel import OrganizationInput, OrganizationUpdateInput, OrganizationPasswordChangeInput,OrganizationGetResponse
from jwtAuthentication.authorization import IsOrganizationAuthenticated




#organization singin
@strawberry.mutation
async def organizationSingin(email:str,password:str) -> JSON:
    organization = await organization_collection.find_one({"email":email})
    
    if organization is None:
        raise Exception("Incorrect email")
    if not verify_password(password, organization['password']):
        raise Exception("Incorrect password")
    
    access=create_access_token(encrypt_data(organization['_id'],"organization"))
    refresh = create_refresh_token(encrypt_data(organization['_id'],"organization"))

    return {
        'token_type':'bearer',
        "access_token": access,
        "refresh_token": refresh
    }


#organization register
@strawberry.mutation()
async def organizationRegister(data : OrganizationInput) -> OrganizationGetResponse:
    fresh_email = email_check(data.email)
    new_password = password_validator(data.password)
    fresh_phone_number = phone_number_validator(data.phoneNumber)
    encrypted_password =get_hashed_password(new_password)

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

    new_admin_data = jsonable_encoder(
        {
        'email': fresh_email,
        'password' : encrypted_password,
        'organization_name':data.organizationName,
        'status': 'active',
        'phone_number': fresh_phone_number,
        'alternative_phone_number': None,
        'organization_logo': None,
        'organization_address': None,
        'trade_license_number':None,
        'trade_lcense_image':None,
        "create_time": datetime.datetime.now(),
        'last_update_time':None

        })
    try:
        await mail_sender(fresh_email)
    except:
        raise Exception("Something is wrong")
    new_admin = await organization_collection.insert_one(new_admin_data)
    data = await organization_collection.find_one({"_id": new_admin.inserted_id})
    

    return OrganizationGetResponse(id=str(data["_id"]), email=data["email"],status=data["status"], organizationName = data["organization_name"], phoneNumber=data["phone_number"], alternativePhoneNumber=data["alternative_phone_number"], organizationLogo = data["organization_logo"], organizationAddress = data["organization_address"], tradeLicenseNumber=data["trade_license_number"], tradeLcenseImage=data["trade_lcense_image"], createTime = data["create_time"], lastUpdateTime = data['last_update_time'])


#organization update
@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def organizationUpdate(data : OrganizationUpdateInput,info:Info) -> OrganizationGetResponse:

    
    fresh_phone_number = phone_number_validator(data.phone_number)
    # all phone number not chacked
    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")
    existing_phone = await organization_collection.find_one({"phone_number": fresh_phone_number})
    if existing_phone:
        raise Exception("Phone number already registered")

    
    new_organization_data = jsonable_encoder(
        {
        'organization_name': data.organization_name,
        'phone_number': fresh_phone_number,
        'alternative_phone_number': data.alternative_phone_number,
       
        'organization_address': data.organization_address,
        'trade_license_number': data.trade_license_number,
        
        'last_update_time': datetime.datetime.now()
        })
    
    get_organization = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": new_organization_data}

    await organization_collection.update_one(get_organization, newvalues)

    data = await organization_collection.find_one({"_id":ObjectId(dencrypt_data_in_list[0])})

    return OrganizationGetResponse(id=str(data["_id"]), email=data["email"],status=data["status"], organizationName = data["organization_name"], phoneNumber=data["phone_number"], alternativePhoneNumber=data["alternative_phone_number"], organizationLogo = data["organization_logo"], organizationAddress = data["organization_address"], tradeLicenseNumber=data["trade_license_number"], tradeLcenseImage=data["trade_lcense_image"], createTime = data["create_time"], lastUpdateTime = data['last_update_time'])





@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def organizationChangePassword(data : OrganizationPasswordChangeInput, info:Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    get_organization = await organization_collection.find_one({"_id" : ObjectId(dencrypt_user_data_in_list[0])})

    if not verify_password(data.password,get_organization["password"]):
        raise Exception("Current password does not match.")
    if verify_password(data.newPassword,get_organization["password"]):
        raise Exception("You have used the old password as the new password.")
    new_password = password_validator(data.newPassword)
    if data.newPassword != data.retypePassword:
        raise Exception("Password does not match")
    
    hashed_password = get_hashed_password(new_password)
    
    find_organization = { "_id": ObjectId(dencrypt_user_data_in_list[0])}
    newvalues = { "$set": {"password" : hashed_password}}

    await organization_collection.update_one(find_organization, newvalues)


    return {
        "message": "password change successful."
    }





@strawberry.mutation
async def fileUpload(file : Upload) -> JSON:

    print( file)


    return {
        "message": "file upload success"
    }