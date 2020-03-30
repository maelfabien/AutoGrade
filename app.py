import streamlit as st

from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

st.sidebar.header("Mots clés")
st.sidebar.markdown("Ecrivez les mots clés séparés par une virgule et un espace")
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
	text = ' '.join([stemmer.stem(t) for t in text])

	text = ' '.join([rmv_acc(t) for t in text.split()])
	if list_words != "":
		list_words = list_words.split(", ")
		list_words = [l.lower() for l in list_words]
		count = 0 
		list_in = []

		for word in list_words:

			word = ' '.join([stemmer.stem(w) for w in word.split()])
			word = rmv_acc(word)

			if word in text:
				count += 1
				list_in.append(word)

		return list_in, count
	else:
		return [], 0

key = 0

if st.button('Effacer les réponses'):
    key += 1

st.subheader("Q1")
txt1 = st.text_area("Texte Q1",  value='', key=key)
ret_q1 = return_grade(txt1, w1)


st.write("Mots identifiés: ", ', '.join(ret_q1[0]))
st.write("Points: ", ret_q1[1])

st.subheader("Q2")
txt2 = st.text_area("Texte Q2",  value='', key=key)
ret_q2 = return_grade(txt2, w2)
st.write("Mots identifiés: ", ', '.join(ret_q2[0]))
st.write("Points: ", ret_q2[1])

st.subheader("Q3")
txt3 = st.text_area("Texte Q3",  value='', key=key)
ret_q3 = return_grade(txt3, w3)
st.write("Mots identifiés: ", ', '.join(ret_q3[0]))
st.write("Points: ", ret_q3[1])
