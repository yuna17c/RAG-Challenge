from django.shortcuts import render
from .forms import MyForm
import cohere
from openai import OpenAI
from multiprocessing import Process

co = cohere.Client('TheBPPLGT2MfubkoO4tUSXUKGnuOYHh6czpk8Lle')

returnDict = {}

def getCitations(string):
    response = co.chat(
        message = string,
        connectors = [{"id": "web-search"}], 
        prompt_truncation="AUTO"
    )
    docs_used = [citation['document_ids'] for citation in response.citations]
    docs_used = [item for sublist in docs_used for item in sublist]
    matched_urls = [doc['url'] for doc in response.documents if doc['id'] in docs_used]
    matched_titles = [doc['title'] for doc in response.documents if doc['id'] in docs_used]
    citations = dict(zip(matched_titles, matched_urls))
    # returnDict['citation_urls'] = matched_urls
    # returnDict['citation_titles'] = matched_titles
    returnDict['citations'] = citations

def classifyLangauge(string):
    response = co.detect_language(texts=[string])
    language_names = [lang.language_name for lang in response.results]
    returnDict["language"] = language_names[0]

def getChatGPTResponse(string):
    client = OpenAI(api_key='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')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": f"{string}"}
                  ]
    )

    returnDict["chatgpt"] = completion.choices[0].message.content
def getCoralResponse(string, connector):
    if connector == True:
        response = co.chat(
            string,
            model="command",
            temperature=0.9,
            connectors=[{"id": "web-search"}]

        )
        returnDict["connect"] = response.text
    else:
        response = co.chat(
            string,
            model="command",
            temperature=0.9
        )
        returnDict["noConnect"] = response.text


def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Process the form data
            message = form.cleaned_data['message']
            returnDict["chatgpt"] = "Null (for now)"
            p1 = Process(target=classifyLangauge(message))
            p1.start()
            p2 = Process(target=getCoralResponse(message, False))
            p2.start()
            p3 = Process(target=getCoralResponse(message, True))
            p3.start()
            p4 = Process(target=getChatGPTResponse(message))
            p5 = Process(target=getCitations(message))
            p4.start()
            p1.join()
            p2.join()
            p3.join()
            p4.join()
            p5.join()
            # Do something with the data (e.g., save to a database)

            # For demonstration purposes, you can just display the data in the template
            return render(request, 'thank_you.html',
                          {'query': message,
                                  'langauge': returnDict["language"],
                                  'noConnect': returnDict["noConnect"],
                                  'withConnect': returnDict["connect"],
                                  'citations':returnDict["citations"],
                                  'chatGPT': returnDict['chatgpt']})
    else:
        form = MyForm()

    return render(request, 'my_form_view.html', {'form': form})