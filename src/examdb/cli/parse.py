#!/usr/bin/env python3
import os
import re
import sys
from typing import Pattern

from ..common import Nextable
from ..db import create_db
from ..document import Document

START_SYLLABUS_REGEX: Pattern = re.compile('^FCC Element (?P<element>[0-9]) Question Pool Syllabus')
START_QUESTIONS_REGEX: Pattern = re.compile('^FCC Element (?P<element>[0-9]) Question Pool')
SUBELEMENT_TITLE_REGEX: Pattern = re.compile(
    '^SUBELEMENT (?P<subelement>[A-Z][0-9]) - (?P<description>[^\[]+?) (- )?\[')
QUESTION_START_REGEX: Pattern = re.compile(
    '^(?P<id>[A-Z][0-9][A-Z][0-9]{2}) \((?P<answer>[A-Z])\)( \[(?P<reference>[^\[]+)\])?( (?P<notes>.*))?$')
ANSWER_REGEX: Pattern = re.compile('^(?P<answer>[A-Z])\. (?P<description>.+)$')


def process_text(doc: Document) -> tuple[list[dict[str, any]], list[dict[str, any]]]:
    found_syllabus_start = False
    found_question_start = False

    gen = Nextable(doc.get_text_iterator())
    groups = []
    questions = []

    while gen.has_next():
        line = gen.next()

        if not found_syllabus_start and START_SYLLABUS_REGEX.match(line):
            found_syllabus_start = True
            continue

        if not found_question_start and START_QUESTIONS_REGEX.match(line):
            found_question_start = True
            continue

        if found_question_start:
            match = QUESTION_START_REGEX.match(line)

            if not match:
                continue

            question_id = match.group('id')
            correct_answer = match.group('answer')
            reference = match.group('reference')
            notes = match.group('notes')
            question_text = ''
            answers = {}

            while gen.has_next():
                if ANSWER_REGEX.match(gen.peek()):
                    break

                question_text += gen.next()

            while gen.has_next():
                match = ANSWER_REGEX.match(gen.peek())

                if not match:
                    break

                gen.next()
                answers[match.group('answer')] = match.group('description')

            questions.append({
                'question_id': question_id,
                'subelement_id': question_id[:2],
                'group_id': question_id[:3],
                'group_question_id': int(question_id[3:5].lstrip('0')),
                'correct_answer': correct_answer,
                'reference': reference or None,
                'notes': notes or None,
                'question_text': question_text,
                'answers': answers
            })

        elif found_syllabus_start:
            match = SUBELEMENT_TITLE_REGEX.match(line)

            if not match:
                continue

            subelement = match.group('subelement')

            groups.append({
                'subelement_id': subelement,
                'group_id': subelement,
                'description': match.group('description')
            })

            while gen.has_next():
                if not gen.peek().startswith(subelement):
                    break

                group, description = gen.next().split(" ", maxsplit=1)

                groups.append({
                    'subelement_id': subelement,
                    'group_id': group,
                    'description': description
                })

    return groups, questions


def process_images(doc: Document) -> list[dict[str, any]]:
    images = []
    image_id = 0

    for image in doc.get_image_iterator():
        image_id += 1

        images.append({
            'figure_id': str(image_id),
            'file_name': image['file_name'],
            'content_type': image['content_type'],
            'data': image['data']
        })

    return images


def parse_main():
    if len(sys.argv) < 3:
        print('Please specify document and database name.', file=sys.stderr)
        exit(1)

    doc_path = sys.argv[1]
    db_path = sys.argv[2]

    if not os.path.exists(doc_path):
        print(f'Invalid document name: {doc_path}', file=sys.stderr)
        exit(1)

    doc = Document(doc_path)

    groups, questions = process_text(doc)
    images = process_images(doc)

    if os.path.exists(db_path):
        os.remove(db_path)

    create_db(db_path, groups, questions, images)


if __name__ == '__main__':
    parse_main()
