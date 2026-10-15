"""Check and package this dependency-free Skill on Windows and macOS."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
NAME = "cross-platform-github-project"
SKILL = ROOT / ".agents" / "skills" / NAME
# Explicit inventory keeps credentials, Git metadata and local caches out of ZIPs.
FILES = (Path("SKILL.md"), Path("agents/openai.yaml"))


def check():
    for relative in FILES:
        path = SKILL / relative
        data = path.read_bytes()
        text = data.decode("utf-8")
        if not text.strip() or b"\r" in data:
            raise ValueError(f"{path}: expected nonempty UTF-8 with LF endings")
        if relative.name == "SKILL.md":
            parts = text.split("---", 2)
            if len(parts) != 3 or parts[0] or not parts[2].strip():
                raise ValueError("SKILL.md requires frontmatter and instructions")
            fields = dict(
                line.split(":", 1) for line in parts[1].splitlines() if ":" in line
            )
            if fields.get("name", "").strip() != NAME:
                raise ValueError("Skill name differs from directory name")
            if not fields.get("description", "").strip():
                raise ValueError("Skill description is missing")
    print(f"Validated {NAME} ({len(FILES)} source files)")


def package():
    check()
    output = ROOT / "dist" / f"{NAME}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w") as archive:
        for relative in FILES:
            entry = ZipInfo(f"{NAME}/{relative.as_posix()}", (2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, (SKILL / relative).read_bytes())
    print(f"Packaged {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "package"))
    args = parser.parse_args()
    if args.action == "check":
        check()
    else:
        package()
