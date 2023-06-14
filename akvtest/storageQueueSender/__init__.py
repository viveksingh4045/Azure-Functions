from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

import os, uuid
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting connection with storage Queue.')
    connect_str=os.environ["AZURE_STORAGE_QUEUE"]
    q_name='vivektest'
    queue_client = QueueClient.from_connection_string(connect_str, q_name)
    message = u"Hello World"
    print("Adding message: " + message)
    queue_client.send_message(message)

    return func.HttpResponse(
            "Message pushed to queue",
            status_code=200
    )
