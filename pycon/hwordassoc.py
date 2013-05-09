import re
import nltk
from nltk import FreqDist

stopwords_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', \
'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', \
'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', \
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', \
'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', \
'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', \
'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', \
'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', \
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

_badpattern = re.compile(r'\d|\W|_')

def is_noun(tag):
    return tag.startswith('N')

def clean_word(token):
    return not bool(_badpattern.search(token))

def proper_length(word):
    return 2 < len(word) <= 20

def we_like(word, tag):
    return bool(word and clean_word(word) and proper_length(word) and is_noun(tag) and word.lower() not in stopwords_list)

def get_token_tag(tagtuple):
    return tagtuple.split('/') if tagtuple.count('/') == 1 else [None, None]

def mapper(key,value):
    sentence = value.split()
    for (index, tagtuple) in enumerate(sentence):
        token, tag = get_token_tag(tagtuple)
        if we_like(token, tag):
            fd = FreqDist()
            token = token.lower()
            window = sentence[index+1:index+5]
            for windowtuple in window:
                wtoken, wtag = get_token_tag(windowtuple)
                if we_like(wtoken, wtag):
                    wtoken = wtoken.lower()
                    fd.inc(wtoken)
            yield token, tuple(fd.items())
    
def reducer(key,values):
    finalfd = FreqDist()
    for fd in values:
        for k, v in fd:
            finalfd.inc(k, v)
    yield key, tuple(finalfd.items())

if __name__ == "__main__":
    import dumbo
    dumbo.run(mapper,reducer, combiner=reducer)
