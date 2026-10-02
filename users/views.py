from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer


class RegisterUser(APIView):

    def post(self, request):                                       #Since the request is POST,this method executes.

        serializer = UserRegistrationSerializer(data=request.data) #This line simply creates a serializer object and puts the incoming data inside it.

        if serializer.is_valid():                                  #This is where control goes into the serializer again.
            serializer.save()                                       #Now Django automatically calls create() from serilizer.py 
    
            return Response(                                        #Send Response to client
                {
                    "message": "User Registered Successfully"
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)