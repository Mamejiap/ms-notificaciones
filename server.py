from flask import Flask, request
import os
import boto3 

app = Flask(__name__)

AWS_ACCESS_KEY_ID = os.environ['aws_access_key_id']

AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']

print("aws ", AWS_ACCESS_KEY_ID) # imprime  el numero de telefono
print("aws 2 ", AWS_SECRET_ACCESS_KEY) # imprime el numero de telefono
## Codigo para enviar mensajes de texto
@app.route('/', methods=['GET']) # define la ruta de la api
def home(): # define la funcion que se ejecutara al llamar a la ruta
    aws_access_key_id = AWS_ACCESS_KEY_ID, # define las credenciales
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY, # define las credenciales
    print("aws ", aws_access_key_id) # imprime el numero de telefono
    print("aws 2 ", aws_secret_access_key) # imprime el numero de telefono
    return "Hola, soy Flask" # retorna un mensaje


## Construir el metodo de la api para enviar mensajes de texto usando AWS SNS
@app.route("/sms", methods=['POST']) # define la ruta de la api
def sms():
    destination = request.form['destination'] # obtiene el numero de telefono de destino
    message = request.form['message'] # obtiene el mensaje a enviar
  
    # Create an SNS client
    client = boto3.client( # crea un cliente de boto3
        "sns", # define el servicio a usar
        aws_access_key_id = AWS_ACCESS_KEY_ID, # define las credenciales
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY, # define las credenciales
        region_name="us-east-1" # define la region
    )
    print(client) # imprime el numero de telefono
  
    # Send your sms message.
    client.publish(
        PhoneNumber=destination,
        Message=message
    )
    return "OK"

# based on the code above, build the email api method using AWS SES
@app.route("/email", methods=['POST']) # define la ruta de la api
def email():
    body = request.get_json() # obtiene el cuerpo de la solicitud
    print("body",body) # imprime el cuerpo de la solicitud

    destination = body['destination'] # obtiene el correo de destino
    message = body['message'] # obtiene el mensaje a enviar
    subject = body['subject'] # obtiene el asunto del mensaje
    
  
    # Create an SES client
    client = boto3.client( # crea un cliente de boto3
        "ses", # define el servicio a usar
        aws_access_key_id = AWS_ACCESS_KEY_ID, # define las credenciales
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY, # define las credenciales
        region_name="us-east-1" # define la region
    )
    # send the email message using the client
    response = client.send_email( # envia el correo
        Destination={ # define la dirección del destino
            'ToAddresses': [ 
                destination,
            ],
        },
        Message={ # define el mensaje
            'Body': {
                'Text': {
                    'Charset': "UTF-8", 
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source="matemejia11@gmail.com" # define el correo de origen
    )
    return response

    ## Plantilla PQRS
    response = ses.send_templated_email(
    Source='nombre_remitente@example.com',
    Destination={
        'ToAddresses': [
            'nombre_destinatario@example.com',
        ],
    },
    Template='PlantillaPQRS',
    TemplateData={ 
        "nombre": "Nombre del destinatario", 
        "correo": "Correo del destinatario", 
        "mensaje": "Mensaje del destinatario"
    }
    )


## Si se ejecuta este archivo, se ejecutara el servidor de flask
if __name__ == '__main__': 
    app.run(debug=True, port=5000) # se ejecuta el servidor en el puerto 5000