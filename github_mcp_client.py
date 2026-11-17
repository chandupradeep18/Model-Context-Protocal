import asyncio,os,json
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
load_dotenv()
groq_client=ChatGroq(model='qwen/qwen3.8-27b')
nvidia_client=ChatNVIDIA(model="nvidia/nemotron-3.5-lightning-30b-a3b")
client=MultiServerMCPClient({
    "client":{
        'transport':"streamable_http",
        'url':'https://api.githubcopilot.com/mcp/',
        "headers":{
            "Authorization":f"Bearer {os.environ['GITHUB_API']}"
        }
    }
})
async def call_a_tool(tool,args):
    response=await tool.ainvoke(args)
    text=response[0]['text']
    try:
        text=json.loads(text)
    except json.JSONDecodeError:
        pass
    return text

async def main():
    tools=await client.get_tools()
    tools_call_by_name={}
    for tool in tools:
        tools_call_by_name[tool.name]=tool

    response=await call_a_tool(tools_call_by_name['get_me'],{})
    print(response)

    create_repo=await call_a_tool(tools_call_by_name['create_repository'],{
        'name':'Model Context Protocal',
        'descriptions':'How to Create Mcp Server Using Stdio and Streamable-Http Along With Mcp Client to Comsume The Mcp Server',
        'private':False,
        'autoInit':True
    })
    print(create_repo)
if __name__=="__main__":
    asyncio.run(main())
