import strawberry
from jwtAuthentication.authorization import IsUserOrOrganizationAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data
from strawberry.types import Info
from featurePermission.permissions import UserPermission



@strawberry.field(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature1show(info:Info) -> str:
    feature_information = {
        "name" : "feature1",
        "operation" : "view"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    
    return "In featires one show"


@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature1create(info:Info) -> str:

    feature_information = {
        "name" : "feature1",
        "operation" : "create"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    return "In features 1 create"


@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature1update(info:Info) -> str:

    feature_information = {
        "name" : "feature1",
        "operation" : "update"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    return "In features 1 update"


@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature1delete(info:Info) -> str:

    feature_information = {
        "name" : "feature1",
        "operation" : "delete"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    await value.organizationPermission()
    await value.userPermission()
    
    return "In features 1 delete"

