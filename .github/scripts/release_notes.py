"""Resolve the CHANGELOG.md section for a release tag.

Used twice by .github/workflows/release.yml: the guard job runs it to fail the
release before anything is built, and the release job runs it again with --out
to produce the file GoReleaser passes to --release-notes.

Requires the `packaging` distribution, so that a semver tag such as v0.1.0-rc1
compares equal to the PEP 440 version 0.1.0rc1 that pyproject.toml carries.
"""

import argparse
import pathlib
import re
import sys

from packaging.version import InvalidVersion, Version

CHANGELOG = pathlib.Path("CHANGELOG.md")


def section(text, label):
    """Return the body under a `## [label]` heading, or None."""
    match = re.search(
        r"^##\s*\[" + re.escape(label) + r"\][^\n]*\n(.*?)(?=^##\s*\[|\Z)",
        text,
        re.S | re.M,
    )
    return match.group(1).strip() if match else None


def resolve(tag):
    """Return the release notes for tag, or exit with an explanation."""
    try:
        version = Version(tag.removeprefix("v"))
    except InvalidVersion:
        sys.exit(f"tag {tag!r} is not a valid version")

    if not CHANGELOG.is_file():
        sys.exit(
            f"{CHANGELOG} not found in the checkout. It must be committed before "
            f"tagging -- note that `git commit -a` does not stage new files."
        )

    text = CHANGELOG.read_text(encoding="utf-8")

    # A pre-release such as v0.1.0-rc1 falls back to the 0.1.0 section, since an
    # rc rehearses the release it precedes.
    body = section(text, str(version)) or section(text, version.base_version)
    if not body:
        headings = re.findall(r"^##\s*\[([^\]]+)\]", text, re.M)
        sys.exit(
            f"{CHANGELOG} has no section for {version} or {version.base_version}. "
            f"Sections present: {', '.join(headings) or 'none'}"
        )
    return body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="the release tag, e.g. v0.1.0 or v0.1.0-rc1")
    parser.add_argument("--out", help="write the notes here instead of only printing them")
    args = parser.parse_args()

    body = resolve(args.tag)
    if args.out:
        pathlib.Path(args.out).write_text(body + "\n", encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
