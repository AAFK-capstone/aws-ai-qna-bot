## [1.0.0]
- Forked project from QnABot (https://github.com/aws-samples/aws-ai-qna-bot); Please refer to the original project for the project features implemented by the QnA bot team
- Added initial files
- Additional features implemented: 
  - To enable these features, add the corresponding settings in Content Designer
  - For improving Kendra answers:
    - Allows Chatbot to show the source link of the FAQ answer, `ALT_SEARCH_KENDRA_FAQ_SHOW_LINK = true`
    - Allows Chatbot to list Kendra Document search answers (source link only) when Kendra FAQ gives an answer `ALT_SEARCH_KENDRA_FAQ_SHOW_HELPFUL_LINKS = true`
    - Allows Chatbot to provide text responses of matching search keywords, on top of the Kendra Document search answers when Kendra FAQ gives an answer (ALT_SEARCH_KENDRA_FAQ_SHOW_HELPFUL_LINKS must be set to true for this to work), `ALT_SEARCH_KENDRA_FAQ_SHOW_HELPFUL_LINKS_TEXT = true`
    - Shows user-defined Message when FAQ answers are showed with document search answers, `ALT_SEARCH_KENDRA_FAQ_HELPFUL_LINKS_MESSAGE = "YOUR MESSAGE HERE"`
    - Shows user-defined message when answers have been translated with Amazon Translate, `AWS_TRANSLATE_MSG = "Answer dynamically translated by Amazon Translate"`
  - For improving chatbot dialog flow and integrating specialty bots:
    - To allow specialty chatbot to ask main bot for answers if it is unable to find an answer, `FALLBACK_TO_MAIN_BOT_WHEN_ANSWER_NOT_FOUND = true`
    - To get specialty chatbot to autoexit and go back to main bot if it cannot find an answer, `AUTO_EXIT_SPECIALTY_BOT_WHEN_ANSWER_NOT_FOUND = true`
  - For improving data collection and logging:
    - Log custom session attributes, `LOG_CUSTOM_SESSION_ATTRIBUTES = true`
    - Prefix for custom session attributes to be logged - this is required if LOG_CUSTOM_SESSION_ATTRIBUTES is set to true, otherwise no session attributes will be logged; `LOG_CUSTOM_SESSION_ATTRIBUTES_PREFIX = "PREFIX FOR CUSTOM SESSION ATTRIBUTES"`
    
