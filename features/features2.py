import strawberry
from jwtAuthentication.authorization import IsUserOrOrganizationAuthenticated
from jwtAuthentication.jwtOuth2 import get_current_user_info,dencrypt_data
from strawberry.types import Info
from featurePermission.permissions import UserPermission



@strawberry.field(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature2show(info:Info) -> str:

    feature_information = {
        "name" : "feature2",
        "operation" : "view"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    
    return "In featires two show"
    

@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature2create(info:Info) -> str:

    feature_information = {
        "name" : "feature2",
        "operation" : "create"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    return "In features two create"


@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature2update(info:Info) -> str:

    feature_information = {
        "name" : "feature2",
        "operation" : "update"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    return "In features two update"


@strawberry.mutation(permission_classes=[IsUserOrOrganizationAuthenticated])
async def feature2delete(info:Info) -> str:

    feature_information = {
        "name" : "feature2",
        "operation" : "delete"
    }

    user_data = get_current_user_info(info.context["request"].headers.get("Authorization"))
    decoded_user_data = dencrypt_data(user_data['data'])

    value = UserPermission(feature_information,decoded_user_data)
    print(await value.organizationPermission())
    print(await value.userPermission())
    
    return "In features two delete"
