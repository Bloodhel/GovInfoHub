from fastapi import FastAPI, HTTPException
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from huggingface_hub import hf_hub_download
from googletrans import Translator, LANGUAGES
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class GovInfoHub:
    def __init__(self):
        self.llm_chain = None
        self.system_prompt = "You are a helpful AI assistant who answers questions in short sentences."

    def initialize_llm_chain(self):
        if not self.llm_chain:
            (repo_id, model_file_name) = ("TheBloke/Mistral-7B-Instruct-v0.1-GGUF", "mistral-7b-instruct-v0.1.Q4_0.gguf")
            model_path = hf_hub_download(repo_id=repo_id, filename=model_file_name, repo_type="model")

            llm = LlamaCpp(
                model_path=model_path,
                temperature=0,
                max_tokens=512,
                top_p=1,
                stop=["[INST]"],
                verbose=False,
                streaming=True,
            )
            
            template = """
            <s>[INST]{}[/INST]</s>

            [INST]{}[/INST]
            """.format(self.system_prompt, "{question}")

            prompt = PromptTemplate(template=template, input_variables=["question"])

            self.llm_chain = prompt | llm

    def get_response(self, user_input):
        self.initialize_llm_chain()

        # Detect user input language
        input_lang = self.detect_language(user_input)

        # Translate user input to English
        english_input = self.translate(user_input, src_lang=input_lang, dest_lang='en')

        # Pass English input to AI
        response = self.llm_chain.invoke({"question": english_input})

        # Translate AI response to user input language
        response_lang = LANGUAGES.get(input_lang)
        translated_response = self.translate(response, src_lang='en', dest_lang=response_lang)

        return translated_response

    def translate(self, text, src_lang, dest_lang):
        translator = Translator()
        translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
        return translated_text

    def detect_language(self, text):
        translator = Translator()
        detected_lang = translator.detect(text).lang
        return detected_lang

gov_info_hub = GovInfoHub()

@app.get("/")
async def read_root():
    # Change directory to where main.html resides
    directory = os.path.join(os.path.dirname(__file__), "FRONTEND", "src")
    # Joining path to main.html
    file_path = os.path.join(directory, "main.html")
    # Return main.html file as response
    return FileResponse(file_path)

@app.post("/ask/")
async def ask_question(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="Please provide a question.")

    response = gov_info_hub.get_response(question)

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
