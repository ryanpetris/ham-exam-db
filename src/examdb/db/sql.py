#!/usr/bin/env python3

import os
import re
import sqlite3
from typing import Iterator, Pattern

from .queries import init_db_sql, insert_group_sql, insert_question_sql, insert_answer_sql, insert_figure_sql, \
    insert_question_figure_sql, select_figures_sql

FIGURE_REGEX: Pattern = re.compile('Figure (?P<id>[A-Z]([0-9]+)?-[0-9]+)', re.IGNORECASE)
FIGURE_ID_REGEX: Pattern = re.compile('(?P<part1>[A-Z])(?P<part2>[0-9]+)?-(?P<part3>[0-9]+)', re.IGNORECASE)
IMAGE_ID_REGEX: Pattern = re.compile('image(?P<id>[0-9]+).*', re.IGNORECASE)


def create_db(dbpath: str, groups: list[dict[str, any]], questions: list[dict[str, any]],
              figures: list[dict[str, any]]):
    if os.path.exists(dbpath):
        raise FileExistsError()

    con: sqlite3.Connection = sqlite3.connect(dbpath)

    con.executescript(init_db_sql)
    con.executemany(insert_group_sql, groups)
    con.executemany(insert_question_sql, questions)
    con.executemany(insert_answer_sql, _get_answer_generator(questions))

    question_figures = list(_get_question_figure_generator(questions))

    _set_figure_ids(figures, question_figures)

    con.executemany(insert_figure_sql, figures)
    con.executemany(insert_question_figure_sql, question_figures)

    con.commit()
    con.close()


def extract_figures(dbpath: str) -> list[dict[str, any]]:
    if not os.path.exists(dbpath):
        raise FileNotFoundError()

    con: sqlite3.Connection = sqlite3.connect(dbpath)
    cur: sqlite3.Cursor = con.execute(select_figures_sql)

    rows = list(cur.fetchall())
    columns = cur.description
    results = []

    for row in rows:
        result = {}

        for i, data in enumerate(row):
            result[columns[i][0]] = data

        results.append(result)

    con.close()

    return results


def _get_answer_generator(questions: list[dict[str, any]]) -> Iterator[dict[str, any]]:
    for question in questions:
        for key, value in question['answers'].items():
            yield {
                'question_id': question['question_id'],
                'answer_id': key,
                'is_correct': key == question['correct_answer'],
                'answer_text': value
            }


def _get_question_figure_generator(questions: list[dict[str, any]]) -> Iterator[dict[str, any]]:
    for question in questions:
        for match in FIGURE_REGEX.finditer(question['question_text']):
            yield {
                'question_id': question['question_id'],
                'figure_id': match.group('id')
            }


def _set_figure_ids(figures: list[dict[str, any]], question_figures: list[dict[str, any]]):
    distinct_figures = set(x['figure_id'] for x in question_figures)

    def figure_id_sort(figure_id: str) -> tuple[str, int, int]:
        match = FIGURE_ID_REGEX.fullmatch(figure_id)

        return match.group('part1'), int(match.group('part2')) if match.group('part2') is not None else 0, int(
            match.group('part3'))

    def image_id_sort(figure: dict[str, any]) -> int:
        match = IMAGE_ID_REGEX.fullmatch(figure['file_name'])

        return int(match.group('id'))

    sorted_figure_ids = sorted(distinct_figures, key=figure_id_sort)
    sorted_figures = sorted(figures, key=image_id_sort)

    if len(sorted_figure_ids) != len(sorted_figures):
        raise Exception(
            f'Referenced ({len(sorted_figure_ids)}) and provided ({len(sorted_figures)}) figures does not match.')

    for i, figure_id in enumerate(sorted_figure_ids):
        sorted_figures[i]['figure_id'] = figure_id
