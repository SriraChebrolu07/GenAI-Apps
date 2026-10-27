# Getting Started:
# AutoGen is a framework that enables development of LLM applications using multiple agents that can converse with each other to solve tasks. 
# AutoGen agents are customizable, conversable, and seamlessly allow human participation. 
# They can operate in various modes that employ combinations of LLMs, human inputs, and tools.

# AutoGen Overview

# Main Features:

# AutoGen enables building next-gen LLM applications based on multi-agent conversations with minimal effort. 

# It simplifies the orchestration, automation, and optimization of a complex LLM workflow. It maximizes the performance of LLM models
# and overcomes their weaknesses.

# It supports diverse conversation patterns for complex workflows. 

# With customizable and conversable agents, developers can use AutoGen to build a wide range of conversation patterns concerning conversation autonomy, the number of agents, and agent conversation topology.
# It provides a collection of working systems with different complexities. 

# These systems span a wide range of applications from various domains and complexities. This demonstrates how AutoGen can easily support diverse conversation patterns.
# AutoGen is powered by collaborative research studies from Microsoft, Penn State University, and University of Washington.

# pip install pyautogen

from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about NVDA and TESLA stock prices.",
)





# What is Autogen?
# Autogen is an open-source tool from Microsoft to build robust multi-agent applications. 
# Designed from the ground up, keeping multiple-agent communication in mind. 
# It lets us create LLM applications where multiple agents converse with each other to find solutions to provided problems. 
# The agents are highly customizable, meaning we can guide them to perform specific tasks. 
# It also integrates well with the Langchain tooling ecosystem, which means we leverage existing Langchain tools to augment our agents.