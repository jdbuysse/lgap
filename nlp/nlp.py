import spacy
import explacy
import io
from contextlib import redirect_stdout
from spacy.matcher import Matcher
from spacy.tokens import DocBin

# https://docs.djangoproject.com/en/3.0/topics/files/#the-file-object
from django.core.files import File

nlp = spacy.load("en_core_web_sm")


# used for the sentence parser
def read(text):
    doc = nlp(text)
    return doc


# takes f (string rep of file upload) and title in file upload form
def process_uploaded_file(f, title):
    doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE", "POS", "TAG", "HEAD", "DEP"], store_user_data=True)
    # add newlines using spacy's sentence detection
    f = lineizer(f)
    # this assumes a text that has sentences split into new lines
    doclist = f
    for doc in nlp.pipe(doclist):
        print(doc)
        doc_bin.add(doc)
    # for doc in nlp.pipe():
    #      print(doc)
    #      doc_bin.add(doc)
    bytes_data = doc_bin.to_bytes()
    with open(f"media/{title}", "wb") as binary_file:
        binary_file.write(bytes_data)


# read a file from disk
def deserialize_file(title):
    nlp = spacy.blank("en")
    with open(f"media/{title}", "rb") as f:
        data = f.read()
    doc_bin = DocBin().from_bytes(data)
    docs = list(doc_bin.get_docs(nlp.vocab))
    return docs


# make sure selected file is parsed
def check_for_file(title):
    try:
        open(f"media/{title}", "r")
        return 1
    except IOError:
        return 0


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


def makematches(docs, query):
    userlist = query.split(',')
    d = []
    # this is ugly rewrite
    for i in userlist:
        d.append('POS')
    p1 = []
    for i, j in zip(d, userlist):
        p1.append({i: j})
    print(p1)
    matcher = Matcher(nlp.vocab)
    matcher.add("pos", None, p1)
    print(type(docs))
    # how do I re-write this to work on my deserialized data?
    matchlist = ''  # for now matchlist is a STRING
    for doc in docs:
        matches = matcher(doc)
        for match_id, start, end in matches:
            # this could be formatted much more nicely
            # add match count and sequence matched at the top
            span = doc[start:end]  # The matched span
            matchlist += (str(span)).upper()
            matchlist += '\n'
            matchlist += (str(doc))
            matchlist += '\n\n'
    return matchlist

