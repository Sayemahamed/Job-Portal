from langchain_openai import ChatOpenAI
from state import AgentResponse
from langchain_core.messages import  HumanMessage, AIMessage,AnyMessage
import json
from rich import print

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def invoke_llm(prompt: list[AnyMessage],count:int=0) -> AgentResponse:
    if count > 2:
        raise Exception("Too many attempts to parse response")
    response: AIMessage = llm.invoke(prompt) # type: ignore
    print("""---"""*80)  
    print(prompt)
    print("""---"""*80)
    print(response.content)  
    print("""---"""*80)  
    try:
        response_json = json.loads(str(response.content))
        return AgentResponse.model_validate(response_json)  
    except Exception as e:
        validation_schema: str = json.dumps(AgentResponse.model_json_schema(), indent=2)
        return invoke_llm([
            AIMessage(content=response.content),
            HumanMessage(content=f"Give the previous response as valid JSON response that strictly matches this schema:\n{validation_schema} Give Only JSON , no other text, not even in Markdown")
        ],count=count+1)
