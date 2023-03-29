import MolDisplay;
import sys;
import io;
from http.server import HTTPServer, BaseHTTPRequestHandler;

class MyHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      if self.path == "/":
         self.send_response( 200 ); # OK
         self.send_header( "Content-length", len(home_page) );
         self.end_headers();
         self.wfile.write( bytes( home_page, "utf-8" ) );

      else:
         self.send_response( 404 );
         self.end_headers();
         self.wfile.write( bytes( "404: not found", "utf-8" ) )

   def do_POST(self):
      if self.path == "/molecule":
         #https://stackoverflow.com/questions/17888504/python-basehttprequesthandler-read-raw-post/57901027#57901027
         fileData = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
         #https://stackoverflow.com/questions/30833409/python-deleting-the-first-2-lines-of-a-string
         data = fileData.split("\n",4)[4]
         mol_file = io.TextIOWrapper(io.BytesIO(bytes(data, 'UTF-8')))

         obj = MolDisplay.Molecule()
         obj.parse(mol_file)
         obj.sort()
         image = obj.svg()

         self.send_response(200)
         self.send_header("Content-type", "image/svg+xml")
         self.end_headers()
         self.wfile.write(bytes(image, 'UTF-8'))
      else:
         self.send_response( 404 );
         self.end_headers();
         self.wfile.write( bytes( "404: not found", "utf-8" ) )





home_page = """
<html>
   <head>
      <title> File Upload </title>
   </head>
   <body>
      <h1> File Upload </h1>
      <form action="molecule" enctype="multipart/form-data" method="post">
         <p>
            <input type="file" id="sdf_file" name="filename"/>
         </p>
         <p>
            <input type="submit" value="Upload"/>
         </p>
      </form>
   </body>
</html>
""";


httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
