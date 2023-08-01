from strawberry.file_uploads import Upload
import strawberry
from strawberry.scalars import JSON
from jwtAuthentication.authorization import IsOrganizationAuthenticated,IsUserAuthenticated
import uuid
import os
from strawberry.types import Info
from bson.objectid import ObjectId



from jwtAuthentication.jwtOuth2 import  get_current_user_info,dencrypt_data
from config.database import organization_collection,user_collection
 
IMAGEDIR = "static/images/"

@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def organizationLogoUpload(file : Upload, info: Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    extension = file.filename.split(".")
    
    if extension[1] not in ['png','jpg',"jpeg"]:
        raise Exception("Image format not supported")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()


     
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    
    
    get_user = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": {"organization_logo" : "inventory-live-8o8d-7c8ubrsv8-bakhtiarmuhib.vercel.app"+IMAGEDIR+"/"+file.filename)}}

    await organization_collection.update_one(get_user, newvalues)

    f.close()



    return {
        "message": "Image upload success"
    }



@strawberry.mutation(permission_classes=[IsOrganizationAuthenticated])
async def organizationTradeLicenseImageUpload(file : Upload, info: Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    extension = file.filename.split(".")
    print(extension)
    if extension[1] not in ['png','jpg',"jpeg"]:
        raise Exception("Image format not supported")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()


    print(type(os.getenv("weblink")))    
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    
    
    get_user = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": {"trade_lcense_image" : "inventory-live-8o8d-7c8ubrsv8-bakhtiarmuhib.vercel.app"+IMAGEDIR+"/"+file.filename)}}

    await organization_collection.update_one(get_user, newvalues)

    f.close()



    return {
        "message": "Image upload success"
    }



@strawberry.mutation(permission_classes=[IsUserAuthenticated])
async def userNidImageUpload(file : Upload, info: Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    extension = file.filename.split(".")
    print(extension)
    if extension[1] not in ['png','jpg',"jpeg"]:
        raise Exception("Image format not supported")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()


    print(type(os.getenv("weblink")))    
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    
    
    get_user = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": {"nid_image" : "inventory-live-8o8d-7c8ubrsv8-bakhtiarmuhib.vercel.app"+IMAGEDIR+"/"+file.filename)}}

    await user_collection.update_one(get_user, newvalues)

    f.close()



    return {
        "message": "Image upload success"
    }



@strawberry.mutation(permission_classes=[IsUserAuthenticated])
async def userProfileImageUpload(file : Upload, info: Info) -> JSON:

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])
    dencrypt_data_in_list = decoded_user_data.split(",")

    extension = file.filename.split(".")
    print(extension)
    if extension[1] not in ['png','jpg',"jpeg"]:
        raise Exception("Image format not supported")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()


    print(type(os.getenv("weblink")))    
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    
    
    get_user = { "_id": ObjectId(dencrypt_data_in_list[0])}
    newvalues = { "$set": {"profile_image" : "inventory-live-8o8d-7c8ubrsv8-bakhtiarmuhib.vercel.app"+IMAGEDIR+"/"+file.filename)}}

    await user_collection.update_one(get_user, newvalues)

    f.close()



    return {
        "message": "Image upload success"
    }
