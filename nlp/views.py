from django.shortcuts import render, redirect
from . import nlp  # to import various nlp functions
# django file handling
from django.core.files import File
# mixin from some django class to check for authorized login
from django.contrib.auth.mixins import LoginRequiredMixin
# templates for view
from django.views import generic, View
# forms
from .forms import TextForm, UploadForm, UploadText, WorkspaceForm, ProcessTextForm
from django.core.files.storage import FileSystemStorage
import io

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
        form_class_process2 = WorkspaceForm(user=request.user)
        return render(request, self.template_name, {
            'processform': form_class_process,
            'queryform': form_class_process2,
        })

    def post(self, request):
        user = request.user
        if 'processform' in request.POST:
            processform = ProcessTextForm(request.POST, user=request.user)
            #workspaceform = WorkspaceForm(request.POST, user=request.user)
            if processform.is_valid():
                # grab cleaned data from form
                cd = processform.cleaned_data
                # grab the text from the db
                workingfile = cd.get('text')
                # process into a docbin
                nlp.process_uploaded_file(workingfile.fulltext, workingfile.title)
                queryform = WorkspaceForm(None, user=request.user)
                return render(request, self.template_name, {'workingfile': workingfile, 'user': user,
                                                            'queryform': queryform, 'processform': processform})
            return render(request, self.template_name, {})

        if 'queryform' in request.POST:
            form = WorkspaceForm(request.POST, user=request.user)
            if form.is_valid():
                cd = form.cleaned_data
                query = cd.get('query')
                query = query.upper()
                # grab the whole model so you can call things like model.fulltext
                textname = cd.get('text')
                if nlp.check_for_file(textname) == 0:
                    matches = "ERROR: please make sure you've parsed your file in the 'Workspace' page first"
                else:
                    docs = nlp.deserialize_file(textname)
                    matches = nlp.makematches(docs, query)  # returns a string, for now at least
                return render(request, 'nlp/query_result.html', {'query': query, 'matches': matches, 'user': user})
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
            # saves the full text in the DB without any newlines
            addtext.fulltext = " ".join(addtext.fulltext.splitlines())
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


