from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import User, Record, Admin
from .md5_utils import calc_md5
from imageai.Prediction import ImagePrediction
from imageai.Detection import ObjectDetection
import requests
import datetime
import keras
import sys
import os
from image_ai.settings import MEDIA_ROOT


def admin_login(request):
    # check if already logged
    if request.session.get('is_admin_login', None):
        # get all users information
        users_info = {}
        for user in User.objects.all():
            users_info[user.username] = user.record_set.all().count()
        message = 'Info: welcome back'
        # show all users in admin.html
        return render(request, 'login/admin.html', {
            'users_info': users_info,
            'message': message
        })

    # check account and password
    if request.method == "POST":
        username = request.POST.get('username', '')
        admin = Admin.objects.filter(username=username).first()
        if admin:
            # check password
            password = request.POST.get('password', '')
            if calc_md5(password) != admin.password:
                message = "Error: password is wrong"
                # return to admin login html
                return render(request, 'login/login.html', {
                    "message": message,
                    'user_type': 'Administrator'
                })
            else:
                request.session['is_admin_login'] = True
                request.session['admin_name'] = admin.username

                # session cookies in valid in 20 minutes
                request.session.set_expiry(1200)
                users_info = {}
                for user in User.objects.all():
                    users_info[user.username] = user.record_set.all().count()
                # show all users in admin.html
                return render(request, 'login/admin.html',
                              {'users_info': users_info})
        else:
            # not found that admin
            message = "Error: no such a administrator"
            return render(request, 'login/login.html', {
                "message": message,
                'user_type': 'Administrator'
            })
    else:
        return render(request, 'login/login.html',
                      {'user_type': 'Administrator'})


def login(request):
    # check if already login
    if request.session.get('is_login', None):
        message = 'Info: welcome back'
        return render(request, 'login/index.html', {
            'username': request.session['user_name'],
            'message': message
        })

    if request.method == "POST":
        username = request.POST.get('username', '')
        user = User.objects.filter(username=username).first()
        if user:
            # check password
            password = request.POST.get('password', '')
            if calc_md5(password) != user.password:
                message = "Error: password is wrong"
                return render(request, 'login/login.html', {
                    "message": message,
                    'user_type': 'User'
                })
            else:
                request.session['is_login'] = True
                request.session['user_name'] = user.username

                # session cookies in valid in 20 minutes
                request.session.set_expiry(1200)
                return render(request, 'login/index.html',
                              {'username': username})
        else:
            # user not found
            message = "Error: no such a user"
            return render(request, 'login/login.html', {
                "message": message,
                'user_type': 'User'
            })
    else:
        return render(request, 'login/login.html', {'user_type': 'User'})


def logon(request):
    # check the request method
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # password match
        if password1 != password2:
            message = "Error: passwords don't match"
            return render(request, 'login/logon.html', {"message": message})

        # search user in database by username
        user = User.objects.filter(username=username).first()
        if user:
            message = "Error: user already exists"
            return render(request, 'login/logon.html', {"message": message})

        # entropy password in database
        User.objects.create(username=username, password=calc_md5(password1))
        message = "Info: you have created an account"
        return redirect('/login/', {"message": message, 'user_type': 'User'})
    else:
        return render(request, 'login/logon.html')


def logout(request):
    # check if admin or user logged
    if request.session.get('is_login', None) or request.session.get(
            'is_admin_login', None):
        message = "Info: you have logged out"
        request.session.flush()  # clear cookies
    else:
        message = "Error: not logged or session expired"

    # back to user login html
    return render(request, 'login/login.html', {
        "message": message,
        'user_type': 'User'
    })


def about(request):
    # render about.html regardless of whether logged
    return render(request, 'login/about.html')


def record(request, username):
    # check if admin or specific user logging
    if request.session.get('is_admin_login', None) or \
            (request.session.get('is_login', None) and request.session.get('user_name', None) == username):
        # now_user get the identity
        now_user = username
        if request.session.get('is_admin_login', None):
            now_user = 'Administrator'

        if request.method == "POST":
            # get records need deleting
            record_delete = request.POST.getlist('record_delete', [])
            for record_id in record_delete:
                rec = Record.objects.filter(record_id=record_id)
                rec.delete()

        # show the records filtered by datetime
        user = User.objects.filter(username=username).first()
        start = request.GET.get('user_date_start', '')
        end = request.GET.get('user_date_end', '')

        # if not valid datetime input then show all records
        # if start date is later than end date, it will show zero record
        if not (start and end):
            all_record = user.record_set.all()
        else:
            start_day = datetime.date(*map(int, start.split('-')))
            end_day = datetime.date(*map(int, end.split('-')))
            all_record = user.record_set.filter(time__range=(start_day,
                                                             end_day))

        # show records by paginator
        # one page contains 10 record at most by default
        p = Paginator(all_record, 10)

        # the page view information will store in data
        if p.num_pages <= 1:
            records = all_record
            data = ''
        else:
            page = int(request.GET.get('page', 1))
            records = p.page(page)
            left = []                   # left page
            right = []                  # right page
            left_has_more = False       # is left ellipsis needed
            right_has_more = False      # is right ellipsis needed
            first = False               # is first page needed
            last = False                # is last page needed
            total_pages = p.num_pages
            page_range = p.page_range
            if page == 1:
                right = page_range[page:page + 2]
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True
            elif page == total_pages:
                left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True
            else:
                left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
                right = page_range[page:page + 2]
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True
            data = {  # page view information
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
                'total_pages': total_pages,
                'page': page
            }
        # render record.html
        return render(
            request, 'login/record.html', {
                'records': records,
                'data': data,
                'record_owner': username,
                'username': now_user
            })
    else:
        # not admin or correct user logging
        message = "Error: not logged or session expired"
        return render(request, 'login/login.html', {
            "message": message,
            'user_type': 'User'
        })


def index(request):
    # check if correct user logging
    if not request.session.get('is_login', None):
        message = "Error: not logged in or session expired"
        return render(request, 'login/login.html', {
            "message": message,
            'user_type': 'User'
        })

    username = request.session.get('user_name', '')

    if request.method == "POST":
        # get the image file uploaded
        imgfile = request.FILES.get('imgfile', None)

        # get the URL uploaded
        imgurl = request.POST.get('imgurl', None)

        if not (imgfile or imgurl):
            message = 'Info: require an image or url'
            return render(request, 'login/index.html', {
                'message': message,
                'username': username
            })

        if imgfile:
            # avoid illegal file uploaded
            filekind = str(imgfile).split('.')[-1]
            if filekind not in [
                    'jpg', 'jpeg', 'gif', 'bmp', 'png', 'JPG', 'JPEG', 'GIF',
                    'BMP', 'PNG'
            ]:
                sys.stderr.write("Error: invalid file error.")
                message = 'Error: not valid image format'
                return render(request, 'login/index.html', {
                    'message': message,
                    'username': username
                })

            # is necessary to clear session before load models
            keras.backend.clear_session()

            # get three loaded models
            predictor_sqz, predictor_res, detector_res = load_models()

            # create record
            record = Record()
            record.handImg = imgfile
            record.user = User.objects.filter(username=username).first()
            record.save()
            nowtime = record.time
            filepath = os.path.join(MEDIA_ROOT, requests.utils.unquote(
                Record.objects.filter(time=nowtime).first().handImg.url)[7:])

            sqz = predictor_sqz.predictImage(filepath, result_count=5)
            res = predictor_res.predictImage(filepath, result_count=5)

            Record.objects.filter(time=nowtime).update(imgPredict_res=res)
            Record.objects.filter(time=nowtime).update(imgPredict_sqz=sqz)

            # change output by models to dict type in order to show on html
            result_res = dict(zip(res[0], res[1]))
            result_sqz = dict(zip(sqz[0], sqz[1]))

            pathlist = filepath.split('/')
            outname = str(pathlist[-1])
            index = outname.rfind('.')
            detect_outfile = 'result/' + outname[:index] + '_out' + outname[
                index:]
            detector_res.detectObjectsFromImage(filepath,
                                                os.path.join(MEDIA_ROOT, detect_outfile))

            Record.objects.filter(time=nowtime).update(
                imgDetect=detect_outfile)
            record = Record.objects.filter(time=nowtime).first()

            # release memory
            del predictor_res
            del predictor_sqz
            del detector_res

            # show results in html
            return render(
                request, 'login/index.html', {
                    'record': record,
                    'username': username,
                    'result_res': result_res,
                    'result_sqz': result_sqz
                })

        if imgurl:
            keras.backend.clear_session()

            # check if download successfully
            try:
                r = requests.get(imgurl)
            except Exception:
                sys.stderr.write("Error: download error.")
                message = 'Error: not valid image url'
                return render(request, 'login/index.html', {
                    'message': message,
                    'username': username
                })
            filename = calc_md5(imgurl) + '.jpg'
            filepath=os.path.join(MEDIA_ROOT, 'download/'+filename)
            with open(filepath, 'wb') as f:
                f.write(r.content)
                

            predictor_sqz, predictor_res, detector_res = load_models()

            record = Record()
            record.handImg = 'download/' + filename
            record.user = User.objects.filter(username=username).first()
            record.save()
            nowtime = record.time

            sqz = predictor_sqz.predictImage(filepath, result_count=5)
            res = predictor_res.predictImage(filepath, result_count=5)

            Record.objects.filter(time=nowtime).update(imgPredict_res=res)
            Record.objects.filter(time=nowtime).update(imgPredict_sqz=sqz)

            result_res = dict(zip(res[0], res[1]))
            result_sqz = dict(zip(sqz[0], sqz[1]))

            pathlist = filepath.split('/')
            outname = str(pathlist[-1])
            index = outname.rfind('.')

            detect_outfile = 'result/' + outname[:index] + '_out' + outname[
                index:]
            detector_res.detectObjectsFromImage(filepath,
                                                os.path.join(MEDIA_ROOT, detect_outfile))

            Record.objects.filter(time=nowtime).update(
                imgDetect=detect_outfile)
            record = Record.objects.filter(time=nowtime).first()

            del predictor_res
            del predictor_sqz
            del detector_res

            return render(
                request, 'login/index.html', {
                    'record': record,
                    'username': username,
                    'result_res': result_res,
                    'result_sqz': result_sqz
                })

    # request method is not POST
    return render(request, 'login/index.html', {
        'message': 'Info: require POST',
        'username': username
    })


# returns three models
def load_models():
    # load models
    keras.backend.clear_session()

    # SqueezeNet for image recognition
    # higher speed and intermediate accuracy
    predictor_sqz = ImagePrediction()
    predictor_sqz.setModelTypeAsSqueezeNet()
    predictor_sqz.setModelPath(os.path.join(MEDIA_ROOT, 'models/squeezenet_weights_tf_dim_ordering_tf_kernels.h5'))
    predictor_sqz.loadModel()

    # ResNet for image recognition
    # high speed and high accuracy
    predictor_res = ImagePrediction()
    predictor_res.setModelTypeAsResNet()
    predictor_res.setModelPath(os.path.join(MEDIA_ROOT, 'models/resnet50_weights_tf_dim_ordering_tf_kernels.h5'))
    predictor_res.loadModel()

    # RetinaNet for object detection
    detector_res = ObjectDetection()
    detector_res.setModelTypeAsRetinaNet()
    detector_res.setModelPath(os.path.join(MEDIA_ROOT, 'models/resnet50_coco_best_v2.0.1.h5'))
    detector_res.loadModel()

    return predictor_sqz, predictor_res, detector_res
