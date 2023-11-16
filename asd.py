data={"object": "whatsapp_business_account", "entry": [{"id": "159738167225852", "changes": [{"value": {"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15551309883", "phone_number_id": "173974499122607"}, "contacts": [{"profile": {"name": "DN"}, "wa_id": "5491166531292"}], "messages": [{"context": {"from": "15551309883", "id": "wamid.HBgNNTQ5MTE2NjUzMTI5MhUCABEYEkY1OTJDQTBCNDc1OUI0QUFFMwA="}, "from": "5491166531292", "id": "wamid.HBgNNTQ5MTE2NjUzMTI5MhUCABIYFjNFQjBBNkE2NEUxRjE3RTE4REU3RTEA", "timestamp": "1700144670", "type": "interactive", "interactive": {"type": "list_reply", "list_reply": {"id": "sed1_row_2", "title": "⭐​⭐​"}}}]}, "field": "messages"}]}]}


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

print(data["entry"][0]['changes'][0]['value']['messages'][0]['context']['id'])
print(len(data["entry"][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply']['title']))