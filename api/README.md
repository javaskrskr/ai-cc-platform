# ai-cc-platform
ai cc platform

# Reference
- https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
- https://pypi.org/project/deep-translator/

# Package Dependencies (Necessary)
- pip install python-dotenv
- pip install flask
- pip install openai
- pip install googletrans==3.1.0a0

# Package Dependencies (If needed)
- pip install openai --upgrade (if needed)
- pip install httpx==0.23.3
- pip install httpcore
- pip install google_trans_new
- pip install -U deep-translator

# ENV on the .env
- OPENAI_API_KEY = "OpenAI_API_KEY"
- DEBUG = "DEBUG"
- SECRET_KEY = "SECRET_KEY"
- UPLOAD_FOLDER = './storage'
- SESSION_PERMANENT = True
- PERMANENT_SESSION_LIFETIME = 300
- SESSION_TYPE = filesystem

# API
- /api/v1/srt/<lang>
lang can be 'zh' or 'en'
