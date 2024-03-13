import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.views import generic
import time
import os
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.http import JsonResponse


# Create your views here.
def view(request):
    return render(request, template_name="view.html")


def file_scan(request):
    file_dir = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'attachment')
    file_lists = {}
    last_color = ''
    for dirpath, dirnames, filenames in os.walk(file_dir):
        color = ['link-primary', 'link-secondary', 'link-success',
                 'link-danger', 'link-warning', 'link-info', 'link-dark']
        select_color = color[random.randint(0, len(color) - 1)]
        while select_color.__eq__(last_color):
            select_color = color[random.randint(0, len(color) - 1)]
            last_color = select_color
        date = dirpath.split('/')[-1].split('\\')[-1]
        file_lists[date] = {}
        for filename in filenames:
            file_lists[date][os.path.join(date, filename)] = select_color
    if 'date' in request.GET and 'filename' in request.GET:
        return render(request, template_name='file_scan.html',
                      context={'file_lists': file_lists, 'upload_file' : os.path.join(request.GET['date'], request.GET['filename'])})
    else:
        return render(request, template_name='file_scan.html', context={'file_lists': file_lists})


def save_file(file):
    curttime = time.strftime("%Y%m%d")
    # 规定上传目录
    upload_url = os.path.join(settings.MEDIA_ROOT, 'attachment', curttime)
    # 判断文件夹是否存在
    folder = os.path.exists(upload_url)
    if not folder:
        os.makedirs(upload_url)
        print("创建文件夹")
    if file:
        file_name = file.name
        # 判断文件是是否重名，懒得写随机函数，重名了，文件名加时间
        if os.path.exists(os.path.join(upload_url, file_name)):
            name, etx = os.path.splitext(file_name)
            addtime = time.strftime("%Y%m%d%H%M%S")
            finally_name = file.name
            # finally_name = name + "_" + addtime + etx
        else:
            finally_name = file.name
        # 文件分块上传
        upload_file_to = open(os.path.join(upload_url, finally_name), 'wb+')
        for chunk in file.chunks():
            upload_file_to.write(chunk)
        upload_file_to.close()
        # 返回文件的URl
        file_upload_url = settings.MEDIA_URL + 'attachment/' + curttime + '/' + finally_name
        # 构建返回值
        response_data = {}
        response_data['FileName'] = file_name
        response_data['FileUrl'] = file_upload_url
        response_json_data = json.dumps(response_data)  # 转化为Json格式
        return curttime, file_name
    return curttime, None

def file_upload(request):
    if request.method == 'GET':
        return render(request, template_name='fileUpload.html')
    file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
    curttime, file_name = save_file(file)
    if file_name is None:
        return HttpResponse("no file found")
    return HttpResponseRedirect(reverse("tickets:scan_file_upload") + "?date={}&filename={}".format(curttime, file_name))

def download(request, year, name):
    download_url = os.path.join(settings.MEDIA_ROOT, 'attachment', year, name)
    file = open(download_url, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(name)
    return response

def progress_show_entry(request):
    return render(request, template_name='progress.html')

num_progress = {}

@csrf_exempt
def process_file(request):
    print("entry process_file")
    file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
    curttime, file_name = save_file(file)
    global num_progress
    num_progress[file_name] = 0
    for i in range(10):
        # ... 数据处理业务
        num_progress[file_name] = i * 100 / 10
        # 更新后台进度值，因为想返回百分数所以乘100
        # print 'num_progress=' + str(num_progress)
        time.sleep(1)
        res = num_progress[file_name]
        # print 'i='+str(i)
        # print 'res----='+str(res)
    res = 100
    num_progress[file_name] = 100
    time.sleep(1)
    retData = {
        'file' : "zttttttttttttttt.txt",
        'path' : os.path.join(curttime, "zttttttttttttttt.txt")
    }
    return JsonResponse(retData, safe=False)


'''
前端JS需要访问此程序来更新数据
'''
def progress_show(request):
    print('{} show_progress----------{}'.format(request.GET['file'], num_progress[request.GET['file']]))
    return JsonResponse(num_progress[request.GET['file']], safe=False)
