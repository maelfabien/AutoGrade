import streamlit as st
#import SessionState

#state = SessionState.get(key=0)

#ta_placeholder = st.empty()

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

def return_grade(text, list_words):
	text = text.lower()
	if list_words != "":
		list_words = list_words.split(", ")
		list_words = [l.lower() for l in list_words]
		count = 0 
		list_in = []

		for word in list_words:
			if word in text:
				if all(w in text.split() for w in word.split()):
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
txt3 = st.text_area("Texte Q3",  value='')
ret_q3 = return_grade(txt3, w3)
st.write("Mots identifiés: ", ', '.join(ret_q3[0]), key=key)
st.write("Points: ", ret_q3[1])
