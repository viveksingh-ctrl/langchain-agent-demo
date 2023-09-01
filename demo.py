from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import load_tools
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os 
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import Tool 
from langchain.chains import SimpleSequentialChain
import requests
import json 
import configs 

os.environ['OPENAI_API_KEY'] = configs.OPEN_API_KEY


template = '''
Identify and fill the following key-value pairs given below from the statement 
{crud}
'''

prompt = PromptTemplate(
    input_variables=["crud"],
    template=template,
)
llm = ChatOpenAI(temperature=0) 


def api_call_to_cstack(data):

    url = "https://api.contentstack.io/v3/content_types/sample_content_type/entries"

    payload = json.dumps({
    "entry": {
        "title": data['title'], 
        "multi_line" : data['content']
    }
    })
    headers = {
    'api_key': configs.API_KEY,
    'authorization': configs.MANAGEMENT_TOKEN,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

def create_entry(args):
    
    data = json.loads(args)
    if "org_id" not in data:
        data['org_id'] = input("Please enter the org_id : ")
        print()

    if "content" not in data:
        data['content'] = input("Please paste the content here : ")
        print()

    if "title" not in data:
        data['title'] = input("Suggest an appropriate title for your entry ? if you don't want we can summarize it for you :")
        print()

    api_call_to_cstack(data)



def update_entry():
    print('something is updated')
    pass 

def delete_entry():
    print('entry deleted with some uid')
    pass 



tools = [
    Tool(
        name = "create", 
        func = create_entry, 
        description='''useful for creating an entry and try to get everything in a key value json pair'''
    ),
    Tool(
        name = "update", 
        func = update_entry, 
        description='''useful for updating an existing entry and try to get everything in a key value json pair'''
    ),
    Tool(
        name = "delete", 
        func = delete_entry, 
        description='''useful for deleting an existing entry and try to get everything in a key value json pair'''
    )
]
crud = input("AGENT :")
crud = "I want to create an entry with language set to Portuguese and consider content model to be 'sample_content_type' and authtoken as cs76cad007525f99546b0b1010"
agent = initialize_agent(tools = tools, llm = llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
print(agent.run(crud))

