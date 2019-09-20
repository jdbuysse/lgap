from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import TextForm
from django.shortcuts import redirect
from .nlp import *  # import everything for now, why not?
from django.core.files.storage import FileSystemStorage # for file uploads
# mixin from some django class to check for authorized login
from django.contrib.auth.mixins import LoginRequiredMixin
# so these are just like common template things for views?
from django.views import generic
from .models import TextInstance

# My 'page' views go here


def index(request):
    return render(request, 'nlp/index.html', {})


def upload(request):
    return render(request, 'nlp/upload.html', {})


# generic class-based view for listing text uploaded by current user
class TextsByUserListView(LoginRequiredMixin, generic.ListView):
    model = TextInstance
    template_name = 'nlp/user_texts.html'
    # let's leave this alone for now
    # paginate_by = 10

    def get_queryset(self):
        # oh shit is owner an arg for .filter? I jusut mean the thing in Text. the colors
        # in pycharm might be throwing me off here
        return TextInstance.objects.filter(owner=self.request.user)



# Stuff for form uploads down here

# this is for the form where you enter a sentence to parse
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


# upload textform on upload.html
# this is a 'minimal' implementation. a better way in the future may be to use model forms
# it's also not working: try the official docs at https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/
# for a better explanation
# def text_upload(request):
#     print('a')
#     if request.method == 'POST' and request.FILES['txtfile']:
#         txtfile = request.FILES['txtfile']
#         fs = FileSystemStorage()
#         filename = fs.save(txtfile.name, txtfile)
#         uploaded_file_url = fs.url(filename)
#         print(uploaded_file_url)
#         return render(request, 'nlp/upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'nlp/upload.html')
