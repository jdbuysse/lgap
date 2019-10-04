import spacy
import explacy
import io
from contextlib import redirect_stdout


nlp = spacy.load("en_core_web_sm")


def read(text):
    doc = nlp(text)
    return doc


# if the text is short enough you can just make it into a doc rather than stream it. the number
# is arbitrary right now pending testing
def safedoc(text):
    if len(text) < 1000:
        doc = nlp.read(text)
        return doc
    else:
        # stream the doc instead or put it into a pd dataframe or something
        return False







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



