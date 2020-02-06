import spacy
import explacy
import io
from contextlib import redirect_stdout
from spacy.matcher import Matcher
# https://docs.djangoproject.com/en/3.0/topics/files/#the-file-object
from django.core.files import File

nlp = spacy.load("en_core_web_sm")

# open a byte doc
# def fileopen():
#     with open('/texts/')

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


# ok  so this version is SLOW: 2:30 to do 'how to write' in full.
# def streamtolist(textsent, query):
#     matcher = Matcher(nlp.vocab)
#     # need to think about how to go from input to this. you can't just send in a string through a form.
#     p1 = [{'POS': 'VERB'}, {'POS': 'ADP'}, {'POS': 'NOUN'}, {'POS': 'PUNCT'}]
#     matcher.add("testing", None, p1)
#     matchlist = []
#     # this part takes way too long. minutes. need to change it to the old streaming version.
#     # my guess is that you're not taking advantage of builtin multithreading etc from spacy if you do line by line nlp()
#     for i in textsent:
#         doc = nlp(i)
#         print(i)
#         matches = matcher(doc)
#         print(matches)
#         for match_id, start, end in matches:
#             string_id = nlp.vocab.strings[match_id]
#             span = doc[start:end]  # The matched span
#             print(string_id, ': ', span.text)
#             sentence = doc[start].sent.text
#             matchlist.append(sentence)
#     return matchlist

# full pipeline: 1:20
# with 'ner' disabled: :53 (weirdly, about the same runtime for HtW and P and P)
# with the current version of pattern matching, you can only disable NER (not sure what that does to accuracy)
def streamtolist(textsent, query):
    matcher = Matcher(nlp.vocab)
    # need to think about how to go get input. you can't just have a user input a list of tuples through a form.
    p1 = [{'POS': 'PRON'}, {'POS': 'VERB'}, {'POS': 'DET'}, {'POS': 'NOUN'}, {'POS': 'ADV'}, {'POS': 'VERB'}]
    matcher.add("testing", None, p1)
    matchlist = []
    # nlp.disable_pipes('parser', 'ner')
    for doc in nlp.pipe(textsent, disable=["ner"]):
        matches = matcher(doc)
        print(matches)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]  # The matched span
            print(string_id, ': ', span.text)
            sentence = doc[start].sent.text
            matchlist.append(sentence)
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
