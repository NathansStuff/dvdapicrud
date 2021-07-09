from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import os

# Runs shell script from website
class MyView(ListAPIView):
    @csrf_exempt
    def post(self,request):
        message = self.request.POST.get('message','')
        os.system('python cout.py '+message)
        return Response(
            {
                "Status":True
            }
        )
