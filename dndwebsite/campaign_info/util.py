from django.urls import reverse
import re

# In the given str, replaces each occurence of a word[0] in wordList with a link to the given url, 
# passing in word[1:] as a parameter. wordList is a list of these words (link, params...)
def replaceAllWithUrl(str, wordList, urlType):
    """ Replaces each occurence of every word[0] from wordlist in str, with a link to the given url type, 
        passing world[1] as a paramter """
    linkedText = str
    for word in wordList:
        searchTerm = re.compile('\\b' + re.escape(word[0]) + '\\b', re.IGNORECASE)
        linkedText = re.sub(searchTerm, "<a href='" + reverse(urlType, args=word[1:]) + "'>\g<0> </a>", linkedText)
    return linkedText