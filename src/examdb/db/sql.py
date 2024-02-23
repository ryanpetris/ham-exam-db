#!/usr/bin/env python3

import os
import re
import sqlite3
from typing import Iterator, Pattern

from .queries import init_db_sql, insert_group_sql, insert_question_sql, insert_answer_sql, insert_figure_sql, \
    insert_question_figure_sql, select_figures_sql

FIGURE_REGEX: Pattern = re.compile('Figure (?P<id>[A-Z][0-9]+-[0-9]+)', re.IGNORECASE)


def create_db(dbpath: str, groups: list[dict[str, any]], questions: list[dict[str, any]],
              figures: list[dict[str, any]]):
    if os.path.exists(dbpath):
        raise FileExistsError()

    con: sqlite3.Connection = sqlite3.connect(dbpath)

    con.executescript(init_db_sql)
    con.executemany(insert_group_sql, groups)
    con.executemany(insert_question_sql, questions)
    con.executemany(insert_answer_sql, get_answer_generator(questions))
    con.executemany(insert_figure_sql, figures)
    con.executemany(insert_question_figure_sql, get_question_figure_generator(questions))

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


def get_answer_generator(questions: list[dict[str, any]]) -> Iterator[dict[str, any]]:
    for question in questions:
        for key, value in question['answers'].items():
            yield {
                'question_id': question['question_id'],
                'answer_id': key,
                'is_correct': key == question['correct_answer'],
                'answer_text': value
            }


def get_question_figure_generator(questions: list[dict[str, any]]) -> Iterator[dict[str, any]]:
    for question in questions:
        for match in FIGURE_REGEX.finditer(question['question_text']):
            yield {
                'question_id': question['question_id'],
                'figure_id': match.group('id')
            }
