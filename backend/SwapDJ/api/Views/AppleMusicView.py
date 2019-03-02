from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from SwapDJ.api.Services import AppleService

@api_view(['GET'])
def CreateAppToken(request):
    dev_token = AppleService.CreateAppToken()
    dev_token = dev_token.decode('utf-8')

    response = Response()
    if('appleDevToken' not in request.session):
        request.session['appleDevToken'] = dev_token
        response.status_code = 201
        response.data = dev_token
    else:
        response.status_code = 200
        response.data = request.session['appleDevToken']

    return response

@api_view(['POST'])
def Callback(request):
    apple_music_user_token = request.data['appleToken']
    
    response = Response()

    if('appleToken' not in request.session):
        request.session['appleToken'] = apple_music_user_token
        response.status_code = 201
    else:
        response.status_code = 200

    return response

@api_view(['GET'])
def GetUserPlaylists(request):
    apple_user_token = request.session['appleToken']
    apple_dev_token = request.session['appleDevToken']

    data = AppleService.GetUserPlaylists(apple_dev_token, apple_user_token)

    response = Response(status=200, data=data)

    return response

@api_view(['GET'])
def Authorized(request):
    if 'appleToken' in request.session:
        appleUserToken = request.session['appleToken']
        appleDevToken = request.session['appleDevToken']

        isAppleAuthorized = AppleService.IsAuthorized(appToken=appleDevToken, userToken=appleUserToken)

        if 'data' in isAppleAuthorized:
            return Response(status=200)

    return Response(status=401)
