#!/usr/bin/python

from app import server
server.app.run(debug=True, host='0.0.0.0', port=5050)
