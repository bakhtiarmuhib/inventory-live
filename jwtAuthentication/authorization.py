
import typing
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info
from fastapi import Depends


from  jwtAuthentication.jwtOuth2 import verify_jwt,dencrypt_data,decodeJWT

class IsAdminAuthenticated(BasePermission):
    message = "User is not authenticated"
   
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization")
            token_devided = authorization.split(" ")
            if token_devided [0] != "Bearer":
                raise Exception("Invalid authentication scheme.")
            if not verify_jwt(token_devided[1]):
                raise Exception("Invalid token or expired token.")
            
            payload = decodeJWT(str(token_devided[1]))
            user_data = dencrypt_data(payload['data'])
            user_data_devided = user_data.split(",")
            if user_data_devided[1] == "admin":
                
                return True
            else:
                return False
        
        return False
    
    
    
    


class IsOrganizationAuthenticated(BasePermission):
    message = "User is not authenticated"
   
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        
        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization")
            token_devided = authorization.split(" ")
            if token_devided [0] != "Bearer":
                raise Exception("Invalid authentication scheme.")
            if not verify_jwt(token_devided[1]):
                raise Exception("Invalid token or expired token.")
            
            payload = decodeJWT(str(token_devided[1]))
            user_data = dencrypt_data(payload['data'])
            user_data_devided = user_data.split(",")
            
            if user_data_devided[1] == "organization":
                return True
            else:
                return False
        
        return False
    

    


class IsUserAuthenticated(BasePermission):
    message = "User is not authenticated"
   
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        
        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization")
            token_devided = authorization.split(" ")
            if token_devided [0] != "Bearer":
                raise Exception("Invalid authentication scheme.")
            if not verify_jwt(token_devided[1]):
                raise Exception("Invalid token or expired token.")
            
            payload = decodeJWT(str(token_devided[1]))
            user_data = dencrypt_data(payload['data'])
            user_data_devided = user_data.split(",")
            if user_data_devided[1] == "user":
                return True
            else:
                return False
        
        return False
    


class IsUserOrOrganizationAuthenticated(BasePermission):
    message = "User is not authenticated"
   
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]
        
        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization")
            token_devided = authorization.split(" ")
            if token_devided [0] != "Bearer":
                raise Exception("Invalid authentication scheme.")
            if not verify_jwt(token_devided[1]):
                raise Exception("Invalid token or expired token.")
            
            payload = decodeJWT(str(token_devided[1]))
            user_data = dencrypt_data(payload['data'])
            user_data_devided = user_data.split(",")
            if user_data_devided[1] == "user" or user_data_devided[1] == "organization":
                return True
            else:
                return False
        
        return False
