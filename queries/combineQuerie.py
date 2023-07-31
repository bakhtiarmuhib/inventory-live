from queries.admin import organizationInfo,adminInfo,crudOperationInfo,organizationModulePermissionInfo
from queries.organization import organizationProfile,organizationUserInfo,userRoleInfo,userRoleFeaturePermissionInfo
from queries.user import userInfo
from features import  features1, features2, features3

queries = [

    organizationInfo.getOrganization,
    adminInfo.getAdmin,
    crudOperationInfo.getCrudOperation,
    organizationModulePermissionInfo.getOrganizationModulePermission,
    organizationProfile.getOrganizationprofile,
    organizationUserInfo.getUser,
    userRoleInfo.getUerRole,
    userInfo.getUserProfile,
    userRoleFeaturePermissionInfo.getUerRoleFeaturePermission,
    
    features1.feature1show,
    features2.feature2show,
    features3.feature3show
]