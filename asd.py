data={"object": "whatsapp_business_account", "entry": [{"id": "108828695276403", "changes": [{"value": {"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15550752089", "phone_number_id": "105875182242051"}, "contacts": [{"profile": {"name": "DN"}, "wa_id": "5491166531292"}], "messages": [{"from": "5491166531292", "id": "wamid.HBgNNTQ5MTE2NjUzMTI5MhUCABIYFjNFQjBFMDk1NzcwRUFBNzM3NkZBQjAA", "timestamp": "1701032240", "text": {"body": "Hola"}, "type": "text"}]}, "field": "messages"}]}]}


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

print(data["entry"][0]["changes"][0]['value']['metadata']['display_phone_number'])




