import datetime, time
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.template import Context
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from psikotes.settings import EMAIL_HOST_USER
from akun.models import (
    AccountProfile,
    AccountLoginAttempt,
    RememberAccount,
    RequestResetPass,
    getUser,
    Kota,
    Kecamatan
)
from .serializers import UserSerializer
from .tokens import account_activation_token



class LoginAPIView(APIView):

    def post(self,request,*args,**kwargs):

        try:
            username = User.objects.get(email=request.data['email']).username
        except:
            return Response({
                'message':'Email tidak terdaftar'
            })
        user=authenticate(
            request=request,
            username=username,
            password=request.data['enkripsi']
        )
        # Login Berhasil
        if user is not None:
            attempts=AccountLoginAttempt.objects.filter(user=user)
            for i in range(0,len(attempts)-1):
                attempts[i].delete()
            profile=AccountProfile.objects.get(user=user)
            expired=0
            if user.is_active:
                try:
                    if int(request.data['keeplogin']) == 1:
                        print("KEEPLOGIN MASUK")
                        expired=86400*30
                except:
                    expired=86400

                self.request.session.set_expiry(expired)
                login(self.request,user)
                session_key=self.request.session.session_key

                try:
                    if int(request.data['keeplogin']) == 1:
                        session_key=self.request.session.session_key
                        lastSession,created=RememberAccount.objects.get_or_create(
                            user=user,
                            lastSession=session_key
                        )
                        if not created:
                            lastSession.lastSession=session_key
                            lastSession.save()
                except:
                    pass

            else:
                if profile.flag == False:
                    return Response({
                        'status':0,
                        'message':'Akun telah dihapus'
                    })
                else:
                    return Response({
                    'status':0,
                    'message':'Akun tersebut belum teraktivasi'
                    })
            return Response({
                'message':1,
                'sessionId':session_key,
                'jenisAkun':profile.kategori,
                'email':user.email,
                'foto':profile.foto.url,
                'nama':user.username
            },status=status.HTTP_200_OK)

        else:

            # Jika username dan password yang dilempar untuk Query user ada
            try:
                userLoginFail=AccountLoginAttempt.objects.filter(
                    user=User.objects.get(
                        username=request.data['username']
                    )
                )

                # Menghandle untuk yang terus mencoba login setelah lebih dari 1x
                if userLoginFail.exists():
                    kondisiWaktu=userLoginFail.last().lastLogin.hour - datetime.datetime.now().hour < 1

                    # Mencoba login lebih dari 5x dan kurang dari satu jam
                    if len(userLoginFail)>=5 and kondisiWaktu:
                        return Response({
                            'message':'akun ada terkunci selama 1 jam'
                        })
                    
                    # Mencoba lebih dari 5x tapi waktu sudah lebih dari 1 jam
                    elif len(userLoginFail)>=5 and not kondisiWaktu:
                        attempts=AccountLoginAttempt.objects.filter(user=user)
                        for i in range(0,len(attempts)-1):
                            attempts[i].delete()
                        return Response({
                            'message':'Username atau Password Salah'
                        })
                    
                    # Mencoba kurang dari 5x dan kurang dari 1 jam (Default)
                    else:
                        AccountLoginAttempt.objects.create(
                            user=User.objects.get(
                                username=request.data['username']
                            )
                        )
                        return Response({
                            'message':'Username atau Password Salah'
                        })
            # Unuk menangkap User yang belum daftar tapi coba melempar login ke Back-end Environment
            except:
                if not User.objects.get(email=request.data['email']).is_active:
                    if AccountProfile.objects.get(user__email=request.data['email']).flag == False:
                        return Response({
                            'status':0,
                            'message':'Akun telah dihapus'
                        })
                    else:
                        return Response({
                            'status':0,
                            'message':'Akun belum teraktivasi'
                        })
                return Response({
                    'message':"Kata sandi yang dimasukkan tidak tepat"
                })

class RememberLoginAPIView(APIView):

    def post(self,request,*args,**kwargs):
        session_key=request.data['sessionId']
        user=getUser(session_key=session_key)

        if user is not None:
            try:
                rememberAccount=RememberAccount.objects.get(user=user)
                if rememberAccount.timeLastSession.day-datetime.datetime.now().day > 60:
                    rememberAccount.delete()
                    return Response({
                        'message':0
                    })
            except:
                pass
            login(request,user)
            return Response({
                'message':1,
                'sessionId':self.request.session.session_key,
                'jenisAkun':AccountProfile.objects.get(user=user).jenisAkun
            })
        else:
            return Response({
                'message':0
            })

class CheckLogin(APIView):

    def post(self,request,*args,**kwargs):
        expired_date=Session.objects.get(session_key=self.request.data["sessionId"]).expire_date
        if timezone.now() < expired_date:
            return Response({
                'status':1
            })
        else:
            return Response({
                'status':0,
                'message':'Anda harus login kembali'
            })


class RegisterAPIView(APIView):

    permission_classes=(AllowAny,)

    def get(self,request,*args,**kwargs):
        username='jihad354'
        passwordInput=request.query_params['password']
        user=authenticate(request=request,username=username,password=passwordInput)
        return Response({
            'password':'newUserObj.password'
        })

    def post(self,request,*args,**kwargs):

        print(request.data['enkripsi'])

        if User.objects.filter(username=request.data['person']).exists() and User.objects.filter(email=request.data['email']).exists():
            return Response({
                'status':0,
                "message":"User dengan nama kontak tersebut sudah terdaftar<br/>Email tersebut sudah terdaftar"
            })

        if User.objects.filter(username=request.data['person']).exists():
            return Response({
                'status':0,
                'message':'User dengan nama kontak tersebut sudah terdaftar'
            })
        if User.objects.filter(email=request.data['email']).exists():
            return Response({
                'status':0,
                'message':'Email tersebut sudah terdaftar'
            })

        newUser=User.objects.create_user(
            email=request.data['email'],
            username=request.data['person'],
            password=request.data['enkripsi'],
        )
        newUser.is_active=False
        newUser.save()
        AccountLoginAttempt.objects.create(
            user=newUser
        )
        AccountProfile.objects.create(
            user=newUser,
            namaPerusahaan=request.data['namaPerusahaan'],
            noKontak=request.data['contact'],
            person=request.data['person']
        )
        current_site = get_current_site(request)
        mail_subject = "Aktivasi akun Ekrutes"
        pesan = render_to_string('activate.html',{
					'user' : newUser,
					'domain' : current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(newUser.pk)),
					'token': account_activation_token.make_token(newUser),
		})
        send_mail(
			    mail_subject,
			    pesan,
			    EMAIL_HOST_USER,
			    [newUser.email],
			    fail_silently=False,
			)
        return Response({
            'message':1
        })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Akun telah teraktivasi!')
    else:
        return HttpResponse('Activation link is invalid!')

class ForgotPasswordAPIView(APIView):

    def post(self,request,*args,**kwargs):
        try:
            user=User.objects.get(email=request.data['email'])
        except:
            user=None
        if user is not None:
            current_site=get_current_site(request)
            code=get_random_string(length=32)
            code=str(code)
            RequestResetPass.objects.create(
                user=user,
                code=code
            )
            link="http://file://D:/PROJECT_WEB/ekrutes/view/login.html?act=reset_act&index={}".format(code)
            template=get_template('pesan-reset-pass.html')
            context={
                'user':user,
                'domain':current_site.domain,
                'link': code,
            }
            content=template.render(context)
            msg = EmailMultiAlternatives("Reset Password", "Important Message",EMAIL_HOST_USER, [user.email])
            msg.attach_alternative(content, "text/html")
            msg.send()
            return Response({
                'message':1
            })
        else:
            return Response({
                'status':0,
                'message':'Email tidak terdaftar'
            })

class PasswordInputAPIView(APIView):

    def post(self,request,*args,**kwargs):
        try:
            # uid=force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user=RequestResetPass.objects.get(code=kwargs['uidb64']).user
            user.set_password(request.data['enkripsi'])
            user.save()
            RequestResetPass.objects.get(user=user).delete()
        except:
            user = None
        if user is not None:
            return Response({
                'username':user.username,
                'message':1
            })
        else:
            return Response({
                'status':0,
                'message':'Tautan reset password ini sudah tidak berlaku'
            })

class PilihKota(APIView):

    def get(self,request,*args,**kwargs):
        user=getUser(session_key=self.request.query_params['sessionId'])
        id_provinsi=int(self.request.query_params['id'])

        if user is not None:
            kota=Kota.objects.filter(f_id_prov=id_provinsi).extra(
                select={
                    'id':'id_kota',
                    'text':'nama_kota'
                }
            ).values(
                'id',
                'text'
                )
            print(kota)
            return Response({
                'status':1,
                'message':'Data berhasil ditemukan',
                'results':kota
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status':0,
                'message':'Data tidak ditemukan'
            })

class PilihKecamatan(APIView):

    def get(self,request,*args,**kwargs):
        user=getUser(session_key=self.request.query_params['sessionId'])
        id_kota=int(self.request.query_params['id'])

        if user is not None:
            kecamatan=Kecamatan.objects.filter(f_id_kota=id_kota).extra(
                select={
                    'id':'id_kecamatan',
                    'text':'nama_kecamatan'
                }
            ).values(
                'id',
                'text'
                )
            return Response({
                'status':1,
                'message':'Data berhasil ditemukan',
                'results':kecamatan
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status':0,
                'message':'Data tidak ditemukan'
            })

class LogoutUserAPIView(APIView):

    def post(self,request,*args,**kwargs):

        session_key=self.request.data['sessionId']
        user=getUser(session_key=session_key)
        if user is not None:
            logout(self.request)
            Session.objects.get(session_key=session_key).delete()
            return Response({
                'status':1
            })
        else:
            return Response({
                'status':0,
                'message':'login gagal'
            })