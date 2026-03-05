import time
import pywinauto
from pywinauto import Desktop, Application
import pytesseract
from PIL import ImageGrab
import re
import sys

print("=== DEBUG CONTROL IDENTIFIERS ===")

try:
    # Kết nối với UltraViewer window (timeout dài hơn)
    app = Application(backend="uia").connect(title_re=".*UltraViewer.*", timeout=120)
    dlg = app.top_window()
    print("Connected to window:", dlg.window_text())

    # Dump controls chi tiết
    print(dlg.print_control_identifiers())

    # Thử lấy Edit controls trực tiếp (ID thường ở Edit đầu)
    edits = dlg.child_window(control_type="Edit")
    if edits.exists():
        id_text = edits.window_text().strip()
        print("Direct Edit text (possible ID):", id_text)

    # Nếu không, fallback OCR toàn màn hình
    print("Thử fallback OCR...")
    time.sleep(5)  # Chờ UI ổn định
    screenshot = ImageGrab.grab()
    screenshot.save("screen_capture.png")  # Lưu để debug nếu cần
    ocr_text = pytesseract.image_to_string(screenshot, lang='vie+eng')  # Hỗ trợ tiếng Việt
    print("OCR text từ màn hình:\n", ocr_text)

    # Parse ID và Pass từ OCR text (regex linh hoạt hơn)
    id_match = re.search(r'ID.*?\b(\d{3}\s*\d{3}\s*\d{3})\b', ocr_text, re.IGNORECASE | re.DOTALL)
    pass_match = re.search(r'(Mat khdu|Password|MatKhau).*?\b(\d{4,6})\b', ocr_text, re.IGNORECASE | re.DOTALL)

    extracted_id = id_match.group(1).replace(" ", "") if id_match else "Không lấy được"
    extracted_pass = pass_match.group(2) if pass_match else "Không lấy được"

    print(f"UltraViewer_ID: {extracted_id}")
    print(f"UltraViewer_Password: {extracted_pass}")

except Exception as e:
    print("LỖI pywinauto:", str(e))
    # Fallback OCR nếu pywinauto fail
    try:
        print("Thử fallback OCR...")
        screenshot = ImageGrab.grab()
        ocr_text = pytesseract.image_to_string(screenshot, lang='vie+eng')
        print("OCR text từ màn hình:\n", ocr_text)

        id_match = re.search(r'ID.*?\b(\d{3}\s*\d{3}\s*\d{3})\b', ocr_text, re.IGNORECASE | re.DOTALL)
        pass_match = re.search(r'(Mat khdu|Password|MatKhau).*?\b(\d{4,6})\b', ocr_text, re.IGNORECASE | re.DOTALL)

        extracted_id = id_match.group(1).replace(" ", "") if id_match else "Không lấy được"
        extracted_pass = pass_match.group(2) if pass_match else "Không lấy được"

        print(f"UltraViewer_ID: {extracted_id}")
        print(f"UltraViewer_Password: {extracted_pass}")
    except Exception as ocr_e:
        print("OCR cũng fail:", str(ocr_e))
        print("UltraViewer_ID: Không lấy được")
        print("UltraViewer_Password: Không lấy được")

print("=== END DEBUG ===")
