import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, Leaderboard


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "udacity_trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Who was the first man on the moon?",
            "category": 1,
            "answer": "Niel Armstrong",
            "difficulty": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        res = self.client().get("/categories")
        self.assertEqual(res.status_code, 200)

    def test_add_category_success(self):
        res = self.client().post("/categories", json={"type": "Entertainment"})
        data = json.loads(res.data)
        category = Category.query.get(data["added"])

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(category)

    def test_add_category_bad_request(self):
        res = self.client().post("/categories", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions_not_found(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_add_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        question = Question.query.get(data["added"])

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(question)

    def test_add_question_bad_request(self):
        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)

    def test_delete_question_success(self):
        question = Question(
            question=self.new_question["question"],
            answer=self.new_question["answer"],
            difficulty=self.new_question["difficulty"],
            category=self.new_question["category"],
        )
        question.insert()
        question_id = question.id

        res = self.client().delete("/questions/" + str(question_id))
        data = json.loads(res.data)

        question = Question.query.get(question_id)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(question)

    def test_delete_question_not_found(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_search_questions_success(self):
        res = self.client().post("/questions", json={"searchTerm": "movie"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_search_questions_empty_string(self):
        res = self.client().post("/questions", json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_search_questions_not_found(self):
        res = self.client().post("/questions", json={"searchTerm": "abcdxyz"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(len(data["questions"]))
        self.assertFalse(data["totalQuestions"])

    def test_get_questions_in_category_success(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_get_question_for_quiz_success(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": 6
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_get_question_for_quiz_when_no_more_questions(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [10, 11],
            "quiz_category": 6
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data["question"])

    def test_get_question_for_quiz_bad_request(self):
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)

    def test_get_leaderboard_scores_success(self):
        res = self.client().get("/leaderboard")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_post_to_leaderboard_success(self):
        res = self.client().post("/leaderboard", json={
            "player": "Karen",
            "score": 4
        })
        data = json.loads(res.data)
        board_item = Leaderboard.query.get(data["added"])

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(board_item)

    def test_post_to_leaderboard_bad_request(self):
        res = self.client().post("/leaderboard", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
