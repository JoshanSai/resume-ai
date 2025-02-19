import os
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from resume_builder import Resume
from tools import PersonalInformation, ProfessionalSummaryTool, ExperienceTool, EducationTool, SkillsTool, ProjectsTool

load_dotenv()


def talkToAgent(session_id: str, query: str):
    llm = AzureChatOpenAI(
        deployment_name="gpt-4o",
        azure_endpoint=os.getenv('AZURE_ENDPOINT'),
        openai_api_version="2023-07-01-preview",
        openai_api_key=os.getenv('AZURE_API_KEY'))
    resume_object = Resume()
    tools = [PersonalInformation(resume=resume_object),
             ProfessionalSummaryTool(resume=resume_object),
             ExperienceTool(resume=resume_object),
             EducationTool(resume=resume_object),
             SkillsTool(resume=resume_object),
             ProjectsTool(resume=resume_object)]

    redis_chat = RedisChatMessageHistory(session_id=session_id,
                                         url=os.getenv('REDIS_URL'))

    memory = ConversationBufferWindowMemory(chat_memory=redis_chat, k=10, return_messages=True,
                                            memory_key="chat_history",
                                            output_key="output")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)

    res = agent_executor.invoke({"input": query})
    return {"response": res['output'], "resume_data": resume_object.resume_data}
