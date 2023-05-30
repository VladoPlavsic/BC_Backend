def server():
    from lib import app
    app.run()

def deploy_contract():
    from lib.client.client import main
    main()


import sys

if len(sys.argv) > 1:
    deploy_contract()
else:
    server()