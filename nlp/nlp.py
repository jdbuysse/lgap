import spacy
import explacy
import io
from contextlib import redirect_stdout
from spacy.matcher import Matcher
from spacy.tokens import DocBin

# https://docs.djangoproject.com/en/3.0/topics/files/#the-file-object
from django.core.files import File

nlp = spacy.load("en_core_web_sm")



# takes f (string rep of file upload) and title in file upload form
def process_uploaded_file(f, title):
    print(f)
    print(title)
    print(type(f.splitlines()))
    # doc = nlp(f) on desktop at least, this will run somehow
    # rewrite to have this pass through lineizer() later on
    doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE", "POS", "TAG", "HEAD", "DEP"], store_user_data=True)
    # some code if it ends up being better to make a list
    doclist = f.splitlines()
    for doc in nlp.pipe(doclist):
        print(doc)
        doc_bin.add(doc)
    # for doc in nlp.pipe():
    #      print(doc)
    #      doc_bin.add(doc)
    bytes_data = doc_bin.to_bytes()
    with open(f"media/{title}", "wb") as binary_file:
        binary_file.write(bytes_data)

# I haven't tested this out yet, copied from working file
# have to think about how to keep that 'title' variable available
def deserialize_file(title):
    print(title)
    nlp = spacy.blank("en")
    with open(f"media/{title}", "rb") as f:
        data = f.read()
    doc_bin = DocBin().from_bytes(data)
    docs = list(doc_bin.get_docs(nlp.vocab))
    return docs

def read(text):
    doc = nlp(text)
    return doc


# Format is pattern-match friendly. Takes a DOC now
# which is different from the original formula.
def posmatch(doc):
    types = []  # type of match token, first item in dict
    values = []  # value of matched token, second item in dict
    for token in doc:
        types.append('POS')
        values.append(token.pos_)
    # use list comprehension to put them together
    matchpattern = [{k: v} for k, v in zip(types, values)]
    return matchpattern


# Format is pattern-match friendly. Takes a DOC now
def depmatch(doc):
    types = []  # type of match token, first item in dict
    values = []  # value of matched token, second item in dict
    for token in doc:
        types.append('DEP')
        values.append(token.dep_)
    # use list comprehension to put them together
    matchpattern = [{k: v} for k, v in zip(types, values)]
    return matchpattern


# The visualizer takes a TEXT (string) not a doc
def visualize(text):
    # Because the visualizer is built to run on stdout, you grab that output here
    f = io.StringIO()
    with redirect_stdout(f):
        explacy.print_parse_info(nlp, text)
    out = f.getvalue()
    print(out)
    return out


# This processes the text into a list of sentences and returns that list
# counting from the first print statement of the matcher function, this seems to take about 7-9 seconds
def lineizer(text):
    # the sentencizer is a pre-built spacy thing
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    with nlp.disable_pipes('tagger', 'parser', 'ner'):
        doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]  # I assume there's a way to combine these
    sentences = [w.replace('\n', ' ') for w in sentences]
    # sentences is a list right now. if you want to turn it back into a string uncomment next line
    # sentences = '\n'.join(sentences)
    # remove sentencizer before you call nlp() again
    nlp.remove_pipe('sentencizer')
    return sentences


# full pipeline: 1:20
# with 'ner' disabled: :53 (weirdly, about the same runtime for HtW and P and P)
# with the current version of pattern matching, you can only disable NER (not sure what that does to accuracy)
def streamtolist(textsent, query):
    # nq = query_constructor(query)
    matcher = Matcher(nlp.vocab)
    # need to think about how to go get input. you can't just have a user input a list of tuples through a form.
    #matcher.add("testing", None, nq)
    matchlist = []
    # nlp.disable_pipes('parser', 'ner')
    # for doc in nlp.pipe(textsent, disable=["ner"]):
    #     matches = matcher(doc)
    #     print(matches)
    #     for match_id, start, end in matches:
    #         string_id = nlp.vocab.strings[match_id]
    #         span = doc[start:end]  # The matched span
    #         print(string_id, ': ', span.text)
    #         sentence = doc[start].sent.text
    #         matchlist.append(sentence)
    return matchlist


# if the text is short enough you can just make it into a doc rather than stream it. the number
# is arbitrary right now pending testing
# def safedoc(text):
#     if len(text) < 1000:
#         doc = nlp.read(text)
#         return doc
#     else:
#         # stream the doc instead or put it into a pd dataframe or something
#         return False
