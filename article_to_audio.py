"""
Refer to https://towardsdatascience.com/easy-text-to-speech-with-python-bfb34250036e
"""
#Imports the following modules used in this function
import os, requests, random 
#Imports the Google Text to Speak module, which converts text into an mp3 file
from gtts import gTTS
#Imports a module for web scrapping =
from bs4 import BeautifulSoup

#A function that converts the article into an mp3 file
def main(URL, audio_file_name):
  #Goes to the following URL
  page = requests.get(URL)

  #Gets the website's HTML code
  soup = BeautifulSoup(page.content, 'html.parser')

  #CTV currently has a current and beta website, the current website headline has a class called "articleHeadline", but if an error occurs while trying to get the headline, it runs the code to get it from the class called "inner-headline"
  try:
    #Gets the article's heading from CTV's current website
    article_title = soup.select('h1.articleHeadline')[0].text.strip(" ")
  except:
    #Gets the article's heading from CTV's beta website
    article_title = soup.select('h1.inner-headline')[0].text.strip(" ")

  #Initalizes the name of the author incase it is not specified 
  author = "CTV"

  #Gets all the div, p, a, span, and footer tags from the HTML code
  divs = soup.find_all('div')
  paragraphs = soup.find_all('p')
  a_links = soup.find_all('a')
  spans = soup.find_all('span')
  footers = soup.find_all('footer')

  #Initalizes a list that will contain all the reccomended articles
  reccomended_articles = []

  #A function that add non empty list items from "unfiltered_reccomended_articles" to "reccomended_articles"
  def filter_text():
    for reccomended_article in unfiltered_reccomended_articles:
      if len(reccomended_article) > 0:
        #Removes additional spaces and adds that item to the list called "reccomended_articles"
        reccomended_articles.append(reccomended_article.strip(" "))

  #For each div element in the HTML code, run the following
  for div in divs:
    try:
      #If the div has a class called "sideItems", remove unnecessary new lines, and split it into a list
      if div.has_attr('class') and div['class'][0] == "sideItems":
          unfiltered_reccomended_articles = div.text.strip("\n ").split("\n")
          #Runs a function called "filter_text"
          filter_text()

      #Else if the div has a class called "content-secondary", remove unnecessary new lines, and split it into a list
      elif div.has_attr('class') and div['class'][0] == "content-secondary":
        unfiltered_reccomended_articles = div.text.strip("\n ").split("\n")
        filter_text()

    #If an error occurs, ignore it
    except:
      pass

  for footer in footers:
    #Gets the text in the footer, remove unnecessary new lines, and split it into a list
    footer_text = footer.text.strip("\n ").split("\n")

  #Loops through all the hyperlinks in the website
  for link in a_links:
      #If the hyperlink has a class called "bioLink", set the variable "author" to the link text
      if link.has_attr('class') and link['class'][0] == "bioLink":
          author = link.text
  
  #Loops through all the span tags in the website
  for span in spans:
    #If the span has a class called "bold", set the variable "author" to the span text
    if span.has_attr('class') and span['class'][0] == "bold":
      author = span.text

  #Initalizes a list that will contain the contents of the article being web scrapped 
  article = []

  #A list that contains p and a tag classes that will be excluded from the audio file (These classes generally contain off-topic content)
  excluded_classes = ["title", "ad-below", "bioLink", "back-top", "newWindow", "socialBio", "contactBio", "socialShareLabel"]

  #Loops through each paragraph in the article
  for paragraph in paragraphs:
      #Gets all the hyperlinks in the paragraph
      paragraph_a_links = paragraph.find("a")

      #If the paragraph text is in the reccomended_articles or footer_text, ignore it
      if paragraph.text.strip("\n ") in reccomended_articles or paragraph.text.strip("\n ") in footer_text:
        pass

      #If a paragraph has a hyperlink, and the hyperlink's class is in the list called "excluded_classes", ignore it
      elif paragraph_a_links != None:
          if paragraph_a_links.has_attr('class') and paragraph_a_links['class'][0] in excluded_classes:
              pass
            
          else:
            #Else, add that paragraph to a list called "article"
              article.append(paragraph.text)

      #If the paragraph has a class in the list called "excluded_classes", ignore it
      elif paragraph.has_attr('class') and paragraph['class'][0] in excluded_classes:
          pass

      #If the word "SHARE" is in a paragraph, ignore it
      elif "SHARE" in paragraph.text:
          pass

      #Else, add that paragraph into a list called "article"
      else:
          article.append(paragraph.text)

  #Adds the article title, author, and combine all the article paragraphs from the list called "article" into a variable called "the_article"
  the_article = article_title + " \n\nThis article is by: " + author + "\n\n" + '\n'.join(article)

  #Sets the language and accent of the voice reading the mp3 file
  language = 'en-ca'

  print("Converting text into audio...")
  #Convert "the_article" into an mp3 file
  speech = gTTS(text = the_article, lang = language, slow = False)
  print("\nSaving text as an audio file...")
  speech.save("static/audio/" + str(audio_file_name) + ".mp3")
  print("\nThe text has been saved as an audio file called " + str(audio_file_name) + ".mp3")
  #Returns the name of the mp3 file
  return str(audio_file_name)
