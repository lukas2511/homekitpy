from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import tlv
import srp
import hashlib
import hmac
import pprint

ACC_NAME = "Test"
PASSWORD = "25111992"

srp_salt, srp_session_key = srp.create_salted_verification_key(ACC_NAME, PASSWORD)

key = hmac.new("Pair-Setup-Salt", srp_session_key, hashlib.sha512).digest()
okm = hmac.new(key, "Pair-Setup-Encryption-Key", hashlib.sha512).digest()

class HomeKitHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        print s.path

    def do_POST(s):
        length = int(s.headers['Content-Length'])
        post_data = s.rfile.read(length)
        if s.path == '/pair-setup':
            s.close_connection = 0
            s.protocol_version = "HTTP/1.1"
            tlv_data = tlv.unpack(post_data)
            pprint.pprint(tlv_data)
            response = []
            response.append({'type': 'auth_tag', 'length': 1, 'data': 2})
            response.append({'type': 'public_key', 'length': len(okm), 'data': okm})
            response.append({'type': 'salt', 'length': 16, 'data': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})
            output = tlv.pack(response)
            s.send_response(200)
            s.send_header("Content-Type", "application/pairing+tlv8")
            s.send_header("Content-Length", len(output))
            s.end_headers()
            s.wfile.write(output)

httpd = HTTPServer(('0.0.0.0', 50000), HomeKitHandler)
try:
    httpd.serve_forever()
except:
    pass
httpd.server_close()
