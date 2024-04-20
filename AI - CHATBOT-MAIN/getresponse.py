from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
from  main import UserPrompt
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
asgi_application = app
translator = Translator()

class UserPrompt(BaseModel):
    prompt: str

@app.post("/chatbot")
def chatbot_endpoint(user_prompt: UserPrompt):
    try:
        # Translate user's input to English
        translated_prompt = translator.translate(user_prompt.prompt, dest='en').text

        # Generate response using the LLM
        response = llm_chain.invoke({"question": translated_prompt})

        # Translate response back to the original language
        detected_lang = translator.detect(user_prompt.prompt).lang
        translated_response = translator.translate(response, src='en', dest=detected_lang).text

        return {"response": translated_response}
    except Exception as e:
        # Handle translation errors
        error_message = f"Translation error: {str(e)}"
        return {"response": error_message}
