# Language-Translation-app
Using openAI API's translate text from source to destination language

Steps:
1) Set up virtual environment :
   python -m venv venv

To activate virtual environment for project :
   On Windows -> .\venv\Scripts\activate
   On Linux   -> source venv/bin/activate

2) Install all the packages :
   pip install -r requirements.txt

3) Set API key in .env file :
   OPENAI_API_KEY=sk-proj-***************************************

4) Run app.py file :
   python app.py

5) Access application at http://127.0.0.1:5000

6) For unit testing :(Running application against mock data)
   change directory to tests folder and run pytest command :
   cd tests & pytest         
