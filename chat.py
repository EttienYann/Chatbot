import nltk
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
nltk.data.path.append(os.path.expanduser('~/.nltk_data'))
# Télécharger des ressources nécessaires de nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')    

# Charger le fichier texte et prétraiter les données
file_path = 'ww2.txt'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().replace('\n', ' ')
except FileNotFoundError:
    st.error(f"Le fichier '{file_path}' est introuvable. Veuillez vérifier le chemin.")
    st.stop()
except Exception as e:
    st.error(f"Une erreur est survenue lors de l'ouverture du fichier : {e}")
    st.stop()

# Tokeniser le texte en phrases
sentences = sent_tokenize(data)

# Définir une fonction pour prétraiter chaque phrase
def preprocess(sentence):
    # Tokeniser la phrase en mots
    words = word_tokenize(sentence)
    # Supprimer les stopwords et la ponctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    # Lemmatiser les mots
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Prétraiter chaque phrase dans le texte
corpus = [preprocess(sentence) for sentence in sentences]

# Définir une fonction pour trouver la phrase la plus pertinente en fonction d'une requête
def get_most_relevant_sentence(query):
    # Prétraiter la requête
    query = preprocess(query)
    # Calculer la similarité entre la requête et chaque phrase du texte
    max_similarity = 0
    most_relevant_sentence = ""
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence

# Définir la fonction du chatbot
def chatbot(question):
    # Vérifier si la question est une salutation
    greetings = ["bonjour", "salut", "hello", "hi"]
    if any(greeting in question.lower() for greeting in greetings):
        return "Bonjour! Comment puis-je vous aider aujourd'hui?"

    # Trouver la phrase la plus pertinente
    most_relevant_sentence = get_most_relevant_sentence(question)
    # Retourner la réponse
    return most_relevant_sentence

# Créer une application Streamlit
def main():
    st.title("Chatbot")
    st.write("Bonjour! Je suis un chatbot. Posez-moi une question sur le sujet du fichier texte.")
    # Obtenir la question de l'utilisateur
    question = st.text_input("Vous :")
    # Créer un bouton pour soumettre la question
    if st.button("Soumettre"):
        # Appeler la fonction du chatbot avec la question et afficher la réponse
        response = chatbot(question)
        st.write("Chatbot : " + response)

# Exécuter l'application
if __name__ == "__main__":
    main()
