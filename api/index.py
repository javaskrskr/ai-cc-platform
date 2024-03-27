import os

import httpcore
from datetime import datetime
setattr(httpcore, 'SyncHTTPTransport', 'AsyncHTTPProxy')

import json
import ffmpeg
from openai import OpenAI
from moviepy.editor import *
from googletrans import Translator
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, abort, make_response


app = Flask(__name__)

app.config.from_object('config.DevConfig')

client = OpenAI(api_key=app.config['OPENAI_API_KEY'])

@app.route('/api/v1/srt/<lang>',methods=['POST','GET'])
def srt(lang):
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file_name = file.filename
        filename = secure_filename(file_name)
        print(filename)
        if file and os.path.splitext(file_name)[1] in app.config['UPLOAD_EXTENSIONS']:
            dt_curr = get_curr_time()
            file.save(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'], dt_curr+'_'+filename))
            
            print('file:'+file.filename+' received at'+ dt_curr)
            language = 'zh' if lang == 'zh' else 'en'
            
            store_filename = dt_curr+'_'+filename
            base_store_filename = store_filename.split('.')[0]+'_'+language
            
            upload_folder = os.path.join(app.root_path,app.config.get('UPLOAD_FOLDER'))
            
            mp3_path = upload_folder + '/' + store_filename
            m4a_path = upload_folder + '/' + base_store_filename + '.m4a'
            srt_path = upload_folder + '/' + base_store_filename + '.srt'
            
            print(filename)
            print(mp3_path)
            print(m4a_path)
            print(srt_path)
            print(os.path.join(upload_folder, filename))
            
            

            stream = ffmpeg.input(mp3_path)
            stream = ffmpeg.output(stream, m4a_path)
            ffmpeg.run(stream)
            m4a = open(m4a_path,'rb')
            srt_result = srt_transcription(m4a_file=m4a)
            print('srt ready')
            trans_result = CamelCase(s=srt_result,language=language)
            print('translation ready')
            
            with open(srt_path,'w',encoding='utf-8') as f:
                f.write(trans_result)
            return "srt with translation has been saved to /static folder."
        else:
            return make_response(json.dumps({'error_message': 'file wrong type'}), 413)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept="audio/*">
      <input type=submit value=Upload>
    </form>
    '''
@app.errorhandler(413)
def request_entity_too_large(error):
    return make_response(json.dumps({'error_message': 'file size too large'}), 413)

def get_curr_time():
    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d_%H:%M')
    return date_time

def srt_transcription(m4a_file,language='zh'):
    tran=client.audio.transcriptions.create(
    file=m4a_file,
    model='whisper-1',
    language=language,
    response_format='srt'
    )
    return tran

def CamelCase(s,language='zh'):
    translator = Translator()
    newString = ''
    for word in s.split('\n'):
      check_word=translator.detect(word)
      if(check_word.lang=="zh-CN"):
        translated_ita = translator.translate(word, dest='zh-TW' if language=='zh' else 'en')
        newString = newString + translated_ita.text + '\n'
      else:
         newString = newString + word + '\n'
    return newString

if __name__ == '__main__':
    app.run(debug=True)