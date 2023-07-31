from config import database

class DataQuery:

    async def get_admin(self, query_parameter :dict  = None):
        if query_parameter :
            return await database.admin_collection.find_one(query_parameter) 
        
    
