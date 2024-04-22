from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from huggingface_hub import hf_hub_download
from googletrans import Translator, LANGUAGES

def create_chain(system_prompt):
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
    """.format(system_prompt, "{question}")

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm_chain = prompt | llm

    return llm_chain

def translate(text, src_lang, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated_text

def detect_language(text):
    translator = Translator()
    detected_lang = translator.detect(text).lang
    return detected_lang

def main():
    system_prompt = "You are a helpful AI assistant who answers questions in short sentences."
    llm_chain = create_chain(system_prompt)

    print("Welcome to GovInfoHub!")
    print("You can ask questions in any language, and GovInfoHub will respond in the same language.")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit']:
            print("Exiting...")
            break

        # Detect user input language
        input_lang = detect_language(user_input)

        # Translate user input to English
        english_input = translate(user_input, src_lang=input_lang, dest_lang='en')

        # Pass English input to AI
        response = llm_chain.invoke({"question": english_input})

        # Translate AI response to user input language
        response_lang = LANGUAGES.get(input_lang)
        translated_response = translate(response, src_lang='en', dest_lang=response_lang)

        print(f"GovInfoHub ({response_lang}): ", translated_response)

if __name__ == "__main__":
    main()
