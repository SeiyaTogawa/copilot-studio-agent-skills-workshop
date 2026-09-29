"""ハンズオン配布物（dist/）を作る。

- expense-policy-check/assets/expense-policy-original.pdf : 規程 md を Edge（headless）で PDF 化した「原本」
  （PDF がない、または references/expense-policy.md のほうが新しい場合だけ再生成。--pdf で強制再生成）
- dist/expense-policy-check.md  : SKILL.md 単体（Upload の .md 方式用）
- dist/expense-policy-check.zip : SKILL.md + references/ + assets/（Upload の .zip 方式用）
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE / "expense-policy-check"
POLICY_MD = SKILL_DIR / "references" / "expense-policy.md"
POLICY_PDF = SKILL_DIR / "assets" / "expense-policy-original.pdf"
DIST = HERE / "dist"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate(skill_md: Path) -> None:
    raw = skill_md.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        sys.exit(f"{skill_md}: UTF-8 BOM があります。BOMなしで保存してください。")
    text = raw.decode("utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"{skill_md}: YAML frontmatter が見つかりません。")
    fm = dict(
        (k.strip(), v.strip().strip('"'))
        for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    )
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        sys.exit(f"name が仕様違反です: {name!r}")
    if name != skill_md.parent.name:
        sys.exit(f"name ({name}) とフォルダ名 ({skill_md.parent.name}) が一致しません。")
    if not desc or len(desc) > 1024:
        sys.exit(f"description が空か 1024 文字を超えています（{len(desc)} 文字）。")
    print(f"OK: name={name} / description={len(desc)} 文字")


def inline(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text))


def md_to_html(md: str) -> str:
    out, list_tag = [], None
    for line in md.splitlines():
        m_ol = re.match(r"^(\d+)\. (.*)", line)
        m_ul = re.match(r"^\s*- (.*)", line)
        tag = "ol" if m_ol else "ul" if m_ul else None
        if list_tag and tag != list_tag and not (list_tag == "ol" and m_ul):
            out.append(f"</{list_tag}>")
            list_tag = None
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("> "):
            out.append(f"<p class='note'>{inline(line[2:])}</p>")
        elif m_ol:
            if list_tag != "ol":
                out.append("<ol>")
                list_tag = "ol"
            out.append(f"<li>{inline(m_ol.group(2))}</li>")
        elif m_ul:
            if list_tag is None:
                out.append("<ul>")
                list_tag = "ul"
            out.append(f"<li class='sub'>・{inline(m_ul.group(1))}</li>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if list_tag:
        out.append(f"</{list_tag}>")
    body = "\n".join(out)
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
body {{ font-family: 'Meiryo', 'BIZ UDPGothic', sans-serif; font-size: 11pt; line-height: 1.7; margin: 20mm; }}
h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4px; }}
h2 {{ font-size: 13pt; margin-top: 16px; }}
.note {{ color: #555; font-size: 9.5pt; }}
ol {{ padding-left: 1.6em; }} li.sub {{ list-style: none; margin-left: 1em; }}
</style></head><body>{body}</body></html>"""


def build_pdf(force: bool) -> None:
    if not force and POLICY_PDF.exists() and POLICY_PDF.stat().st_mtime >= POLICY_MD.stat().st_mtime:
        print(f"PDF は最新: {POLICY_PDF.relative_to(HERE)}")
        return
    if not EDGE.exists():
        sys.exit(f"Edge が見つかりません: {EDGE}")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "policy.html"
        src.write_text(md_to_html(POLICY_MD.read_text(encoding="utf-8")), encoding="utf-8")
        subprocess.run(
            [str(EDGE), "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={Path(tmp) / 'edge'}", f"--print-to-pdf={POLICY_PDF}", src.as_uri()],
            check=True, capture_output=True, timeout=120,
        )
    if not POLICY_PDF.exists() or POLICY_PDF.stat().st_size == 0:
        sys.exit("PDF の生成に失敗しました。")
    print(f"PDF を生成: {POLICY_PDF.relative_to(HERE)}")


def main() -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    validate(skill_md)
    build_pdf(force="--pdf" in sys.argv[1:])
    DIST.mkdir(exist_ok=True)

    shutil.copyfile(skill_md, DIST / f"{SKILL_DIR.name}.md")

    zip_path = DIST / f"{SKILL_DIR.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(SKILL_DIR.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(SKILL_DIR).as_posix())
    print(f"作成: {DIST / (SKILL_DIR.name + '.md')}")
    print(f"作成: {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        for n in zf.namelist():
            print("  ", n)


if __name__ == "__main__":
    main()
