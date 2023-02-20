import os
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import random

class FinancialService(ServiceBase):
    @rpc(Unicode, Integer, Unicode, _returns=bool)
    def process_transaction(ctx, name, number, expiration_date):
        result = random.choices([True, False], weights=[9, 1], k=1)[0]
        return result

if __name__ == '__main__':
    soap_host = os.getenv("soap_host","localhost")
    soap_port = int(os.getenv("soap_port",6666))
    app = Application([FinancialService], 'spyne.financial.service.soap',
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11())

    wsgi_app = WsgiApplication(app)
    print(f'Listening on hostname: {soap_host}, port {soap_port}')
    server = make_server(soap_host, soap_port, wsgi_app)
    server.serve_forever()
