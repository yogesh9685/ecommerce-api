from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.shortcuts import render
from django.contrib.auth import authenticate , login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .serializers import RegisterSerializer,LoginSerializer,OtpSerializer , ProductSerializer , CategorySerializer
from .models import OTPVerification ,Product , Category
import random
from rest_framework.viewsets import  ModelViewSet 
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .permission import IsSeller


class RegisterView(APIView):

    def get(self,request):
        return render(request,"register.html")


    def post(self,request):
        print(request.data)
        print(type(request.data))
    

        serializer = RegisterSerializer(data=request.data)
        print(request.data)
        print(type(request.data))
        if serializer.is_valid():
            
            user = serializer.save()

            otp = random.randint(100000,999999)

            OTPVerification.objects.create(user=user,otp=otp)

            send_mail(
                subject="OTP Verification",
                message=f"Your OTP is {otp}",
                from_email="yogeshgiri182@gmail.com",
                recipient_list=[user.email]
            )

            request.session["user_id"] = user.id

            return Response({"message":"OTP sent"})


        return Response(serializer.errors)



class OtpView(APIView):

    def get(self,request):
        return render(request,"verify_otp.html")


    def post(self,request):

        serializer = OtpSerializer(data=request.data)

        if serializer.is_valid():

            otp = serializer.validated_data["otp"]

            user_id = request.session.get("user_id")

            record = OTPVerification.objects.filter(
                user_id=user_id,
                otp=otp
            ).first() 
            print( "record  is " , record)
        

            if record:
                print(record.user)
                user = record.user
               
                if user.role == "seller":
                    user.is_seller = True
                user.is_verified = True
                user.save()

                record.delete()

                return Response({"message":"OTP verified"})

            return Response({"error":"Invalid "})

        return Response(serializer.errors)



class LoginView(APIView):

    def get(self,request):
        return render(request,"login.html")

    def post(self,request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username,password=password)

            if user:

                if not user.is_verified:
                    return Response({"error":"Email not verified"})

                login(request, user)  

                refresh = RefreshToken.for_user(user)

                return Response({

                    "access":str(refresh.access_token),
                    "refresh":str(refresh)

                })

            return Response({"error":"Invalid credentials"})

        return Response(serializer.errors)


class ProfileView(APIView):

    
    permission_classes = [IsAuthenticated]
    def get(self,request):

        return Response({

            "username":request.user.username,
            "email":request.user.email

        })
    


class ProductListView(ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    
    def get_permissions(self):

        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), IsSeller()]

        return [IsAuthenticated()]

    def get_queryset(self):

        category = self.request.query_params.get("category")

        if category:
            return Product.objects.filter(category_id=category)

        return Product.objects.all()

def home(request):
    print("User:", request.user)
    print("Username:", request.user.username)
    print("Seller:", request.user.is_seller)
    print(request.user.is_authenticated)
    print(request.user.is_seller)
    if request.user.is_authenticated and request.user.is_seller:
        return render(request, "sellerhome.html")
    else:
        return render(request, "home.html")

 

class CategoryListView(ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated]



@csrf_exempt
@api_view(["POST"])
def logout_view(request):

    try:

        refresh_token = request.data.get("refresh")

        token = RefreshToken(refresh_token)

        token.blacklist()

        return Response({"message": "Logout successful"})

    except Exception as e:

        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



def addProduct(request):

    return render(request , "product.html")


def seller(request):
    return render(request , "sellerhome.html")



def cart(request):
    return render(request , "cart.html")


def transaction(request):
    return render(request , "home.html")