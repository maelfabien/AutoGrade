import streamlit as st
import string
from collections import Counter

from nltk.stem.porter import *
stemmer = PorterStemmer()

punc = string.punctuation

with open('css.txt') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

st.sidebar.header("Key words")
st.sidebar.markdown(
    "Write the keywords you are looking for. Split them by a comma.")
st.sidebar.markdown("*Eg: word1, word2, word3*")

w1 = st.sidebar.text_input("Words you're looking for?")

st.header("Where's the word? Automatic grading")

st.markdown("Paste your text in the text area below. The application will look for words sharing similar roots or that are close. Words matching are in orange, words not matching but quite similar are in purple. A matching score is then displayed")

st.sidebar.markdown("---")
st.sidebar.subheader("What is it?")
st.sidebar.markdown("This tool is meant for teachers who want to automatically detect keywords in a text written by their students (typically remote school work duing the COVID-19 crisis).")
st.sidebar.markdown("At the end, a 'score' is proposed. It shows how many of the words you were looking for found a match, e.g. if you were looking for 5 words and it found 4, the score will be 4.")

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
    text2 = text

    text = text.split()
    text = ' '.join([rmv_acc(stemmer.stem(t)) for t in text])
    start = '<div class="entities"> '
    end = ' </div>'
    sent = start + text2 + end

    if list_words != "":
        list_words = list_words.split(", ")
        list_words = [l.lower() for l in list_words]
        count = 0 
        list_in = []

        for word in list_words:

            word = rmv_acc(word)

            if word in text2:
                if word not in list_in:
                    sent = sent.replace(word, ' <mark entity="OK">%s</mark> '%(word))
                    count += 1

                    list_in.append(' '.join([stemmer.stem(w) for w in word.split()]))

            else:
                word = ' '.join([stemmer.stem(w) for w in word.split()])
                k = 0

                for w in text.split():

                    if word in w:
                        if word not in list_in:
                            count += 1

                            list_in.append(' '.join([stemmer.stem(w) for w in word.split()])) #text2.split()[k])
                            sent = sent.replace(text2.split()[k], ' <mark entity="OK">%s</mark> '%(text2.split()[k]))

                    else:
                        if 1 - levenshtein(word, w)/(max(len(word), len(w))) >= 0.6:
                            
                            sent = sent.replace(text2.split()[k], ' <mark entity="NOK">%s</mark> '%(text2.split()[k]))
                    k+=1

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

if st.button('Erase answer'):
    key += 1

st.subheader("Answer")
txt1 = st.text_area("Paste answer here",  value='', key=key)
ret_q1 = return_grade(txt1, w1)
st.markdown(ret_q1[2], unsafe_allow_html=True)
st.markdown("***Words identified: ***%s"%(', '.join(ret_q1[0])))
st.write("Points: ", ret_q1[1])
