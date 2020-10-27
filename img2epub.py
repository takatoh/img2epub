#!/usr/bin/env python
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


def make_dirs(tmp_dir_name):
    os.makedirs(os.path.join(tmp_dir_name, "META-INF"))
    os.makedirs(os.path.join(tmp_dir_name, "EPUB"))


def copy_images(src_dir, tmp_dir_name):
    images_dir = os.path.join(tmp_dir_name, "EPUB/images")
    shutil.copytree(src_dir, images_dir)
    return glob.glob("{dir}/*".format(dir=images_dir))


def gen_mimetype(tmp_dir_name):
    with open(os.path.join(tmp_dir_name, "mimetype"), "w") as f:
        f.write("application/epub+zip")


def copy_container(tmp_dir_name):
    shutil.copyfile("data/container.xml", os.path.join(tmp_dir_name, "META-INF/container.xml"))


def gen_book_opf(tmp_dir_name, context):
    env = Environment(loader=FileSystemLoader("data"))
    template = env.get_template("book.opf.template")
    context["images"] = [s.replace("{tmp}/EPUB".format(tmp=tmp_dir_name), ".") for s in context["images"]]
    context["cover"] = context["images"][0]
    context["uuid"] = str(uuid.uuid4())
    with open(os.path.join(tmp_dir_name, "EPUB/book.opf"), "w") as f:
        f.write(template.render(context))


def copy_nav(tmp_dir_name):
    shutil.copyfile("data/nav.xhtml", os.path.join(tmp_dir_name, "EPUB/nav.xhtml"))


def gen_chap1_xhtml(tmp_dir_name, context):
    env = Environment(loader=FileSystemLoader("data"))
    template = env.get_template("chap1.xhtml.template")
    images = [s.replace("{tmp}/EPUB".format(tmp=tmp_dir_name), ".") for s in context["images"]]
    with open(os.path.join(tmp_dir_name, "EPUB/chap1.xhtml"), "w") as f:
        f.write(template.render(images=images))


def zip_epub(tmp_dir_name, title):
    epub_file_name = "../{title}.epub".format(title=title)
    os.chdir(tmp_dir_name)
    subprocess.run(["zip", "-X0", epub_file_name, "mimetype"], stdout=subprocess.DEVNULL)
    subprocess.run(["zip", "-r9", epub_file_name, "*", "-x", "mimetype"], stdout=subprocess.DEVNULL)
    os.chdir("..")



main()
