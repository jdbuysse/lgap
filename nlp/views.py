from django.shortcuts import render
from . import nlp  # to import various nlp functions
# mixin from some django class to check for authorized login
from django.contrib.auth.mixins import LoginRequiredMixin
# so these are just like common template things for views?
from django.views import generic
# forms
from .forms import TextForm, UploadForm, UploadText, WorkspaceForm, ProcessTextForm

# workspace


def workspace(request):
    workingfile = "empty rn"
    user = request.user
    if request.method == "POST":
        if 'processform' in request.POST:
            processform = ProcessTextForm(request.POST)
            if processform.is_valid():
                cd = processform.cleaned_data
                rawtext = cd.get('text')
                workingfile = 'file from processform'
                queryform = WorkspaceForm()
                # add something to process the text
                return render(request, 'nlp/workspace.html', {'workingfile': workingfile, 'user': user,  'queryform': queryform, 'processform': processform})

            return render(request, 'nlp/workspace.html', {})
        if 'queryform' in request.POST:
            form = WorkspaceForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                query = cd.get('query')
                # grab the whole model so you can call things like model.fulltext
                model = cd.get('text')
                text = model.fulltext
                textlist = nlp.lineizer(text)
                matches = nlp.streamtolist(textlist, query)
                return render(request, 'nlp/query_result.html', {'query': query, 'matches': matches})

    else:
        queryform = WorkspaceForm()
        processform = ProcessTextForm()
    return render(request, 'nlp/workspace.html', {'workingfile': workingfile, 'user': user, 'queryform': queryform, 'processform': processform})


# home page/index


def index(request):
    return render(request, 'nlp/index.html', {})

# it's called test but it's the real deal. change the name sometime if you want
def uploadtest(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            # this binds to form I believe?
            addtext = form.save(commit=False)
            # save to current user!
            addtext.owner = request.user
            # save in DB
            addtext.save()
            textname = addtext.title
            return render(request, 'nlp/upload_success.html', {'textname': textname})
    else:
        form = UploadForm()
    # display form on 'get'
    return render(request, 'nlp/uploadtest.html', {'form': form})


# show user-uploaded texts with a queryset at /mytexts/
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

