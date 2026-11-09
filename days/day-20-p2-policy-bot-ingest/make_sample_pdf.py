"""Day 20: build two small sample PDFs, using only the Python standard library.

    python make_sample_pdf.py

1. lala_hr_policy.pdf      : 12 pages with real text (read from sample_policy.txt)
2. lala_scanned_notice.pdf : 1 page with only grey boxes and no text layer.
                             It behaves like a scanned page: extract_text() gives "".

All content is fictional sample data for learning.
"""

import textwrap
from pathlib import Path

HERE = Path(__file__).parent


def read_pages(path):
    """Split the text file on '=== PAGE n ===' lines. Returns a list of page texts."""
    pages = []
    current = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("=== PAGE"):
            if current:
                pages.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        pages.append("\n".join(current).strip())
    return pages


def escape(text):
    """PDF strings need backslash and brackets escaped."""
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text_stream(page_text):
    """Drawing commands that write the page text, one line under the other."""
    lines = []
    for raw in page_text.splitlines():
        lines.extend(textwrap.wrap(raw, 85) or [""])
    parts = ["BT", "/F1 11 Tf", "16 TL", "50 790 Td"]
    for line in lines:
        parts.append(f"({escape(line)}) Tj T*")
    parts.append("ET")
    return "\n".join(parts)


def boxes_stream():
    """Only grey bars, like a photo of text. No text inside the PDF."""
    parts = ["0.6 g"]
    y = 780
    for width in [420, 380, 460, 300, 440, 360, 400, 250]:
        parts.append(f"50 {y} {width} 10 re f")
        y -= 24
    return "\n".join(parts)


def write_pdf(path, streams):
    """Write a minimal valid PDF. One content stream per page."""
    objects = []  # object bodies; object number = index + 1
    page_count = len(streams)
    # Object 1: catalog, 2: page list, 3: font. Then page + content pairs.
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(page_count))
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {page_count} >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for i, stream in enumerate(streams):
        content_num = 5 + 2 * i
        objects.append(
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_num} 0 R >>"
        )
        data = stream.encode("latin-1")
        objects.append(f"<< /Length {len(data)} >>\nstream\n{stream}\nendstream")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for num, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{num} 0 obj\n{body}\nendobj\n".encode("latin-1")

    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("latin-1")
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode("latin-1")
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("latin-1")
    out += f"startxref\n{xref_at}\n%%EOF\n".encode("latin-1")
    path.write_bytes(bytes(out))


def main():
    pages = read_pages(HERE / "sample_policy.txt")
    write_pdf(HERE / "lala_hr_policy.pdf", [text_stream(p) for p in pages])
    print(f"Made lala_hr_policy.pdf ({len(pages)} pages, text PDF)")

    write_pdf(HERE / "lala_scanned_notice.pdf", [boxes_stream()])
    print("Made lala_scanned_notice.pdf (1 page, no text layer: the trap)")


if __name__ == "__main__":
    main()
