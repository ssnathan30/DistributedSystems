#!/usr/bin/env python3

import logging
import pathlib
import time
import connexion

from seller_server import encoder


def main():
    src_dir = pathlib.Path(__file__).parent.resolve()
    logging.basicConfig(filename="{0}/logs/seller_server_throughput.log".format(src_dir),
                        format='%(message)s',
                        )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Seller API'}, pythonic_params=True)
    def my_decorator(f):
        def wrapper(*args, **kwargs):
            # Do something before the endpoint is 
            start_time = time.time()
            result = f(*args, **kwargs)
            # Do something after the endpoint is called
            elapsed_time = time.time() - start_time
            print((f"{elapsed_time:.5f}"))
            logger.info((f'{f.__name__!r},{(elapsed_time):.5f}'))
            return result
        return wrapper

    # Apply the decorator to all endpoints
    app.app.wsgi_app = my_decorator(app.app.wsgi_app)
    app.run(port=9090,host='0.0.0.0')

if __name__ == '__main__':
    main()
