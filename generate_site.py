import os
import qrcode

# --- SETTINGS ---
BASE_URL = "https://omkar1160.github.io/Graph/student_graphs/"  # Hosted location of graphs
GRAPH_DIR = "student_graphs"   # Folder where analysis.py saves graphs
QRCODE_DIR = "qrcodes"         # Folder to save QR codes
INDEX_FILE = "index.html"      # Main webpage

# --- Ensure output folders exist ---
os.makedirs(QRCODE_DIR, exist_ok=True)

# --- Collect graph files ---
graph_files = [f for f in os.listdir(GRAPH_DIR) if f.lower().endswith(".png")]

# --- Generate QR codes ---
for fname in graph_files:
    url = BASE_URL + fname
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(QRCODE_DIR, fname.replace(".png", "_qr.png"))
    img.save(qr_path)

print(f"✅ QR codes saved in '{QRCODE_DIR}'")

# --- Generate index.html ---
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write("<html><head><title>Cadet Graphs</title></head><body>\n")
    f.write("<h1>Cadet Performance Graphs</h1>\n<ul>\n")

    for fname in graph_files:
        cadet_name = fname.replace(".png", "").replace("_", " ")
        graph_url = f"{GRAPH_DIR}/{fname}"
        qr_url = f"{QRCODE_DIR}/{fname.replace('.png', '_qr.png')}"
        f.write(f"<li><b>{cadet_name}</b><br>\n")
        f.write(f"<img src='{graph_url}' width='400'><br>\n")
        f.write(f"QR: <img src='{qr_url}' width='150'><br><br></li>\n")

    f.write("</ul>\n</body></html>")

print(f"✅ Website generated: {INDEX_FILE}")
