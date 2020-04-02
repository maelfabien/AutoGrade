import streamlit as st
import string
from collections import Counter

from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

punc = string.punctuation

with open('css.txt') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

st.sidebar.header("Mots clés")
st.sidebar.markdown(
    "Ecrivez les mots clés, dans leur forme courte, séparés par une virgule et un espace")
st.sidebar.markdown("*Ex: mot1, mot2*")

st.sidebar.markdown("---")
st.sidebar.subheader("Q1")
w1 = st.sidebar.text_input("Mots Q1")

st.sidebar.subheader("Q2")
w2 = st.sidebar.text_input("Mots Q2")

st.sidebar.subheader("Q3")
w3 = st.sidebar.text_input("Mots Q3")

st.header("Notation automatique")
st.write("Collez la réponse de l'élève dans la question appropriée")


def rmv_acc(string_1):

    string_1 = string_1.replace("ç", "c")
    string_1 = string_1.replace("Ç", "C")
    string_1 = string_1.replace("à", "a")
    string_1 = string_1.replace("Ä", "A")
    string_1 = string_1.replace("ä", "a")
    string_1 = string_1.replace("À", "A")
    string_1 = string_1.replace("Â", "A")
    string_1 = string_1.replace("â", "a")
    string_1 = string_1.replace("é", "e")
    string_1 = string_1.replace("è", "e")
    string_1 = string_1.replace("É", "E")
    string_1 = string_1.replace("È", "E")
    string_1 = string_1.replace("Ë", "E")
    string_1 = string_1.replace("ë", "e")
    string_1 = string_1.replace("Ê", "E")
    string_1 = string_1.replace("ê", "e")
    string_1 = string_1.replace("û", "u")
    string_1 = string_1.replace("Û", "U")
    string_1 = string_1.replace("ü", "u")
    string_1 = string_1.replace("Ü", "U")
    string_1 = string_1.replace("ï", "i")
    string_1 = string_1.replace("Ï", "I")
    string_1 = string_1.replace("î", "i")
    string_1 = string_1.replace("Î", "I")
    string_1 = string_1.replace("Ô", "O")
    string_1 = string_1.replace("ô", "o")
    string_1 = string_1.replace("Ö", "O")
    string_1 = string_1.replace("ö", "o")
    string_1 = string_1.replace("Ù", "U")
    string_1 = string_1.replace("ù", "u")

    return string_1


def return_grade(text, list_words):

    text = text.lower()
    text = text.split()
    text = ' '.join([rmv_acc(stemmer.stem(t)) for t in text])
    start = '<div class="entities"> '
    end = ' </div>'
    sent = start + text + end

    if list_words != "":
        list_words = list_words.split(", ")
        list_words = [l.lower() for l in list_words]
        count = 0 
        list_in = []

        for word in list_words:

            word = ' '.join([stemmer.stem(w) for w in word.split()])
            word = rmv_acc(word)

            for w in text.split():

                if word in w:
                    if word not in list_in:
                        count += 1
                        list_in.append(word)
                        sent = sent.replace(word, '<mark data-entity="OK">%s</mark>'%(word))

                else:
                    if 1 - levenshtein(word, w)/(max(len(word), len(w))) >= 0.45:
                        sent = sent.replace(w, '<mark data-entity="NOK">%s</mark>'%(w))

        return list_in, count, sent
    else:
        return [], 0, ""

def call_counter(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    helper.__name__= func.__name__

    return helper

def memoize(func):
    mem = {}
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in mem:
            mem[key] = func(*args, **kwargs)
        return mem[key]
    return memoizer

@call_counter
@memoize    
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    
    res = min([levenshtein(s[:-1], t)+1,
               levenshtein(s, t[:-1])+1, 
               levenshtein(s[:-1], t[:-1]) + cost])

    return res


key = 0

if st.button('Effacer les réponses'):
    key += 1

st.subheader("Q1")
txt1 = st.text_area("Texte Q1",  value='', key=key)
ret_q1 = return_grade(txt1, w1)
st.markdown(ret_q1[2], unsafe_allow_html=True)
st.markdown("***Mots identifiés: ***%s"%(', '.join(ret_q1[0])))
st.write("Points: ", ret_q1[1])


st.subheader("Q2")
txt2 = st.text_area("Texte Q2",  value='', key=key)
ret_q2 = return_grade(txt2, w2)
st.markdown(ret_q2[2], unsafe_allow_html=True)
st.markdown("***Mots identifiés: ***%s"%(', '.join(ret_q2[0])))
st.write("Points: ", ret_q2[1])

st.subheader("Q3")
txt3 = st.text_area("Texte Q3",  value='', key=key)
ret_q3 = return_grade(txt3, w3)
st.markdown(ret_q3[2], unsafe_allow_html=True)
st.markdown("***Mots identifiés: ***%s"%(', '.join(ret_q3[0])))
st.write("Points: ", ret_q3[1])
