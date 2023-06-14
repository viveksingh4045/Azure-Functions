import logging
import pandas as pd
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        role = req_body.get('user_role')
    except Exception as e:
        role = "BG Finance"

    kpis = {}
    df = pd.read_excel('config.xlsx', sheet_name='kpi')
    df = df[df["role"]==role]
    data = df.to_dict(orient='records')
    for row in data:
        kpis[row['kpiname']] = {
            "value":row['value'],
            "indicator":row['indicator'],
            "summary":row['summary']
        }
    return func.HttpResponse(json.dumps(kpis),
                            mimetype="application/json",
                             status_code=200)