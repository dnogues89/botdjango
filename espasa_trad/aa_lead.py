import requests
import json

class LeadAA():
    def __init__(self, cliente) -> None:
        self.modelo = cliente.modelo
        self.telefono = cliente.telefono
        self.email = cliente.email
        self.canal = cliente.canal_contacto
        self.comentario = cliente.comentario
        self.get_name(cliente.nombre)
        self.send_lead()

    def get_name(self, cliente):
        lista = cliente.split(' ')
        if len(lista)>=2:
            self.name = lista[0]
            self.last_name = ' '.join(lista[1:])
        else:
            self.name = cliente
            self.last_name = 'NN'

    def send_lead(self):
        json_data = json.dumps(self.build_lead())
        url = "https://espasa.tecnomcrm.com/api/v1/webconnector/consultas/adf"
        headers = {
            "Content-Type" : "application/json ",
            }
        username = "espasa_landing@api.com"
        password = "123456"
        headers = {"Content-Type" : "application/json "}
        self.response = requests.post(url, headers=headers ,auth=(username, password),data=json_data)

    def build_lead(self):

        data = {

  "prospect": {

      "customer": {
          "comments": self.comentario,

          "contacts": [

              {

                  "emails": [

                      {

                          "value": self.email

                      }

                  ],

                  "names": [

                      {

                          "part": "first",

                          "value": self.name

                      },

                      {

                          "part": "last",

                          "value": self.last_name

                      }

                  ],

                  "phones": [

                      {

                          "type": "cellphone",

                          "value": self.telefono

                      }

                  ],

              }

          ]

      },

        "vehicles": [

          {

              "make": "Volkswagen",

              "model": self.modelo

          }

        ],

      "provider": {

          "name": {

              "value": self.canal

          },

          "service": "Espasa Tradicional"

      },


  }

}
        return data
