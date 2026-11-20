import http.server
import socketserver
import json
import os
import subprocess
import time

PORT = 8089

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/save_progress':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            photos = json.loads(body.decode('utf-8'))
            
            # Save to database
            with open("database_indexed.json", "w", encoding="utf-8") as f:
                json.dump(photos, f, ensure_ascii=False)
                
            faces_count = sum(len(p.get('descriptors', [])) for p in photos)
            print(f"💾 Saved progress: {len(photos)} photos, {faces_count} faces indexed.")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()

def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Server started at http://localhost:{PORT}")
        print("Launching Chrome to compute face descriptors...")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        cmd = [chrome_path, f"http://localhost:{PORT}/tools/compute_descriptors.html"]
        subprocess.Popen(cmd)
        
        while True:
            httpd.handle_request()
            if os.path.exists("database_indexed.json"):
                with open("database_indexed.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if len(data) >= 322:
                    print("✅ Completed all 322 photos!")
                    break

if __name__ == '__main__':
    main()
