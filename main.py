"""
By: Donald Lee
Project name: Ardio
Date: November 2020

Refer to 
  - https://repl.it/talk/learn/Flask-Tutorial-Part-1-the-basics/26272
  - https://www.youtube.com/watch?v=Z1RJmh_OqeA
"""
#Imports a python file called "article_to_audio.py"
import article_to_audio
#Imports the following modules
import random, string, concurrent.futures, os
#Imports Flask, a web framework
from flask import Flask, render_template, url_for, request
#Imports a module that allows us to detect the "MissingSchema" error
from requests.exceptions import MissingSchema

#Sets up the flask app
app = Flask(
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

#Sets up the home page
@app.route('/')
def base_page():
  #Renders the "base.html" file (Renders the website) and sends some arguments for the following variables
  return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="none")

#Runs the following when the convert button is pressed, or the user presses the enter key on the form
@app.route('/', methods=['POST'])
def my_form_post():
    #Generates a random number for the name of the file
    audio_file_name = random.randint(1111111,9999999)
    #Attempts the following until an error occurs
    try:
      #Retrieves the URL from the form
      link = request.form['article_link']

      #If "ctv" is not in the link, render the website again, but set the status of "invalid_url_state" to block (Visible)
      if "ctv" not in link:
        return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")

      else:
        #Allows mutiple functions to run concurrently (Ex - If there are 2+ users on the website)
        with concurrent.futures.ThreadPoolExecutor() as executor:
          #Runs the main function from "article_to_audio.py" and set the return varible to "name_of_file"
          name_of_file = executor.submit(article_to_audio.main, link, audio_file_name).result()

          print("I converted a file and named it " + str(name_of_file) + ".mp3")

        #Render the website again, but set the status of "audio_visibility" to block (Visible)
        return render_template('base.html', audio_file_name = str(name_of_file), audio_visibility = "block", loading_status = "none", invalid_url_state="none")
      
    #If the text the user enters is not a valid URL, render the website again, but set the status of "invalid_url_state" to block (Visible)
    except MissingSchema:
      return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")

    #If an error occurs while converting the article, also render the website again, but set the status of "invalid_url_state" to block (Visible)
    except:
      return render_template('base.html', audio_file_name = "", audio_visibility = "none", loading_status = "none", invalid_url_state="block")


if __name__ == "__main__":  #Makes sure this is the main process
	app.run( 
    debug=True,
    #Starts the website
		host='0.0.0.0',  #Sets the host, required for repl to detect the site
		port=random.randint(2000, 9000)  #Randomly select the port the machine hosts on.
	)
