#!/usr/bin/env python3
"""Entry point for THE WORLD TODAY - Monday 23 November 2026.

Copies the pre-rendered front page (news.png) to the make.fun output
location: $MAKEFUN_OUTPUT_DIR/entry.png when set, else /output/entry.png.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
