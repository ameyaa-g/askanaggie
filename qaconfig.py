import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering.authoring import AuthoringClient




endpoint = "https://aggieask.cognitiveservices.azure.com/"
credential = AzureKeyCredential("d914669beeb647a09792e638e08280da")
# get service secrets

key = "d914669beeb647a09792e638e08280da"

# create client
client = AuthoringClient(endpoint, AzureKeyCredential(key))
with client:

    # create project
    project_name = "AskAnAggie"
    project = client.create_project(
        project_name=project_name,
        options={
            "description": "TSPE special project",
            "language": "en",
            "multilingualResource": True,
            "settings": {
                "defaultAnswer": "no answer"
            }
        })

    project_name = "AskAnAggie"
    update_sources_poller = client.begin_update_sources(
        project_name=project_name,
        sources=[
            {
                "op": "add",
                "value": {
                    "displayName": "Ask An Aggie",
                    # add a source here -- website with the information
                    "sourceUri": " ",
                    "sourceKind": "url"
                }
            }
        ]
    )
    update_sources_poller.result()


    client1 = QuestionAnsweringClient(endpoint, credential)


