import os
from application import app
import logging

# run the application!
if __name__ == '__main__':
     # Bind to PORT if defined, otherwise default to 5000.
 
    
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)

 
 	
    port = int(os.environ.get('PORT', 8000))
    print('Running on port: %s' % str(port))
    app.run(host='0.0.0.0', port=port, debug=True)
