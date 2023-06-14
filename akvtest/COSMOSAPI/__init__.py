import logging
import os
from urllib import request
import pymongo
import json
import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    CONNECTION_STRING = os.environ["cosmos_db_connection_string"]
    DB_NAME = os.environ["cosmosdb_database_name"]
    COLLECTION_ID = os.environ["collection_id"]	
    
    client = pymongo.MongoClient(CONNECTION_STRING)

    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")
    
    name = req.params.get('name')
    db = client[DB_NAME]
    COLLECTION = db[COLLECTION_ID]
    document_id = COLLECTION.insert_one({"Name":name}).inserted_id
    
    print(f"Record id - {document_id } have been inserted successfully")
    
    if document_id:
        receiveMessage(1)
        #sendMessage(document_id)
        return func.HttpResponse(f"Hello,{name} record id {document_id} have been inserted successfully")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def sendMessage(document_id):
    cn = os.environ['akstest_SERVICEBUS']
    qn = os.environ['QUEUE_NAME']
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=cn)
    with servicebus_client:
        # get a Queue Sender object to send messages to the queue
        sender = servicebus_client.get_queue_sender(queue_name=qn)
        with sender:
            message = ServiceBusMessage(b'{"MessageName":"DEMO","MessageText":"TestMessage"}')
            # send the message to the queue
            sender.send_messages(message)
            print(f"{document_id} sent for uuid genration")

def receiveMessage(batchSize):
    cn = os.environ['akstest_SERVICEBUS']
    qn = os.environ['R_QUEUE_NAME']
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=cn)
    with servicebus_client:
    # get the Queue Receiver object for the queue
        receiver = servicebus_client.get_queue_receiver(queue_name=qn, max_wait_time=5)
        sb = receiver.receive_messages(max_message_count = batchSize)
        print("************ROXM****",str(sb))
