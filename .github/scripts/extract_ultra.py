import time
from pywinauto import Application
import re

print("=== DEBUG CONTROL IDENTIFIERS ===")

try:
    # Kết nối window với timeout dài
    app = Application(backend="uia").connect(title_re=".*UltraViewer.*", timeout=120)
    dlg = app.top_window()
    print("Connected to window:", dlg.window_text())

    # Dump full controls (để log thấy rõ)
    dlg.print_control_identifiers()

    # Parse từ output của print_control_identifiers() – tìm Pane/Edit có title là số (ID 9 chữ số, Pass 5 chữ số)
    # Vì print_control_identifiers() in ra stdout, ta capture và parse (hoặc duyệt tree)

    # Duyệt tất cả Pane/Edit để tìm title chứa ID/Pass
    id_found = "Không lấy được"
    pass_found = "Không lấy được"

    # Duyệt children (Pane chứa ID/Pass thường là Pane với title số)
    for child in dlg.descendants():
        try:
            title = child.window_text().strip()
            if re.match(r'^\d{3}\s*\d{3}\s*\d{3}$', title):  # ID format 9 số + space
                id_found = title.replace(" ", "")
                print(f"Found ID in Pane/Edit title: {id_found}")
            elif re.match(r'^\d{4,6}$', title):  # Pass format 4-6 số
                pass_found = title
                print(f"Found Password in Pane/Edit title: {pass_found}")
        except:
            pass

    # Nếu không tìm thấy từ descendants, fallback parse từ log text (nhưng tốt nhất dùng tree)

    print(f"UltraViewer_ID: {id_found}")
    print(f"UltraViewer_Password: {pass_found}")

except Exception as e:
    print("LỖI pywinauto:", str(e))
    print("UltraViewer_ID: Không lấy được")
    print("UltraViewer_Password: Không lấy được")

print("=== END DEBUG ===")
