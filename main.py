"""
By: Donald Lee


Refer to 
https://repl.it/talk/learn/Flask-Tutorial-Part-1-the-basics/26272
https://www.youtube.com/watch?v=Z1RJmh_OqeA
"""


import article_to_audio
from flask import Flask, render_template, url_for, request
import random, string, concurrent.futures, os

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

#Prevents cache from using the old css file, makes it use the updated one
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
  return render_template('base.html', audio_file_name = "", Wait="", audio_visibility = "none", loading_status = "none")

@app.route('/', methods=['POST'])
def my_form_post():
    try:
      text = request.form['article_link']
      name_of_file = article_to_audio.main(text)

      with concurrent.futures.ThreadPoolExecutor() as executor:
        name_of_file = executor.submit(article_to_audio.main, text).result()
        print(name_of_file)
        
      return render_template('base.html', audio_file_name = str(name_of_file), Wait="Your article has been converted into mp3!", audio_visibility = "block", loading_status = "none")
      
    except:
      return render_template('base.html', audio_file_name = "", Wait="", audio_visibility = "none", loading_status = "none")
   

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( 
    debug=True,
    # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
