from django.shortcuts import render

def mainfunc(request):
    if request.method == 'POST[inlineRadioOptions6]':
    return render(request, 'main.html', {})
    
    elif request.method == 'POST[inlineRadioOptions5]':
    return render(request, 'main.html', {})


    return render(request, 'main.html', {})


def hiyoshifunc(request):
    return render(request, 'hiyoshi.html', {})


    
