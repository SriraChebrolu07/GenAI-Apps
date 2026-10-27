from autogen import Agent, Intent

# Define intents
request_chat_history_intent = Intent("request_chat_history", ["Download chat history", "Generate PDF", "Save chat as PDF"])
greeting_intent = Intent("greeting", ["Hi", "Hello", "Hey there"])
farewell_intent = Intent("farewell", ["Goodbye", "Bye", "See you later"])
query_intent = Intent("query", ["Can you show me the chat history?", "How can I save this conversation?"])
confirmation_intent = Intent("confirmation", ["Yes, please generate the PDF", "Sure, download the chat"])
denial_intent = Intent("denial", ["No, don't generate the PDF", "I don't want to download"])
fallback_intent = Intent("fallback", [])

# Define agents
user_agent = Agent("User Agent")
user_agent.add_intent(request_chat_history_intent)
user_agent.add_intent(greeting_intent)
user_agent.add_intent(farewell_intent)
user_agent.add_intent(query_intent)
user_agent.add_intent(confirmation_intent)
user_agent.add_intent(denial_intent)
user_agent.add_intent(fallback_intent)

pdf_generator_agent = Agent("PDF Generator Agent")

# You can define more intents and agents as needed
