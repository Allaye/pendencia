import jwt
from django.conf import settings
from rest_framework.authentication import (get_authorization_header, BaseAuthentication)
from rest_framework import exceptions
from authentication.models import User

class JwtAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        '''
        implementation of custome authenication method to authenticate users token
        '''
        # get the authroization header from the request
        auth_header = get_authorization_header(request)

        # decode the auth_header and get the token by spliting it
        auth_data = auth_header.decode('utf-8')
        auth_data = auth_data.split(' ')

        # check if the splited data contains a potencial token or not
        if len(auth_data) != 2:
            raise exceptions.AuthenticationFailed('Token not valid')
        # get the token which is in the second index after it was splited
        token = auth_data[1]
        
        # decode the jwt token in other to get the user
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            # the the username from the decoded jwt
            username = payload['username']
            user = User.objects.get(username=username)

            return (user, token)


        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token has expired')
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid try loging in again')
        
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('User does not exist, are you sure this account belong to you?')


        return super().authenticate(request)