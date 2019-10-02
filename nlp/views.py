from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import TextForm
from django.shortcuts import redirect
from . import nlp  # to import various nlp functions
from django.core.files.storage import FileSystemStorage  # for file uploads
# mixin from some django class to check for authorized login
from django.contrib.auth.mixins import LoginRequiredMixin
# so these are just like common template things for views?
from django.views import generic
from .models import TextInstance, TextUploadDB
from .forms import AddText, TextUploadDB, UploadForm, UploadText

# My 'page' views go here


def index(request):
    return render(request, 'nlp/index.html', {})


def uploadtest(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            # this binds to form I believe?
            addtext = form.save(commit=False)
            # need to save to current user!
            addtext.owner = request.user
            # save in DB
            addtext.save()
            textname = addtext.title
            return render(request, 'nlp/upload_success.html', {'textname': textname})
    else:
        form = UploadForm()
    # display form on 'get'
    return render(request, 'nlp/uploadtest.html', {'form': form})

# old version where I was working on file upload
# def uploadtest(request):
#     if request.method == 'POST':
#         form = TextUploadDB(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = TextUploadDB(docfile=request.FILES['docfile'])
#             newdoc.save()
#             textname = TextUploadDB.title
#             return render(request, 'nlp/upload_success.html', {'textname': textname})
#     else:
#         form = TextUploadDB()
#     # display form on 'get'
#     return render(request, 'nlp/uploadtest.html', {'form': form})


# the view to upload a 'text' (currently just a title field)
def upload(request):
    if request.method == "POST":
        form = AddText(request.POST)
        # so where do I add any custom validation or specify what the validation is?
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            textname = post.title
            # really important: note that this is render() and not redirect(). this has caused confusion in the past
            # you do not need to mess with urls.py when you are render()ing things. just on redirect().
            return render(request, 'nlp/upload_success.html', {'textname': textname})
        else:
            form = AddText()
            return render(request, 'nlp/upload.html', {'form': form})
    form = AddText()
    return render(request, 'nlp/upload.html', {'form': form})


# generic class-based view for listing text uploaded by current user
# class TextsByUserListView(LoginRequiredMixin, generic.ListView):
#     model = TextInstance
#     template_name = 'nlp/user_texts.html'
#     # let's leave this alone for now
#     # paginate_by = 10
#
#     def get_queryset(self):
#         # oh shit is owner an arg for .filter? I jusut mean the thing in Text. the colors
#         # in pycharm might be throwing me off here
#         return TextInstance.objects.filter(owner=self.request.user)

# working off the model above, but updating it to show user-uploaded texts
class TextsByUserListView(LoginRequiredMixin, generic.ListView):
    model = UploadText
    template_name = 'nlp/user_texts.html'
    # paginate_by = 10

    def get_queryset(self):
        # list = UploadText.objects.filter(owner=self.request.user)
        # this part seems to work
        # for l in list:
        #     print(l)
        return UploadText.objects.filter(owner=self.request.user)


# Stuff for form uploads down here

# this is for the form where you enter a sentence to parse
def post_new(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = cd.get('a')
            length = len(post)
            doc = nlp.read(post)
            pos = nlp.posmatch(doc)
            dep = nlp.depmatch(doc)
            viz = nlp.visualize(post)
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
