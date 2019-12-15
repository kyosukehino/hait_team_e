from django.shortcuts import render

def mainfunc(request):
    if request.method == 'POST[inlineRadioOptions6]':
        hiyoshi = request.POST['inlineRadioOptions6']


    return render(request, 'main.html', {})


def hiyoshifunc(request):
    return render(request, 'hiyoshi.html', {})


    