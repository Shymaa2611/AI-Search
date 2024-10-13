import re
import string
from autocorrect import Speller
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

def remove_html_tags(text):
        """
        Removes HTML tags from the given text.
        
        Args:
            text (str): The text from which to remove HTML tags.
        
        Returns:
            str: The text without HTML tags.
        """
        return re.sub(r'<.*?>', ' ', text)

def convert_to_lower(text):
        """
        Converts the given text to lowercase.
        
        Args:
            text (str): The text to convert.
        
        Returns:
            str: The lowercase text.
        """
        return text.lower()

def remove_urls_numbers_punctuation(text):
        """
        Removes URLs, numbers, and punctuation from the given text.
        
        Args:
            text (str): The text to clean.
        
        Returns:
            str: The cleaned text without URLs, numbers, and punctuation.
        """
        punctuation_table = str.maketrans('', '', string.punctuation)
        text = re.sub(r'https?://\S+|www\.\S+|\d+', ' ', text)
        return text.translate(punctuation_table)

def remove_stopwords(text):
        """
        Removes stopwords from the given text.
        
        Args:
            text (str): The text from which to remove stopwords.
        
        Returns:
            str: The text without stopwords.
        """
        stop_words = set(stopwords.words("english"))
        tokens = word_tokenize(text)
        return " ".join(word for word in tokens if word not in stop_words)

def lemmatizing(text):
        """
        Lemmatizes the words in the given text.
        
        Args:
            text (str): The text to lemmatize.
        
        Returns:
            str: The lemmatized text.
        """
        lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(text)
        lemmatized_text = [lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(lemmatized_text)

def spell_check(text):
        """
        Performs spell checking and correction on the given text.
        
        Args:
            text (str): The text to spell check.
        
        Returns:
            str: The corrected text.
        """
        spell_checker = Speller(lang="en")
        tokens = word_tokenize(text)
        corrected_text = [spell_checker(word) for word in tokens]
        return " ".join(corrected_text)

def clean(text):
        """
        Cleans the text by applying various preprocessing steps.
        
        Returns:
            str: The cleaned and processed text.
        """
        without_html_tags = remove_html_tags(text)
        lowercase_text = convert_to_lower(without_html_tags)
        no_urls_numbers_punctuation = remove_urls_numbers_punctuation(lowercase_text)
        without_stopwords = remove_stopwords(no_urls_numbers_punctuation)
        lemmatized_text = lemmatizing(without_stopwords)
        corrected_text = spell_check(lemmatized_text)
        
        return corrected_text


