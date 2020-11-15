"""
Refer to https://towardsdatascience.com/easy-text-to-speech-with-python-bfb34250036e
"""

import os, requests, random 
from gtts import gTTS
from bs4 import BeautifulSoup

#A function that converts the article into an mp3 file
def main(URL, audio_file_name):
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
  
  spans = soup.find_all('span')
  for span in spans:
    if span.has_attr('class') and span['class'][0] == "bold":
      author = span.text

  article = []

  #For p and a
  excluded_classes = ["title", "ad-below", "bioLink", "back-top", "newWindow", "socialBio", "contactBio", "socialShareLabel"]


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

  the_article = article_title + " \n\nThis article is by: " + author + "\n\n" + '\n'.join(article)

  #Sets the language and accent of the voice reading the mp3 file
  language = 'en-ca'

  print("Converting text into audio...")
  
  speech = gTTS(text = the_article, lang = language, slow = False)

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

  return str(audio_file_name)

