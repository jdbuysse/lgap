from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import TextForm
from django.shortcuts import redirect
from .nlp import *  # import everything for now, why not?


# Create your views here.

def index(request):
    return render(request, 'nlp/index.html', {})


def post_new(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = cd.get('a')
            length = len(post)
            doc = read(post)
            pos = posmatch(doc)
            dep = depmatch(doc)
            viz = visualize(post)
            return render(request, 'nlp/textresult.html',
            {'post': post, 'pos': pos, 'dep': dep, 'viz': viz, 'len': length})
    else:
        form = TextForm()
    return render(request, 'nlp/text_edit.html', {'form': form})

def upload(request):
        return render(request, 'nlp/upload.html', {})

