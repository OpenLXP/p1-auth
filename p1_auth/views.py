from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class IsLoggedInView(APIView):
    """Checks if a user is logged in"""

    def get(self, request):
        """
        Validates that a user has a valid sessionid
        """
        # if the user is not found/authenticated (invalid session id)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(request.user.is_authenticated,
                        status=status.HTTP_200_OK)
