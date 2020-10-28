# encoding: utf-8


import sys
import os
import shutil
import subprocess
from datetime import datetime, timezone
import uuid
import glob
from jinja2 import Template, Environment, FileSystemLoader


def main():
    src_dir = sys.argv[1]
    now = datetime.now(timezone.utc)
    tmp_dir_name = "tmp.epub.{time}".format(time=now.strftime("%Y%m%d%H%M%S"))

    make_dirs(tmp_dir_name)
    images = copy_images(src_dir, tmp_dir_name)
    images = [s.replace("\\","/") for s in sorted(images)]
    gen_mimetype(tmp_dir_name)
    copy_container(tmp_dir_name)
    book_opf_context = {
        "title": src_dir,
        "time": now.isoformat(),
        "images": images
    }
    gen_book_opf(tmp_dir_name, book_opf_context)
    copy_nav(tmp_dir_name)
    gen_chap1_xhtml(tmp_dir_name, book_opf_context)
    zip_epub(tmp_dir_name, src_dir)
