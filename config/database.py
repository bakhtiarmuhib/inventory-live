import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://inventory:cpl12345@cluster0.mpvarvo.mongodb.net/?retryWrites=true&w=majority")
db = client.inventory_management


admin_collection = db.get_collection("admin")
organization_collection = db.get_collection("organization")
user_collection = db.get_collection("user")
user_role_collection = db.get_collection("user_role")
crud_operation_collection = db.get_collection("crud_operation")
user_role_features_permission_collection = db.get_collection("user_role_features_permission")
feature_collection = db.get_collection("feature")
module_collection = db.get_collection("module")
organization_module_permission_collection = db.get_collection("organization_module_permission")