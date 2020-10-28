# encoding: utf-8


import sys
from datetime import datetime, timezone
from img2epub import functions as func


def main():
    src_dir = sys.argv[1]
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
