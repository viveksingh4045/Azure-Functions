import logging
import pandas as pd
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    questions = {}
    df = pd.read_excel('config.xlsx')
    data = df.to_dict(orient='records')
    for row in data:
        questions[row['question']] = {
            "id":row['reportid'],
            "pageName":row['pageName'],
            "visualName":row['visualName'],
            "sectionid":row['sectionid']
        }
    
    return func.HttpResponse(json.dumps(questions),
                            mimetype="application/json",
                             status_code=200)
