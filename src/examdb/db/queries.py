#!/usr/bin/env python3

init_db_sql = """
CREATE TABLE groups (
    subelement_id  CHAR(2),
    group_id       CHAR(3),
    description    TEXT,
    
    PRIMARY KEY (group_id)
) WITHOUT ROWID;

CREATE TABLE questions (
    question_id       CHAR(5),
    subelement_id     CHAR(2),
    group_id          CHAR(3),
    group_question_id INT,
    reference         TEXT,
    notes             TEXT,
    question_text     TEXT,
    
    PRIMARY KEY (question_id)
) WITHOUT ROWID;

CREATE TABLE answers (
    question_id CHAR(5),
    answer_id   CHAR(1),
    is_correct  BOOLEAN,
    answer_text TEXT,
    
    PRIMARY KEY (question_id, answer_id)
) WITHOUT ROWID;

CREATE TABLE figures (
    figure_id    VARCHAR(5),
    file_name    VARCHAR(100),
    content_Type VARCHAR(100),
    data         BLOB,
    
    PRIMARY KEY (figure_id)
) WITHOUT ROWID;

CREATE TABLE question_figure (
    question_id CHAR(5),
    figure_id VARCHAR(5),
    
    PRIMARY KEY (question_id, figure_id)
) WITHOUT ROWID;
"""

insert_group_sql = """
INSERT INTO groups
    (subelement_id, group_id, description)
VALUES
    (:subelement_id, :group_id, :description)
"""

insert_question_sql = """
INSERT INTO questions
    (question_id, subelement_id, group_id, group_question_id, reference, notes, question_text)
VALUES
    (:question_id, :subelement_id, :group_id, :group_question_id, :reference, :notes, :question_text);
"""

insert_answer_sql = """
INSERT INTO answers
    (question_id, answer_id, is_correct, answer_text)
VALUES
    (:question_id, :answer_id, :is_correct, :answer_text);
"""

insert_figure_sql = """
INSERT INTO figures
    (figure_id, file_name, content_type, data)
VALUES
    (:figure_id, :file_name, :content_type, :data);
"""

insert_question_figure_sql = """
INSERT INTO question_figure
    (question_id, figure_id)
VALUES
    (:question_id, :figure_id);
"""

select_figures_sql = """
SELECT figure_id, file_name, content_type, data
FROM figures;
"""
