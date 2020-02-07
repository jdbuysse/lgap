from django.shortcuts import render, redirect
from . import nlp  # to import various nlp functions
# django file handling
from django.core.files import File
# mixin from some django class to check for authorized login
from django.contrib.auth.mixins import LoginRequiredMixin
# templates for view
from django.views import generic, View
# forms
from .forms import TextForm, UploadForm, UploadText, WorkspaceForm, ProcessTextForm, DocumentForm, UploadToBytesForm, BookForm
from django.core.files.storage import FileSystemStorage
from .models import Book

# function views up here
# home page/index
def index(request):
    return render(request, 'nlp/index.html', {})


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
            return render(request, 'nlp/textresult.html', {'post': post, 'pos': pos, 'dep': dep,
                                                           'viz': viz, 'len': length})
    else:
        form = TextForm()
    return render(request, 'nlp/text_edit.html', {'form': form})


# my test model form upload
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DocumentForm()
    return render(request, 'nlp/file_upload_practice.html', {
        'form': form
    })


# class based views here
# user 'workspace' page
class WorkspaceView(LoginRequiredMixin, View):

    form_class_query = WorkspaceForm
    template_name = 'nlp/user_workspace.html'

    # send user object to the form to decide which text choices to display
    # worth digging a little more to understand this better
    def get_form_kwargs(self):
        kwargs = super(WorkspaceView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request):
        # create 'process text' form down here so that I can get user
        form_class_process = ProcessTextForm(user=request.user)
        return render(request, self.template_name, {
            'processform': form_class_process,
            'queryform': self.form_class_query,
        })

    def post(self, request):
        user = request.user
        if 'processform' in request.POST:
            processform = ProcessTextForm(request.POST, user=request.user)
            if processform.is_valid():
                cd = processform.cleaned_data
                # grab the text from the db
                workingfile = cd.get('text')
                queryform = WorkspaceForm()
                # process it to a docbin
                # save the docbin somehow...like this? https://gearheart.io/blog/how-to-upload-files-with-django/
                # save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['file'])
                # path = default_storage.save(save_path, request.FILES['file'])
                return render(request, self.template_name, {'workingfile': workingfile, 'user': user,
                                                            'queryform': queryform, 'processform': processform})
            return render(request, self.template_name, {})

        if 'queryform' in request.POST:
            form = WorkspaceForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # open the corresponding file that has been processed (the r is to interpret raw string rather than escape
                with open(r'C:\Users\jordan\Desktop\Projects\lgap-auth\documents\meal_prep_things.txt', 'w') as f:
                    # this is just grabbing the file type right now. want to get it into the shape of a list of strings right?
                    processedtext = File(f)
                query = cd.get('query')
                # grab the whole model so you can call things like model.fulltext
                model = cd.get('text')
                text = model.fulltext
                textlist = nlp.lineizer(text)
                matches = nlp.streamtolist(textlist, query)
                return render(request, 'nlp/query_result.html', {'query': query, 'matches': matches})
            return render(request, self.template_name, {})


# upload a text page
class UploadTextView(LoginRequiredMixin, View):
    form_class = UploadForm
    template_name = 'nlp/upload.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            addtext = form.save(commit=False)
            addtext.owner = request.user
            addtext.save()
            textname = addtext.title
            return render(request, 'nlp/upload_success.html', {'textname': textname})
        return render(request, self.template_name, {'form': form})


# show user-uploaded texts with a queryset at /mytexts/
class TextsByUserListView(LoginRequiredMixin, generic.ListView):
    model = UploadText
    template_name = 'nlp/user_texts.html'
    # paginate_by = 10

    def get_queryset(self):
        return UploadText.objects.filter(owner=self.request.user)


class UploadToBytesView(LoginRequiredMixin, View):
    form_class = UploadToBytesForm
    template_name = 'nlp/upload_to_byte.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            addtext = form.save(commit=False)
            addtext.owner = request.user
            addtext.save()
            #print(form.name)
            textname = addtext.title
            return render(request, 'nlp/upload_success.html', {'textname': textname})
        return render(request, self.template_name, {'form': form})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'nlp/book_list.html', {'books': books})

def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.save(commit=False)
            # print(type(text.pdf)) returns <class 'django.db.models.fields.files.FieldFile'>
            # send the file as a string to get processed into a DocBin
            nlp.process_uploaded_file(str(request.FILES['pdf']), text.title)
            #form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'nlp/upload_book.html', {'form': form})

