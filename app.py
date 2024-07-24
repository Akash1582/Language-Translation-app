import logging 
from flask import Flask, request, render_template, jsonify 
from dotenv import load_dotenv 
import os 
import openai 

app = Flask(__name__) 

# Load environment variables from .env 
load_dotenv() 

# Initialize OpenAI API client 
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Set up logging 
logging.basicConfig(level=logging.DEBUG)   

# Translation function using OpenAI GPT-4 
def translate_text(source_text, source_lang, target_lang, formality, domain): 
    prompt = f"Translate from {source_lang} to {target_lang}:\n\nSource Text: {source_text}\n\nFormality: {formality}\n\nDomain: {domain}\n\nTranslated:" 
    try: 
        logging.debug(f"API Request Prompt: {prompt}") 
        response = openai.Client().completions.create( 
            model="gpt-3.5-turbo-instruct", 
            prompt=prompt, 
            max_tokens=100, 
            #stop=["\n", ""] 
        ) 

        logging.debug(f"API Response: {response}") 
        translated_text = response.choices[0].text.strip() 
        logging.debug(f"Translated Text: {translated_text}") 
        return translated_text 

    except openai.OpenAIError as e: 
        logging.error(f"OpenAIError: {e}") 
        return f"Translation Error: {str(e)}" 

    except Exception as e: 
        logging.error(f"Unexpected error: {e}") 
        return f"Unexpected error: {str(e)}" 

@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/translate', methods=['POST']) 
def translate(): 
    try: 
        source_text = request.form['source_text'] 
        source_lang = request.form['source_lang'] 
        target_lang = request.form['target_lang'] 
        formality = request.form['formality'] 
        domain = request.form['domain'] 

        translated_text = translate_text(source_text, source_lang, target_lang, formality, domain) 
        logging.debug(f"Translated Text from translate function: {translated_text}") 

        return render_template('index.html', translated_text=translated_text) 

    except KeyError as e: 
        logging.error(f"KeyError: {e}") 
        return jsonify({'error': 'Missing form data'}), 400 

    except Exception as e: 
        logging.error(f"Unexpected error: {e}") 
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500 

# Custom error handler for 404 Not Found errors 
@app.errorhandler(404) 
def page_not_found(error): 
    return render_template('404.html'), 404 

if __name__ == '__main__': 
    app.run(debug=True) 