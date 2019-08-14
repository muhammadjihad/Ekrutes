from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from akun.models import(
    getUser,
    AccountProfile,
    Kecamatan,
    Kota
)
from superadmin.models import TokenDefault
from django.db.models import Q, F
from django.db.models.functions import Lower
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from .pagination import ResultLimitOffsetPagination
from django.core.paginator import Paginator
from datetime import date

class SuperAdminDashboardAPIView(ListModelMixin,GenericAPIView,APIView):

    def post(self,request):
        print(self.request.data)
        orderParam='id'
        tanggal_registrasi=self.request.data['tanggalRegistrasi'].split(' ')
        tanggal_mulai=tanggal_registrasi[0].replace('/','-')
        tanggal_akhir=tanggal_registrasi[2].replace('/','-')
        tanggal_mulai=date(
            year=int(tanggal_mulai[6:10]),
            month=int(tanggal_mulai[4:6]) if not tanggal_mulai[5] == '-' else int(tanggal_mulai[4]),
            day=int(tanggal_mulai[:2])
        )
        tanggal_akhir=date(
            year=int(tanggal_akhir[6:10]),
            month=int(tanggal_akhir[4:6]) if not tanggal_akhir[5] == '-' else int(tanggal_akhir[4]),
            day=int(tanggal_akhir[:2])
        )
        print(self.request.data['start'])
        # Ini karena plugin DataTables secara default tidak melempar query parameter order[0][dir]
        try:
            urutan=self.request.data['order[0][dir]']
        except:
            urutan='asc'

        # Ini dikarenakan plugin DataTables secara default tidak melempar query parameter order[0][column] 
        try:
            if self.request.data['order[0][column]'] == '0':
                orderParam='user__id'
            elif self.request.data['order[0][column]'] == '1':
                orderParam='user__username'
            elif self.request.data['order[0][column]'] == '2':
                orderParam='user__email'
            elif self.request.data['order[0][column]'] == '3':
                orderParam='namaPerusahaan'
            elif self.request.data['order[0][column]'] == '4':
                orderParam='user__is_active'
            elif self.request.data['order[0][column]'] == '5':
                orderParam='jenisAkun'
            elif self.request.data['order[0][column]'] == '6':
                orderParam='tokenTest'
            elif self.request.data['order[0][column]'] == '7':
                orderParam='tanggalRegistrasi'
        except:
            pass

        # Dapatkan model user dengan sessionId yang dikirim
        user=getUser(session_key=self.request.data['sessionId'])
        print(user)

        # Pastikan bahwa user adalah super User
        if user.is_superuser:

            # Cek apakah query parameter dengan statusAkun ada atau tidak
            # Parameter ini tidak bisa di bypass dengan '' karena typenya harus True atau False
            if not self.request.data['statusAkun'] == None:

                # Lihat parameter tabel yang terubah dari plugin DataTable, apakah tabel yang diubah
                # merupakan salah satu dari tuple di bawah ini ?
                # Jika bukan, maka diperlukan sinkronisasi dengan cara membuat lowercase pada string
                jenisAkun=[int(self.request.data["jenisAkun"]),] if int(self.request.data['jenisAkun']) in [0,1] else [0,1]
                if orderParam not in ('user__id','user__is_active','jenisAkun','tokenTest','tanggalRegistrasi'):
                    if self.request.data['length'] == '-1':
                        dirParam=Lower(orderParam).desc() if urutan == 'desc' else Lower(orderParam)
                        companies=AccountProfile.objects.filter(
                            Q(user__username__icontains=self.request.data['username']) &
                            Q(user__email__icontains=self.request.data['email']) &
                            Q(namaPerusahaan__icontains=self.request.data['namaPerusahaan'])&
                            Q(tanggalRegistrasi__range=[str(tanggal_mulai),str(tanggal_akhir)]) &
                            Q(flag=True)
                        ).order_by(
                                dirParam
                            ).values(
                            'user__id',
                            'user__username',
                            'user__email',
                            'namaPerusahaan',
                            'user__is_active',
                            'jenisAkun',
                            'tokenTest',
                            'noKontak',
                            'tanggalRegistrasi')

                        return Response({
                            'draw':int(self.request.data['draw']),
                            'recordsTotal':len(companies),
                            'recordsFiltered':AccountProfile.objects.all().count(),
                            'data':companies
                        })
                    else:
                        dirParam=Lower(orderParam).desc() if urutan == 'desc' else Lower(orderParam)
                        companies=AccountProfile.objects.filter(
                            Q(user__username__icontains=self.request.data['username']) &
                            Q(user__email__icontains=self.request.data['email']) &
                            Q(namaPerusahaan__icontains=self.request.data['namaPerusahaan'])&
                            Q(tanggalRegistrasi__range=[str(tanggal_mulai),str(tanggal_akhir)]) &
                            Q(flag=True)
                        ).order_by(
                                dirParam
                            ).values(
                            'user__id',
                            'user__username',
                            'user__email',
                            'namaPerusahaan',
                            'user__is_active',
                            'jenisAkun',
                            'tokenTest',
                            'noKontak',
                            'tanggalRegistrasi')[int(self.request.data['start']):int(self.request.data['start'])+int(self.request.data['length'])]

                        return Response({
                            'draw':int(self.request.data['draw']),
                            'recordsTotal':len(companies),
                            'recordsFiltered':AccountProfile.objects.all().count(),
                            'data':companies
                        })
   
                    
                # Jika tabel yang diubah merupakan salah satu dari tuple di atas, maka
                # tidak diperlukan sinkronisasi lower case, karena sifatnya bisa langsung dikomparasi
                # seperti Boolean atau Integer
                else:
                    if self.request.data['length'] == '-1':
                        dirParam='-' if not urutan == 'desc' else ''
                        jenisAkun=[int(self.request.data["jenisAkun"]),] if int(self.request.data['jenisAkun']) in [0,1] else [0,1]
                        statusAkun=[bool(int(self.request.data["statusAkun"])),] if int(self.request.data['statusAkun']) in [0,1] else [True,False]
                        print(statusAkun)
                        all_companies=AccountProfile.objects.filter(
                            Q(user__username__icontains=self.request.data['username']) &
                            Q(user__email__icontains=self.request.data['email']) &
                            Q(namaPerusahaan__icontains=self.request.data['namaPerusahaan'])&
                            Q(tanggalRegistrasi__range=[str(tanggal_mulai),str(tanggal_akhir)]) &
                            Q(jenisAkun__in=jenisAkun) &
                            Q(user__is_active__in=statusAkun) &
                            Q(flag=True)
                        ).order_by(
                                '{}{}'.format(dirParam,orderParam)
                            ).values(
                            'user__id',
                            'user__username',
                            'user__email',
                            'namaPerusahaan',
                            'user__is_active',
                            'jenisAkun',
                            'tokenTest',
                            'noKontak',
                            'tanggalRegistrasi')
                        paging_companies=all_companies
                        return Response({
                            'draw':int(self.request.data['draw']),
                            'recordsTotal':paging_companies.count(),
                            'recordsFiltered':len(all_companies),
                            'data':paging_companies
                        })
                    else:
                        dirParam='-' if not urutan == 'desc' else ''
                        jenisAkun=[int(self.request.data["jenisAkun"]),] if int(self.request.data['jenisAkun']) in [0,1] else [0,1]
                        statusAkun=[bool(int(self.request.data["statusAkun"])),] if int(self.request.data['statusAkun']) in [0,1] else [True,False]
                        print(statusAkun)
                        all_companies=AccountProfile.objects.filter(
                            Q(user__username__icontains=self.request.data['username']) &
                            Q(user__email__icontains=self.request.data['email']) &
                            Q(namaPerusahaan__icontains=self.request.data['namaPerusahaan'])&
                            Q(tanggalRegistrasi__range=[str(tanggal_mulai),str(tanggal_akhir)]) &
                            Q(jenisAkun__in=jenisAkun) &
                            Q(user__is_active__in=statusAkun) &
                            Q(flag=True)
                        ).order_by(
                                '{}{}'.format(dirParam,orderParam)
                            ).values(
                            'user__id',
                            'user__username',
                            'user__email',
                            'namaPerusahaan',
                            'user__is_active',
                            'jenisAkun',
                            'tokenTest',
                            'noKontak',
                            'tanggalRegistrasi')
                        paging_companies=all_companies[int(self.request.data['start']):int(self.request.data['start'])+int(self.request.data['length'])]
                        return Response({
                            'draw':int(self.request.data['draw']),
                            'recordsTotal':paging_companies.count(),
                            'recordsFiltered':len(all_companies),
                            'data':paging_companies
                        })

            # Jika client mengirimkan parameter user__is_active
            else:
                companies=AccountProfile.objects.filter(
                    Q(user__username__icontains=self.request.data['username']) &
                    Q(user__email__icontains=self.request.data['email']) &
                    Q(user__is_active__icontains=self.request.data['isActive']) &
                    Q(namaPerusahaan__icontains=self.request.data['namaPerusahaan']) &
                    Q(noKontak__icontains=self.request.data['noKontak']) &
                    Q(flag=True)
                ).values('namaPerusahaan','noKontak','user__username','user__email','user__id','user__is_active').order_by('-id')
                return Response({
                    'status':1,
                    'data':companies
                })

        # Jika user yang melakukan login bukanlah super user
        else:
            return Response({
                'status':0,
                'message':'Kamu bukan SuperAdmin',
                'data':[]
            })

class TokenDefaultAPIView(APIView):

    def post(self,request,*args,**kwargs):
        user=getUser(session_key=self.request.data['sessionId'])
        if user is not None:
            token=self.request.data['token']
            if token == '':
                TokenDefault.objects.create(
                    tokenDefault=0
                )
            else:
                TokenDefault.objects.create(
                    tokenDefault=int(token)
                )
            return Response({
                'pesan':int(token)
            })
        else:
            return Response({
                'pesan':'User tidak valid'
            })

class PerusahaanDetailAPIView(APIView):

    def get(self,request,*args,**kwargs):
        user=getUser(session_key=self.request.query_params['sessionId'])
        profile=AccountProfile.objects.select_related('user','idKecamatan').get(user__id=int(self.request.query_params['id']))
        if user is not None:
            if profile.idKecamatan is not None:
                kota=Kota.objects.get(id_kota=profile.idKecamatan.f_id_kota)
                return Response({
                    'status':1,
                    'message':'Data berhasil ditemukan',
                    'data':{
                        'nama':profile.user.username,
                        'namaPerusahaan':profile.namaPerusahaan,
                        'kontak':profile.noKontak,
                        'email':profile.user.email,
                        'alamat':profile.alamatPerusahaan,
                        'foto':profile.foto.url,
                        'kecamatan':profile.idKecamatan.id_kecamatan,
                        'kota':kota.id_kota,
                        'provinsi':kota.f_id_prov,
                        'npwp':profile.npwp,
                        'deskripsi':profile.deskripsi,
                        'tanggalRegistrasi':profile.tanggalRegistrasi,
                        'statusAkun':profile.user.is_active,
                        'jenisAkun':profile.jenisAkun,
                        'tokenTest':profile.tokenTest
                    }
                })
            else:
                return Response({
                    'status':1,
                    'message':'Data berhasil ditemukan',
                    'data':{
                        'nama':profile.user.username,
                        'namaPerusahaan':profile.namaPerusahaan,
                        'kontak':profile.noKontak,
                        'email':profile.user.email,
                        'alamat':profile.alamatPerusahaan,
                        'foto':profile.foto.url,
                        'npwp':profile.npwp,
                        'deskripsi':profile.deskripsi,
                        'tanggalRegistrasi':profile.tanggalRegistrasi,
                        'statusAkun':profile.user.is_active,
                        'jenisAkun':profile.jenisAkun,
                        'tokenTest':profile.tokenTest,
                    }
                })
        else:
            return Response({
                'status':0,
                'message':'Pastikan sudah login',
                'data':'Tidak ditemukan'
            })

class DeleteHRAPIView(APIView):

    def delete(self,request,*args,**kwargs):
        user=AccountProfile.objects.get(id=self.request.data['id'])
        user.flag=False
        user.user.is_active=False
        user.user.save()
        user.save()
        return Response({
            'status':1,
            'message':'',
        })

class UpdateHRAPIView(APIView):

    def put(self,request,*args,**kwargs):
        idUser=self.request.data['edit_id']
        user=AccountProfile.objects.filter(user__id=int(idUser))
        if self.request.data['edit_kecamatan'] == '0':
                user.update(
                person=self.request.data['edit_person'],
                namaPerusahaan=self.request.data['edit_namaPerusahaan'],
                noKontak=self.request.data['edit_contact'],
                # user__user.email=self.request.data['edit_email'],
                npwp=self.request.data['edit_npwp'],
                idKecamatan=None,
                alamatPerusahaan=self.request.data['edit_alamat'],
                deskripsi=self.request.data['edit_deskripsi'],
                tokenTest=int(self.request.data['edit_token'])
            )
        else:
            user.update(
                person=self.request.data['edit_person'],
                namaPerusahaan=self.request.data['edit_namaPerusahaan'],
                noKontak=self.request.data['edit_contact'],
                # user__user.email=self.request.data['edit_email'],
                npwp=self.request.data['edit_npwp'],
                idKecamatan=int(self.request.data['edit_kecamatan']),
                alamatPerusahaan=self.request.data['edit_alamat'],
                deskripsi=self.request.data['edit_deskripsi'],
                tokenTest=int(self.request.data['edit_token'].replace(".",""))
            )
        return Response({
            'status':1,
            'message':'berhasil'
        })

class UploadPhoto(APIView):

    def post(self,request,*args,**kwargs):
        idUser=self.request.data['id']
        user=AccountProfile.objects.get(id=int(idUser))
        user.foto=self.request.data['qqfile']
        user.save()
        return Response(
            {'success':1,
            'message':''
            }
        )

    def delete(self,request,*args,**kwargs):
        idUser=self.request.data['id']
        user=AccountProfile.objects.get(user__id=int(idUser))
        user.foto="company-profile-picture/default.png"
        user.save()
        print("DELETE MASUK")
        return Response(
            {'success':1,
            'message':''
            }
        )