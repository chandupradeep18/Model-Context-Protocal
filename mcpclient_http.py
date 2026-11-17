from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.shared.context import RequestContext
from pathlib import Path
import sys
Server_path=Path(__file__).parent/"mcpserver_stdio.py"
import asyncio
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage
from dotenv import load_dotenv
load_dotenv()

groq_client=ChatGroq(model='qwen/qwen3.8-27b')
nvidia_client=ChatNVIDIA(model="nvidia/nemotron-3.5-lightning-30b-a3b")
groq=init_chat_model(model='qwen/qwen3.8-27b',model_provider='groq')

client=MultiServerMCPClient({
    "client":{
        'transport':"streamable_http",
        'url':'http://127.0.0.1:8000/mcp'
    },
    "client2":{
            'transport':'stdio',
            'command':sys.executable,
            'args':[str(Server_path)]
        },
})

async def main():
    tools=await client.get_tools()
    tools_by_name={}
    for tool in tools:
        tools_by_name[tool.name]=tool
    groq_llm=groq_client.bind_tools(list(tools))
    history=[]
    while True:
        user=input("Ask a Question : ")
        if not user or user.strip()=="bye":
            print("Chat Ended")
            break
        history.append(HumanMessage(content=user))
        response=groq_llm.invoke(history)
        history.append(AIMessage(content=response.content,tool_call=response.tool_calls))
        #while response.tool_calls:
        for tool_call in response.tool_calls:
            tool=tools_by_name[tool_call['name']]
            tool_response=await tool.ainvoke(tool_call['args'])
            history.append(ToolMessage(content=tool_response,tool_call_id=tool_call['id'],name=tool_call['name']))
        response =await groq_llm.ainvoke(history)
        history.append(response)
        print("AI :",response.content)

if __name__=="__main__":
    asyncio.run(main())