"""
By: Donald Lee
Assignment: 7.0
Class: Computer Programming 11
Project name: Ardio
Date: November 4th 2020 - Present

Assignment 7.0:  Self-directed project 

For the final project, you can make a program of your choice. You know how to do a lot now, but depending on what you want to tackle you may need to learn more. You can easily find tutorials on any topic, or you can ask me for suggestions.  

Refer to 
  - https://repl.it/talk/learn/Flask-Tutorial-Part-1-the-basics/26272
  - https://www.youtube.com/watch?v=Z1RJmh_OqeA

"""

import article_to_audio
import random, string, concurrent.futures, os
from flask import Flask, render_template, url_for, request
from requests.exceptions import MissingSchema

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates', #Name of folder containing html files
	static_folder='static'  #Name of folder containing static files
)

# Prevents cache from using the old css file, makes it use the updated one
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
# ^ ^ ^

@app.route('/')  # '/' for the default page
def base_page():
  #Renders the base.html file (Renders the website)
  return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="none")

#Runs the following when the convert button is pressed, or the user presses the enter key on the form
@app.route('/', methods=['POST'])
def my_form_post():
    audio_file_name = random.randint(1111111,9999999)
    try:
      #Retrieves the URL from the form
      text = request.form['article_link']

      if "ctv" not in text:
        return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")

      else:
        #Allows mutiple functions to run concurrently (Ex - If there are 2+ users on the website)
        with concurrent.futures.ThreadPoolExecutor() as executor:
          name_of_file = executor.submit(article_to_audio.main, text, audio_file_name).result()
          print(name_of_file)
          
        return render_template('base.html', audio_file_name = str(name_of_file), audio_visibility = "block", loading_status = "none", invalid_url_state="none")
      
    #If the text the user enters is not a valid URL
    except MissingSchema:
      return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")

    #If an error occurs while converting the article
    except:
      return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( 
    debug=True,
    # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
