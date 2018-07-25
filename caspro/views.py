from decimal import Decimal

from django.shortcuts import render

from cass.Crewer import Crewer
from cass.analysis import analysis
from cass.predict import *

def index(request):
    return render(request, "index.html")


def ana(request):
    url = request.GET["target_url"]
    res = analysis(url)
    score = str(float(res[0]) * 100)
    score = Decimal(score).quantize(Decimal('0.00'))
    keywords = json.dumps(res[1])
    print(res[1])
    print(keywords)
    return render(request, "conclution.html", {'score': score, 'keywords': keywords})
    # return render(request, "conclution.html", {'score': score, 'key1': keywords[0], 'key2': keywords[1], 'key3': keywords[2], 'key4': keywords[3], 'key5': keywords[4], 'key6': keywords[5], 'key7': keywords[6], 'key8': keywords[7], 'key9': keywords[8], 'key10': keywords[9]})
