import datetime, time
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.utils.crypto import get_random_string
from django.template import Context
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from psikotes.settings import EMAIL_HOST_USER
from akun.models import (
    AccountProfile,
    AccountStatus,
    AccountLoginAttempt,
    RememberAccount,
    RequestResetPass,
    getUser
)
from .serializers import UserSerializer


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
            login(self.request,user)
            session_key=self.request.session.session_key
            profile=AccountProfile.objects.get(user=user)
            try:
                if int(request.data['keeplogin']) == 1:
                    try:
                        lastSession=RememberAccount.objects.get(user=user)
                        lastSession.lastSession=session_key
                        lastSession.save()
                    except:
                        RememberAccount.objects.create(
                            user=user,
                            lastSession=session_key
                        )
            except:
                pass
            return Response({
                'message':1,
                'sessionId':session_key,
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
                if rememberAccount.timeLastSession.day-datetime.datetime.now().day > 30:
                    rememberAccount.delete()
                    return Response({
                        'message':0
                    })
            except:
                pass
            login(request,user)
            return Response({
                'message':1,
                'sessionId':self.request.session.session_key
            })
        else:
            return Response({
                'message':0
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

        email=request.data['email']
        username=email.split('@')[0]

        newUser=User.objects.create_user(
            email=request.data['email'],
            username=request.data['username'],
            password=request.data['password']
        )
        newUser.save()
        AccountLoginAttempt.objects.create(
            user=newUser
        )
        before=time.time()
        AccountProfile.objects.create(
            user=newUser,
            namaPerusahaan=request.data['namaPerusahaan'],
            alamatPerusahaan=request.data['alamatPerusahaan'],
            noKontak=request.data['noKontak'],
            foto=request.data['foto']
        )
        print(time.time()-before)
        AccountStatus.objects.create(
            user=newUser
        )
        return Response({
            'pesan':'OKE'
        })

class ForgotPasswordAPIView(APIView):

    def post(self,request,*args,**kwargs):
        # try:
        user=User.objects.get(email=request.data['email'])
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