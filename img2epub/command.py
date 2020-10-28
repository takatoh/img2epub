# encoding: utf-8


#import sys
import click
from datetime import datetime, timezone
from img2epub import functions as func
import os


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "__init__.py")) as f:
    exec(f.read(), about)
VERSION = about["__version__"]


def main():
    cmd(obj={})


@click.group()
@click.pass_context
@click.version_option(version=VERSION, message="v%(version)s")
def cmd(ctx):
    pass


@cmd.command(help="Build EPUB book.")
@click.pass_context
@click.argument("src_dir")
def build(ctx, src_dir):
#    src_dir = sys.argv[1]
    now = datetime.now(timezone.utc)
    tmp_dir_name = "tmp.epub.{time}".format(time=now.strftime("%Y%m%d%H%M%S"))

    func.make_dirs(tmp_dir_name)
    images = func.copy_images(src_dir, tmp_dir_name)
    images = [s.replace("\\","/") for s in sorted(images)]
    func.gen_mimetype(tmp_dir_name)
    func.copy_container(tmp_dir_name)
    book_opf_context = {
        "title": src_dir,
        "time": now.isoformat(),
        "images": images
    }
    func.gen_book_opf(tmp_dir_name, book_opf_context)
    func.copy_nav(tmp_dir_name)
    func.gen_chap1_xhtml(tmp_dir_name, book_opf_context)
    func.zip_epub(tmp_dir_name, src_dir)



if __name__ == "__main__":
    main()
