from src.llm import get_context, get_me_result
# user_query = input('user :')
# user_query = "how to integrate Jira on zluri"
# user_query = "how to get Beta Integration Access on zluri" # <----
# user_query = "what roles or access levels are supported by Zluri"
# user_query = "What is Zluri Desktop Agents and how it works?"
user_query = "can i integrate Jira on zluri if so how ?"
context = get_context(user_query)
# print(context)
print(get_me_result(user_query, context))