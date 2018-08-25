import sys

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .models import Account,Manager,Outlets
import json
import csv

# Create your views here.

def get_response_from_data(data: dict):
    response = HttpResponse(json.dumps(data))
    response['Content-Type'] = "application/json"
    return response




@csrf_exempt
def CreateCustomUserView(request):
    print("hello")
    if request.method == "GET":
        return HttpResponse(json.dumps({"status": "error",
                                        "errors": ["GET Request not allowed"]
                                        }))
    try:
        request_json = json.loads(request.body.decode("utf-8"))  # when postman
    except Exception as E:
        request_json = request.POST.copy()
    try:
        obj = Account.objects.create(**request_json)
        user = User.objects.create_user(username = request_json["username"],email=request_json["email"],password=request_json["password"])
        user.save()
        obj.password = user.password
        obj.save()

        print("User created succefully")

        data = {
            "status": "success",
            "message":"user created succesfully"
        }

        response = HttpResponse(json.dumps(data))
        response['Content-Type'] = "application/json"
        return response

    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("in line no", exc_tb.tb_lineno)
        print("error is ", E)
        data = {
            "status": "error",
            "errors": str(E)
        }

        response = HttpResponse(json.dumps(data))
        response['Content-Type'] = "application/json"
        return response



@csrf_exempt
def LoginView(request):
    try:
        print(request.auth)
    except:
        print("No auth")
    print("user is", request.user)
    if request.method == "GET":
        # return render(request, "app_one/adjustment_add.html", {"form": LoginForm()})
        data = {"status": "error",
                "message": "GET Request not allowed"
                }

        return get_response_from_data(data)
    try:
        request_json = json.loads(request.body.decode("utf-8"))
    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("in line no", exc_tb.tb_lineno)
        request_json = request.POST.copy()

    try:
        custom_user = Account.objects.get(username = request_json['username'],user_type= request_json["user_type"])
        request.user_type = request_json["user_type"] # adding the user type in request object
        user = authenticate(username=request_json["username"],password=request_json["password"])
        if user is not None:
            if user.is_active:
                login(request, user)

                data = {"status": "success",
                        "message":"login successfully",
                        "token":Token.objects.get(user=user).key
                        }
                return HttpResponse(json.dumps(data),content_type="text/javascript")
                # Redirect to a success page.
            else:
                print("user is not active")
                data = {"status": "error",
                        "message": "user is not active"
                        }
                return HttpResponse(json.dumps(data), content_type="text/javascript")
                # Redirect to a success page.
        else:
            data = {"status": "error",
                    "message": "User is not registered"
                    }
            return HttpResponse(json.dumps(data), content_type="text/javascript")
        # Return a 'disabled account' error message
    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("in line no", exc_tb.tb_lineno)
        print("error is ", E)

        data = {
            "status": "error",
            "message": str(E)
        }
        return get_response_from_data(data)


@csrf_exempt
def logoutUser(request):
    print(request.method)
    if request.method == "GET":
        # return render(request, "app_one/adjustment_add.html", {"form": LoginForm()})
        data = {"status": "error",
                "errors": ["GET Request not allowed"]
                }
        return get_response_from_data(data)
    if hasattr(request, "auth"):
        token = request.auth
        token.delete()
        print("deleted")
    logout(request)
    data = {
        "status": "success"
    }

    return get_response_from_data(data)



#salesmanview
@csrf_exempt
def salesmanView(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            li = []

            #for i in


    else:

        response_data = {"status": "error", "message": "Please Login first"}

        return HttpResponse(json.dumps(response_data), content_type="text/javascript")



from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2): # for calculating distance
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r









@csrf_exempt
def imageUpload(request):
    print("hello")


    if request.user.is_authenticated:

        if request.method == "GET":
            return HttpResponse(json.dumps({"status": "error",
                                            "errors": ["GET Request not allowed"]
                                            }))
        try:
            request_json = json.loads(request.body.decode("utf-8"))  # when postman

        except Exception as E:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("in line no", exc_tb.tb_lineno)
            request_json = request.POST.copy()


        try:
            image = request.FILES["image"]
        except Exception as E:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("in line no", exc_tb.tb_lineno)
            print(E)
            image = None
        if image != None:

            try:
                user = Account.objects.get(username=request.auth.user.username)

                outlets_list = Outlets.objects.filter(user=user)
                for i in outlets_list:
                    lon1  = i.long
                    lat1 = i.lang
                    lon2 = request_json["longitude"]
                    lat2 = request_json["latitude"]

                    if haversine(lon1,lat1,lon2,lat2) <= 400:
                        manager_obj = Manager.objects.create(image= image,outlet = i)
                        response_data = {"status": "error", "message": "Please upload the image for given loction"}
                        return HttpResponse(json.dumps(response_data),content_type="text/javascript")

                response_data = {"status": "error", "message": "Outlets is not found with given latitude and longitude"}
                return HttpResponse(json.dumps(response_data), content_type="text/javascript")




            except Exception as E:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("in line no", exc_tb.tb_lineno)
                print(E)
                response_data = {"status":"error","message":str(E)}

                return HttpResponse(json.dumps(response_data),content_type="text/javascript")

        else:
            response_data = {"status": "error", "message": "Please upload the image for given loction"}

            return HttpResponse(json.dumps(response_data), content_type="text/javascript")

    else:

        response_data = {"status": "error", "message": "Please Login first"}

        return HttpResponse(json.dumps(response_data), content_type="text/javascript")


@csrf_exempt
@api_view(["GET"])
def managerView(request):
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        print(request.user)
        if request.method == "GET":

            li = []

            for i in Manager.objects.all():
                print(i.outlet.name)
                image_url = "http://192.168.43.12:8000/media/"+str(i.image)
                di = {"id":i.id,"image":image_url,"outlet":i.outlet.name,"salesman":i.outlet.user.name}
                li.append(di)

            response_data = {"status": "success", "data": li}

            return HttpResponse(json.dumps(response_data), content_type="text/javascript")

    else:

        response_data = {"status": "error", "message": "Please Login first"}

        return HttpResponse(json.dumps(response_data), content_type="text/javascript")














#for downloading the content
def downloadCSV(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="outlets_grade.csv"' # it add the extension csv on file name
        writer = csv.writer(response)
        import datetime
        now = datetime.date.today()
        print(now)

        writer.writerow(('Manager Name','Outlet Name','Salesman','Grade','Date'))

        for i in Manager.objects.filter(date=now):
            listi = (request.auth.user.username,i.outlet.name, i.outlet.user.name, i.grade,i.date)
            writer.writerow(listi)
        return response

    else:
        return HttpResponse("login first")













