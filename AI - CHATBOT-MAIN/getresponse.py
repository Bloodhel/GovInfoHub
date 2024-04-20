from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googletrans import Translator
from main import UserPrompt
app = FastAPI()
translator = Translator()

class UserPrompt(BaseModel):
    prompt: str

@app.post("/chatbot")
async def chatbot_endpoint(user_prompt: UserPrompt):
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

# Add CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ASGI application entry point
asgi_application = app
