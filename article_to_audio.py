"""
Refer to https://towardsdatascience.com/easy-text-to-speech-with-python-bfb34250036e
"""
from gtts import gTTS
import os
import requests
from bs4 import BeautifulSoup
import random 


def main(URL, audio_file_name):
  text_file_name = "static/articles/" + str(audio_file_name) + ".txt"
  text_file = open(text_file_name, "w")

  #URL = 'https://www.ctvnews.ca/world/trump-fires-u-s-secretary-of-defense-mark-esper-1.5181146'

  page = requests.get(URL)

  soup = BeautifulSoup(page.content, 'html.parser')

  try:
    article_title = soup.select('h1.articleHeadline')[0].text.strip()
  except:
    article_title = soup.select('h1.inner-headline')[0].text.strip()

  author = "CTV"

  paragraphs = soup.find_all('p')

  divs = soup.find_all('div')

  reccomended_articles = []

  def filter_text():
    for reccomended_article in unfiltered_reccomended_articles:
      if len(reccomended_article) > 0:
        reccomended_articles.append(reccomended_article.strip(" "))

  for div in divs:
    try:
      if div.has_attr('class') and div['class'][0] == "sideItems":
          unfiltered_reccomended_articles = div.text.strip("\n ").split("\n")
          filter_text()
      
      elif div.has_attr('class') and div['class'][0] == "content-secondary":
        unfiltered_reccomended_articles = div.text.strip("\n ").split("\n")
        filter_text()

    except:
      pass

  footers = soup.find_all('footer')

  for footer in footers:
    footer_text = footer.text.strip("\n ").split("\n")

  a_links = soup.find_all('a')

  for link in a_links:
      if link.has_attr('class') and link['class'][0] == "bioLink":
          author = link.text

  print("\n\n\n")

  text_file.write(article_title + " \n\nThis article is by: " + author + "\n\n")

  text_file.close()

  text_file = open(text_file_name, "a")

  print("\n\n\n")


  article = []

  #For p and a
  excluded_classes = ["title", "ad-below", "bioLink", "back-top", "newWindow", "socialBio", "contactBio"]


  for paragraph in paragraphs:
      a_test = paragraph.find("a")
      if paragraph.text.strip("\n ") in reccomended_articles:
        pass

      elif paragraph.text in footer_text:
        pass

      elif a_test != None:

          if a_test.has_attr('class') and a_test['class'][0] in excluded_classes:
              pass
          else:
              article.append(paragraph.text)

      elif paragraph.has_attr('class') and paragraph['class'][0] in excluded_classes:
          pass

      elif "SHARE" in paragraph.text:
          pass

      else:
          article.append(paragraph.text)

  for line in article:
      text_file.write(line)

  text_file.close()

  entire_article = open(text_file_name, "r").read()

  language = 'en-ca'

  print("Converting text into audio...")

  speech = gTTS(text = entire_article, lang = language, slow = False)

  print("\nSaving text as an audio file...")

  saved = False
  Attempts = 0
  while saved == False or Attempts == 20:
      try:
          print("Attempt " + str(Attempts))
          Attempts += 1
          speech.save("static/audio/" + str(audio_file_name) + ".mp3")
          saved = True
      except:
          pass


  print("\nThe text has been saved as an audio file called " + str(audio_file_name) + ".mp3")

  #print("\nOpening audio file...")
  #os.system("start " + str(audio_file_name) + ".mp3")
  return str(audio_file_name)

