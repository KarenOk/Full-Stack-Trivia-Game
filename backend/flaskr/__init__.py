import os
import sys
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_cors import CORS
import random

from models import setup_db, Question, Category, Leaderboard

QUESTIONS_PER_PAGE = 10


def standalone_print(item):
    print("\n\n", item, "\n\n")


def paginator(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start: end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    '''
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        '''
          Set Access-Control headers
        '''
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, PATCH, DELETE, OPTIONS")

        return response

    @app.route("/categories")
    def get_categories():
        '''
          Endpoint to get all available categories.
        '''
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}

        return jsonify({
            "categories": formatted_categories
        })

    @app.route("/categories", methods=["POST"])
    def add_category():
        '''
          Endpoint to add a new category.
        '''
        try:
            type = request.get_json()["type"]
            category = Category(type=type)
            category.insert()

            return jsonify({
                "added": category.id,
                "success": True
            })
        except:
            abort(400)

    @app.route("/questions")
    def get_questions():
        '''
          Endpoint to get all questions with pagination.
        '''
        questions = Question.query.all()
        categories = Category.query.all()
        paginated_questions = paginator(request, questions)

        if not len(paginated_questions):
            abort(404)

        return jsonify({
            "questions": paginated_questions,
            "total_questions": len(questions),
            "categories": {
                category.id: category.type for category in categories},
            "current_category": None
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        '''
          Endpoint to DELETE question using a question ID.
        '''
        question = Question.query.get(question_id)
        if not question:
            abort(404)

        try:
            question.delete()
            return jsonify({
                "success": True,
                "deleted": question.id
            })
        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def add_question():
        '''
          Endpoint to add a new question and to get questions based on a search term.
        '''
        try:
            data = request.get_json()

            searchTerm = data.get("searchTerm", None)

            if searchTerm is not None:
                questions = Question.query.filter(
                    Question.question.ilike("%{}%".format(searchTerm))
                ).all()
                formatted_questions = [question.format()
                                       for question in questions]

                return jsonify({
                    "questions": formatted_questions,
                    "totalQuestions": len(questions),
                    "currentCategory": None
                })
            else:
                question = data["question"]
                answer = data["answer"]
                difficulty = int(data["difficulty"])
                category = int(data["category"])

                question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category,
                )

                question.insert()

                return jsonify({
                    "added": question.id,
                    "success": True
                })

        except Exception:
            abort(400)

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_in_category(category_id):
        '''
          Endpoint to get questions based on category.
        '''
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(questions),
            "currentCategory": None
        })

    @app.route("/quizzes", methods=["POST"])
    def get_question_for_quiz():
        '''
          Endpoint to get questions to play the quiz.

          This endpoint takes category and previous question parameters
          and returns a random questions within the given category,
          if provided, and that is not one of the previous questions.
        '''
        data = request.get_json()
        try:
            previous_questions = data["previous_questions"]
            quiz_category = data["quiz_category"]
        except Exception:
            abort(400)

        if quiz_category:
            questions = Question.query.filter_by(category=quiz_category).filter(
                Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.filter(
                ~Question.category.in_(previous_questions)).all()

        question = random.choice(questions).format() if questions else None

        return jsonify({
            "question": question
        })

    @app.route("/leaderboard")
    def get_leaderboard_scores():
        ''' Endpoint to get leaderboard scores '''

        results = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
        paginated_results = paginator(request, results)
        return jsonify({
            "results": paginated_results,
            "totalResults": len(results)
        })

    @app.route("/leaderboard", methods=["POST"])
    def post_to_leaderboard():
        '''
          Endpoint to add a new category.
        '''
        try:
            player = request.get_json()["player"]
            score = int(request.get_json()["score"])

            board_item = Leaderboard(player=player, score=score)
            board_item.insert()

            return jsonify({
                "added": board_item.id,
                "success": True
            })
        except:
            abort(400)

    '''
      Error handlers for all expected errors
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": 404,
            "message": "The requested resource was not found."
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "error": 422,
            "message": "Your request was unprocessable."
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": 400,
            "message": "Bad request."
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": 500,
            "message": "Internal server error."
        })

    return app
