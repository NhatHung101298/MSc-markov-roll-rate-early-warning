"""Chuyển khối MỤC LỤC do pandoc sinh ra xuống sau trang bìa.

Pandoc luôn chèn mục lục vào đầu tài liệu, tức đứng trước cả trang bìa. Script
này đọc lại file .docx vừa tạo, cắt khối mục lục ở đầu và chèn lại ngay sau dấu
ngắt trang đầu tiên (dấu ngắt trang kết thúc trang bìa), đồng thời thêm một dấu
ngắt trang sau mục lục để chương 1 bắt đầu ở trang mới.

Ngoài ra, script chèn dòng hướng dẫn vào phần kết quả của trường TOC. Word
thường tự cập nhật trường này khi mở file (do có thuộc tính w:dirty), khi đó
dòng hướng dẫn sẽ bị thay bằng mục lục thật; nếu vì lý do nào đó Word không tự
cập nhật, người đọc vẫn thấy hướng dẫn thay vì một trang trắng.
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

PAGE_BREAK = "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"
FALLBACK = (
    "<w:r><w:t xml:space=\"preserve\">"
    "(Bôi đen toàn bộ tài liệu và nhấn F9 để hiển thị mục lục.)"
    "</w:t></w:r>"
)


def fix(document_xml: str) -> str:
    match = re.search(r"<w:sdt>.*?Table of Contents.*?</w:sdt>", document_xml, re.DOTALL)
    if not match:
        raise SystemExit("Không tìm thấy khối mục lục trong document.xml")
    toc = match.group(0)

    # Thêm dòng hướng dẫn vào vùng kết quả của trường TOC.
    toc = toc.replace(
        "<w:fldChar w:fldCharType=\"separate\" />",
        "<w:fldChar w:fldCharType=\"separate\" /></w:r>" + FALLBACK + "<w:r>",
        1,
    )

    body = document_xml[: match.start()] + document_xml[match.end():]

    break_pos = body.find(PAGE_BREAK)
    if break_pos == -1:
        raise SystemExit("Không tìm thấy dấu ngắt trang sau trang bìa")
    insert_at = break_pos + len(PAGE_BREAK)
    return body[:insert_at] + toc + PAGE_BREAK + body[insert_at:]


def main(path: Path) -> None:
    backup = path.with_suffix(".docx.orig")
    shutil.copy2(path, backup)

    with zipfile.ZipFile(backup) as src:
        items = {name: src.read(name) for name in src.namelist()}

    items["word/document.xml"] = fix(items["word/document.xml"].decode("utf-8")).encode("utf-8")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as dst:
        for name, data in items.items():
            dst.writestr(name, data)

    backup.unlink()
    # In bằng ASCII để không phụ thuộc bảng mã của cửa sổ dòng lệnh Windows.
    print("Da chuyen muc luc xuong sau trang bia.")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
