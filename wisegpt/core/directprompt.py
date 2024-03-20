from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
# from langchain.chat_models.base import BaseChatModel


def organize_info_from_invoice(extracted_text, openai_api_key):

    prompt = PromptTemplate.from_template(f"""
                Let's think step by step. 
                Your job is to extract these information in html format
                                          
                <b>Total amount</b>:
                <br><b>Customer information:</b>
                <br><b>VIN Number</b>:
                <br><b>Vehicle Information:</b>
                <br><b>Services Performed:</b>
                
                
                from the ONE invoice for ONE customer.  
                Then write the definition of services for non-technical users.
                                          
                {extracted_text}""")

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,openai_api_key=openai_api_key)
    llm_chain = LLMChain(prompt=prompt, llm=chat)
    result = llm_chain.predict()
    return result


    
