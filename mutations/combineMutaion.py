from mutations.admin import adminAuth,crudOperationOperatonPermission, organizationModulePermission
from mutations.organization import organizationAuth, userRole, userRoleFeaturePermission
from mutations.user import userAuth
from features import features1,features2,features3
from fileUpload import imageUpload


mutations = [
    adminAuth.adminSingin,
    adminAuth.adminRegister,
    adminAuth.adminChangePassword,

    organizationAuth.organizationSingin,
    organizationAuth.organizationRegister,
    organizationAuth.organizationUpdate,
    organizationAuth.organizationChangePassword,
    organizationAuth.fileUpload,

    crudOperationOperatonPermission.CreateCrudOperation,
    crudOperationOperatonPermission.updateCrudOperation,

    userRole.CreateUserRole,
    userRole.updateUserRole,

    userAuth.userSingin,
    userAuth.userRegister,
    userAuth.userUpdate,
    userAuth.userChangePassword,

    userRoleFeaturePermission.CreateUserRoleFeaturesPermission,
    # userRoleFeaturePermission.updateUserRoleFeaturePermission,


    organizationModulePermission.createOrganizationModulePermission,
    imageUpload.organizationLogoUpload,
    imageUpload.organizationTradeLicenseImageUpload,
    imageUpload.userNidImageUpload,
    imageUpload.userProfileImageUpload,



    features1.feature1create,
    features1.feature1update,
    features1.feature1delete,

    features2.feature2create,
    features2.feature2update,
    features2.feature2delete,

    features3.feature3create,
    features3.feature3update,
    features3.feature3delete,

]