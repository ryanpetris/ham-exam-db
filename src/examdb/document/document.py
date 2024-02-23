#!/usr/bin/env python3
import os.path
from typing import Iterator

import docx
import docx.document
import docx.parts.image


class Document:
    def __init__(self, docpath: str):
        with open(docpath, 'rb') as f:
            self._doc: docx.document.Document = docx.Document(f)

    def get_text_iterator(self) -> Iterator[str]:
        for p in self._doc.paragraphs:
            for line in p.text.splitlines():
                yield line

    def get_image_iterator(self) -> Iterator[dict[str, any]]:
        for i in self._doc.part.package.image_parts:
            i: docx.parts.image.ImagePart

            yield {
                'file_name': os.path.basename(i.partname),
                'content_type': i.content_type,
                'data': i.image.blob
            }
