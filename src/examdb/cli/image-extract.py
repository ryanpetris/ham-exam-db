#!/usr/bin/env python3

import os
import sys

from ..db import extract_figures


def image_extract_main():
    if len(sys.argv) < 3:
        print('Please specify database name and extraction directory.', file=sys.stderr)
        exit(1)

    db_path = sys.argv[1]
    image_dir = sys.argv[2]

    if not os.path.exists(db_path):
        print(f'Invalid database name: {db_path}', file=sys.stderr)
        exit(1)

    if not os.path.exists(image_dir):
        os.makedirs(image_dir, exist_ok=True)

    for image in extract_figures(db_path):
        file_name = image['figure_id'] + os.path.splitext(image['file_name'])[1]

        with open(os.path.join(image_dir, file_name), 'wb') as f:
            f.write(image['data'])


if __name__ == '__main__':
    image_extract_main()
