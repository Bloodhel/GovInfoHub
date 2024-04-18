from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from huggingface_hub import hf_hub_download
from googletrans import Translator

class StreamHandler(BaseCallbackHandler):
    def _init_(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        print(self.text)

def create_chain(system_prompt):
    fine_tuning_data_path = r"C:\Users\kanch\OneDrive\Desktop\ai-chatbot-main\ai-chatbot-main\Government scheme dataset"

    (repo_id, model_file_name) = ("TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                                  "mistral-7b-instruct-v0.1.Q4_0.gguf")

    model_path = hf_hub_download(repo_id=repo_id,
                                 filename=model_file_name,
                                 repo_type="model")

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
    """.format(system_prompt, "{question}")

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm_chain = prompt | llm  # LCEL

    return llm_chain


print("Welcome to GovInfoHGub")

system_prompt = input("System Prompt: ")

llm_chain = create_chain(system_prompt)

print("How may I help you today?")

translator = Translator()

while True:
    user_prompt = input("Your message here: ")

    if user_prompt.lower() == "exit":
        print("Have a nice day!")
        break

    # Translate user's input to English
    translated_prompt = translator.translate(user_prompt, dest='en').text

    # Generate response using the LLM
    response = llm_chain.invoke({"question": translated_prompt})

    # Translate response back to the original language
    translated_response = translator.translate(response, src='en', dest=translator.detect(user_prompt).lang).text

    print(translated_response)
