import urllib.parse

import MolDisplay;
import sys;
import io;
import molsql
import json
from http.server import HTTPServer, BaseHTTPRequestHandler;


public_files = [ '/index.html', '/upload.html', '/select.html', '/script.js', '/upload_script.js' ,'/select_script.js', '/display.html', '/display_script.js'];

def first_handler(db):
   
   class MyHandler(BaseHTTPRequestHandler):

      def do_GET(self):

         if self.path == "/get_mol.html":
            self.send_response(200);
            self.send_header("Content-type", "text/html")


            names = db.getAllNames();
            res = {}
            for i, name in enumerate( names):
               cur = name[0]
               mol  = db.load_mol(cur)
               res[cur] = [mol.atom_no, mol.bond_no]
            message = str(res)
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );
         # used to GET a file from the list ov public_files, above
         if self.path in public_files:   # make sure it's a valid file
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            if (self.path[1:] == "index.html"):
               self.path = "/"
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();

            # send the contents
            self.wfile.write( bytes( page, "utf-8" ) );

      def do_POST(self):
         if self.path == "/upload_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print(  postvars);
            mol_name = postvars['mol_name'][0]
            file_content = postvars['fileInfo'][0]
            print(file_content)
            mol_file = io.TextIOWrapper(io.BytesIO(bytes(file_content, 'UTF-8')))
            db.add_molecule(mol_name, mol_file)
            
            

            message = "data received";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
      
         elif self.path == "/display_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            print(postvars)
            mol = db.load_mol(postvars['mol_name'][0])
            image = mol.svg()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(image, 'UTF-8'))
         elif self.path == "/add_handler.html":
             # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print(  postvars);
            mol_name = postvars['mol_name'][0]
            file_content = postvars['fileInfo'][0]
            print(file_content)
            mol_file = io.TextIOWrapper(io.BytesIO(bytes(file_content, 'UTF-8')))
            db.add_molecule(mol_name, mol_file)
            
            

            message = "data received";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
         else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

   return  MyHandler
      




db = molsql.Database(reset=False);

MolDisplay.radius = db.radius(); 
MolDisplay.element_name = db.element_name(); 
MolDisplay.header += db.radial_gradients();


httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), first_handler(db) );
httpd.serve_forever();
