from gtts import gTTS
from googletrans import Translator
from flask import Flask, render_template, request
import caption_image

# __name__ == __main__
app = Flask(__name__)

def translate(caption,userlang):
	translator=Translator()
	out=translator.translate(caption,dest=userlang)
	return out.text

def textToAudio(caption,language,pathAudio):
	output=gTTS(text=caption,lang=language)
	output.save(pathAudio)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/', methods= ['POST'])
def predict():
	if request.method == 'POST':

		f = request.files['userfile']
		path = "./static/images/{}".format(f.filename)# ./static/images.jpg
		f.save(path)

		caption = caption_image.caption_this_image(path)
		
		userlang=str(request.form.get("languageSelected"))
		
		pathAudio="./static/audio/apeak{}.mp3".format(f.filename)
		caption=translate(caption,userlang)
		textToAudio(caption,userlang,pathAudio)

		result_dic = {
		'image' : path,
		'audio' : pathAudio,
		'caption' : caption
		}

	return render_template("index.html", your_result =result_dic)

if __name__ == '__main__':
	# app.debug = True
	# due to versions of keras we need to pass another paramter threaded = False to this run function
	app.run(debug = True, threaded = False)
