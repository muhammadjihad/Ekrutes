from rest_framework.response import Response
from rest_framework.views import APIView
from peserta.models import BiodataPeserta

class RegistrasiPesertaAPI(APIView):

    def post(self,request,*args,**kwargs):
        print(self.request.data)
        return Response({
            'status':1,
            'message':'berhasil mengirim biodata'
        })

