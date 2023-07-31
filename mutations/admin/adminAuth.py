import strawberry
from fastapi.encoders import jsonable_encoder
from jwtAuthentication.authorization import IsAdminAuthenticated
from models.adminModel import AdminPasswordChangeInput
from config.databaseQuery import DataQuery
from strawberry.scalars import JSON
from strawberry.types import Info
from bson import ObjectId

from config.database import admin_collection

from jwtAuthentication.jwtOuth2 import verify_password, create_access_token, create_refresh_token, get_hashed_password,encrypt_data
from jwtAuthentication.jwtOuth2 import get_current_user_info, dencrypt_data
from validation.validations import password_validator

find_data = DataQuery()


@strawberry.mutation
async def adminSingin(email:str,password:str) -> JSON:
    admin = await find_data.get_admin({"email":email})
    
    if admin is None:
        raise Exception("Incorrect email")
    if not verify_password(password, admin['password']):
        raise Exception("Incorrect password")
    
    access=create_access_token(encrypt_data(admin['_id'],"admin"))
    refresh = create_refresh_token(encrypt_data(admin['_id'],"admin"))
    return {
        'token_type':'bearer',
        "access_token": access,
        "refresh_token": refresh
    }




@strawberry.mutation
async def adminRegister(email:str,password:str) -> JSON:
    existing_admin = await find_data.get_admin({"email": email})

    if existing_admin:
        raise Exception("Email already registered")

    encrypted_password =get_hashed_password(password)


    new_admin_data = jsonable_encoder({'email': email, 'password' : encrypted_password, 'status': 'active'})
    await admin_collection.insert_one(new_admin_data)
    

    return  {"detail":"user created successfully", 'admin' : "created_admin"}



# admin password change
@strawberry.mutation(permission_classes=[IsAdminAuthenticated])
async def adminChangePassword(data : AdminPasswordChangeInput, info:Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_user_data_in_list = decoded_user_data.split(",")

    # get_user = await admin_collection.find_one()
    get_admin = await find_data.get_admin({"_id" : ObjectId(dencrypt_user_data_in_list[0])})

    if not verify_password(data.password,get_admin["password"]):
        raise Exception("Current password does not match.")
    if verify_password(data.newPassword,get_admin["password"]):
        raise Exception("You have used the old password as the new password.")
    new_password = password_validator(data.newPassword)
    if data.newPassword != data.retypePassword:
        raise Exception("Password does not match")
    
    hashed_password = get_hashed_password(data.newPassword)
    
    find_admin = { "_id": ObjectId(dencrypt_user_data_in_list[0])}
    newvalues = { "$set": {"password" : hashed_password}}

    await admin_collection.update_one(find_admin, newvalues)


    return {
        "message": "password change successful."
    }
