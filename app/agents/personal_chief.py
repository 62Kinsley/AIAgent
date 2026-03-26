from dotenv import load_dotenv
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
import os
import sqlite3

load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
# GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

#tool
search = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_SEARCH_API_KEY"),
    google_cse_id=os.getenv("GOOGLE_SEARCH_ENGINE_ID")
)
web_search = Tool(
    name="web_search",
    func=search.run,
    description="Search for recipes and cooking-related information on the web",
)

#model
multimodal_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

#storage
# checkpointer = SqliteSaver(sqlite3.connect("resources/personal_chief.db", check_same_thread=False))
# checkpointer.setup()


#intial agent
system_prompt = """ 
You are a personal chef. The user will give you a list of ingredients they have at home, or a photo of ingredients. Your workflow is as follows:
- If the user provides a photo, first analyze the ingredients in the photo, identify usable ingredients based on freshness and quantity.
- Prioritize using the web_search tool to search for recipes that can be made with the available ingredients. If no suitable recipes are found, provide 3-5 creative combination suggestions.
- Rate each recipe on nutritional value and difficulty, then rank them overall.
- Return the ranked recipe suggestions and instructions to the user.
"""

agent = create_react_agent(
    model=multimodal_model,
    tools=[web_search],
    # checkpointer=checkpointer,
    prompt=system_prompt,         
)

