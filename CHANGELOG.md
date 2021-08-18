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

## [1.0.1]
- Experimentation with Kendra Indexing features - Added files and implemented features to automatically scrape a URL for json metadata to automatically index Kendra documents. This is in developmental stage. 
- Files/components added:
  - Frontend integration for the scraper (additional page & APIs)
  - API gateway resources for the backend API endpoint of the scrapers
  - Lambda functions for the scrapers: Three scrapers were created, for scraping AWS content: case-study, blog, and FAQ
- To use this feature, set up a Kendra index first, create the document source and create the bucket and set `DOCUMENT_BUCKETNAME="YOUR_KENDRA_BUCKET"` and `KENDRA_WEB_PAGE_INDEX="KENDRA_INDEX_FOR_YOUR_DOCUMENTS"` in Content Designer 
