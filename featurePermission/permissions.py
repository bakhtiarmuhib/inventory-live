from typing import List
from config.database import organization_module_permission_collection, feature_collection, user_role_features_permission_collection,user_collection, crud_operation_collection
from bson import ObjectId


class UserPermission:
    def __init__(self, feature: dict, user: str):
        self.feature = feature
        self.user = user
    async def organizationPermission(self):
        splite_into_id_and_user_type = self.user.split(",")
        if splite_into_id_and_user_type[1] == "organization":
            all_module = []
            async for module1 in organization_module_permission_collection.find({"organization_id" : splite_into_id_and_user_type[0]}) :
                all_module.append(module1["module_id"])
            if not all_module:
                raise   Exception("No feature permission found.")
            find_feature = await feature_collection.find_one({"feature_name" : self.feature["name"]})
            
            if not find_feature:
                raise   Exception("No feature found.")
            
            if  find_feature["module_id"] in all_module:
                return  True
            raise Exception("permission not found")
        else:
            return False
        
    async def userPermission(self):
        splite_into_id_and_user_type = self.user.split(",")
        if splite_into_id_and_user_type[1] == "user":
            
            find_feature = await feature_collection.find_one({"feature_name" : self.feature["name"]})
            if not find_feature:
                raise Exception("No feature found")
            find_user = await user_collection.find_one({"_id" : ObjectId(splite_into_id_and_user_type[0])})
            find_operation = await crud_operation_collection.find_one({"operationName" : self.feature["operation"]})
            find_feature_permission = await user_role_features_permission_collection.find_one({"feature_id" : str(find_feature["_id"]), "user_role" : find_user["user_role"], "organization" : find_user["organization_id"], "crud_operation_permission" :  str(find_operation['_id']) })
            if not find_feature_permission:
                raise Exception("User is not selected for this role")
            else:
                return True
            
        else:
            raise Exception("User is not selected for this role")

