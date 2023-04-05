import urllib.parse

import MolDisplay;
import sys;
import io;
import molsql
import json
import molecule
from http.server import HTTPServer, BaseHTTPRequestHandler;


public_files = [ '/index.html', '/upload.html', '/select.html', '/script.js', '/upload_script.js' ,'/select_script.js', '/display.html', '/display_script.js'];

def first_handler(db):
   
   class MyHandler(BaseHTTPRequestHandler):

      def do_GET(self):

         if self.path == "/get_element.html":
            self.send_response(200);
            self.send_header("Content-type", "text/html")
            elements = db.conn.execute( "SELECT * FROM Elements;" ).fetchall()
            
            res = str(elements)
            self.send_header( "Content-length", len(res) );
            self.end_headers();
            self.wfile.write( bytes( res, "utf-8" ) );

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

         if self.path == "/remove_element_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            cur_element = postvars['remove_element[]']
            db.conn.execute("""DELETE FROM Elements WHERE ELEMENT_NAME = ?""", (cur_element[2],))
            MolDisplay.radius = db.radius(); 
            MolDisplay.element_name = db.element_name();
            MolDisplay.header = ""
            header = """<svg version="1.1" width="1000" height="1000"
            xmlns="http://www.w3.org/2000/svg">"""
            radiant = """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
            <stop offset="0%%" stop-color="#%s"/>
            <stop offset="50%%" stop-color="#%s"/>
            <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % ("any_element", "403A3A", "A65E2E", "633A34")
            MolDisplay.header += header
            MolDisplay.header += radiant
            MolDisplay.header += db.radial_gradients();
            message = "Successfully removed the element";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );

         if self.path == "/upload_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);


            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            mol_name = postvars['mol_name'][0]
            file_content = postvars['fileInfo'][0]
            mol_file = io.TextIOWrapper(io.BytesIO(bytes(file_content, 'UTF-8')))
            try:
               db.add_molecule(mol_name, mol_file)
               
               message = "Successfuly added the molecule %s" % (mol_name);
               self.send_response( 200 ); # OK
               self.send_header( "Content-type", "text/plain" );
               self.send_header( "Content-length", len(message) );
               self.end_headers();
               self.wfile.write( bytes( message, "utf-8" ) );
            except Exception as e:
               message = "The file you have entered is not correct, please try again";
               self.send_response( 200 ); # OK
               self.send_header( "Content-type", "text/plain" );
               self.send_header( "Content-length", len(message) );
               self.end_headers();
               self.wfile.write( bytes( message, "utf-8" ) );
         elif self.path == "/display_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);


            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            is_there_rotation = postvars['is_there_rotation'][0]
            mol = db.load_mol(postvars['mol_name'][0])
            

            if (is_there_rotation == 'true'):
               rotations = []
               for n in postvars["rotations[]"]:
                  rotations.append(int(n))

               mx = molecule.mx_wrapper(rotations[0],rotations[1],rotations[2]);
               mol.xform( mx.xform_matrix );
            mol.sort()
            image = mol.svg()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(image, 'UTF-8'))
         elif self.path == "/add_handler.html":
             # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            element_info = [postvars['element_num'][0], postvars['element_code'][0], postvars['element_name'][0], postvars['color_1'][0], postvars['color_2'][0], postvars['color_3'][0], postvars['radius'][0]]
            try:
               db['Elements'] = (element_info[0], element_info[1], element_info[2], element_info[3], element_info[4], element_info[5], element_info[6])
               MolDisplay.radius = db.radius(); 
               MolDisplay.element_name = db.element_name();
               MolDisplay.header = ""
               header = """<svg version="1.1" width="1000" height="1000"
               xmlns="http://www.w3.org/2000/svg">"""
               radiant = """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
               <stop offset="0%%" stop-color="#%s"/>
               <stop offset="50%%" stop-color="#%s"/>
               <stop offset="100%%" stop-color="#%s"/>
               </radialGradient>""" % ("any_element", "403A3A", "A65E2E", "633A34")
               MolDisplay.header += header
               MolDisplay.header += radiant
               MolDisplay.header += db.radial_gradients();
            
               message = "Successfully added the element";

               self.send_response( 200 ); # OK
               self.send_header( "Content-type", "text/plain" );
               self.send_header( "Content-length", len(message) );
               self.end_headers();
               self.wfile.write( bytes( message, "utf-8" ) );
            except:
               message = "The information you have entered is invalid, please try again.";
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
# db.create_tables(); 
 
# db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 ); 
# db['Elements'] = ( 6, 'C', 'Carbon',   '808080', '010101', '000000', 40 ); 
# db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 ); 
# db['Elements'] = ( 8, 'O', 'Oxygen',   'FF0000', '050000', '020000', 40 );
MolDisplay.radius = db.radius(); 
MolDisplay.element_name = db.element_name(); 
MolDisplay.header += db.radial_gradients();


httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), first_handler(db) );
httpd.serve_forever();
