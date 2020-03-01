this is the user-auth-enabled version of the lgap site, if I choose to go that route.

1. requires django
2. requires spacy, plus pre-trained model: use 'python -m spacy download en'


coverage ref:
>coverage run manage.py test
>coverage html
and then open index in htmlcov/
