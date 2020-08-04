import React, { Component } from "react";
import $ from "jquery";
import { Link } from "react-router-dom";
import "../stylesheets/QuizView.css";

const questionsPerPlay = 5;

class QuizView extends Component {
	constructor(props) {
		super();
		this.state = {
			quizCategory: null,
			previousQuestions: [],
			showAnswer: false,
			categories: {},
			numCorrect: 0,
			currentQuestion: {},
			guess: "",
			forceEnd: false,
			player: "",
		};
	}

	componentDidMount() {
		$.ajax({
			url: `/categories`,
			type: "GET",
			success: (result) => {
				this.setState({ categories: result.categories });
				return;
			},
			error: (error) => {
				alert("Unable to load categories. Please try your request again");
				return;
			},
		});
	}

	selectCategory = ({ type, id = 0 }) => {
		this.setState({ quizCategory: { type, id } }, this.getNextQuestion);
	};

	handleChange = (event) => {
		this.setState({ [event.target.name]: event.target.value });
	};

	getNextQuestion = () => {
		const previousQuestions = [...this.state.previousQuestions];
		if (this.state.currentQuestion.id) {
			previousQuestions.push(this.state.currentQuestion.id);
		}

		$.ajax({
			url: "/quizzes",
			type: "POST",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				previous_questions: previousQuestions,
				quiz_category: this.state.quizCategory.id,
			}),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {
				this.setState(
					{
						showAnswer: false,
						previousQuestions: previousQuestions,
						currentQuestion: result.question,
						guess: "",
						forceEnd: result.question ? false : true,
					},
					() => {
						if (this.state.forceEnd) this.submitToLeaderboard();
					}
				);
				return;
			},
			error: (error) => {
				alert("Unable to load question. Please try your request again");
				return;
			},
		});
	};

	submitToLeaderboard = () => {
		$.ajax({
			url: "/leaderboard",
			type: "POST",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				player: this.state.player,
				score: this.state.numCorrect,
			}),
			crossOrigin: true,
			xhrFields: {
				withCredentials: true,
			},
			success: (result) => {
				this.setState({ player: "" });
				return;
			},
			error: (error) => {
				alert(
					"Something went wrong. Your score was not posted to the leaderboard."
				);
				return;
			},
		});
	};

	submitName = (event) => {
		const value = document.getElementById("player").value;
		this.setState({ player: value });
	};

	submitGuess = (event) => {
		event.preventDefault();
		const formatGuess = this.state.guess
			.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
			.toLowerCase();
		let evaluate = this.evaluateAnswer();
		this.setState({
			numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
			showAnswer: true,
		});
	};

	restartGame = () => {
		this.setState({
			quizCategory: null,
			previousQuestions: [],
			showAnswer: false,
			numCorrect: 0,
			currentQuestion: {},
			guess: "",
			forceEnd: false,
		});
	};

	renderPrePlay() {
		return (
			<div className="quiz-play-holder">
				{this.state.player ? (
					<>
						<div className="choose-header">Choose Category</div>
						<div className="category-holder">
							<div
								className="play-category pointer-cursor"
								onClick={this.selectCategory}
							>
								ALL
							</div>
							{Object.keys(this.state.categories).map((id) => {
								return (
									<div
										key={id}
										value={id}
										className="play-category pointer-cursor"
										onClick={() =>
											this.selectCategory({
												type: this.state.categories[id],
												id,
											})
										}
									>
										{this.state.categories[id]}
									</div>
								);
							})}
						</div>
					</>
				) : (
					<div>
						<label htmlFor="player"> Enter your name: </label>
						<input
							type="text"
							name="player"
							id="player"
							style={{ padding: "8px 5px", marginRight: "5px" }}
						/>
						<input
							className="button"
							type="button"
							value="Submit"
							onClick={this.submitName}
						/>
					</div>
				)}
			</div>
		);
	}

	renderFinalScore() {
		return (
			<div className="quiz-play-holder">
				<div className="final-header">
					Your Final Score is {this.state.numCorrect}
					<p>
						<Link to="leaderboard">
							See where you rank in the leaderboard.{" "}
						</Link>{" "}
					</p>
				</div>
				<div className="play-again button" onClick={this.restartGame}>
					{" "}
					Play Again?{" "}
				</div>
			</div>
		);
	}

	evaluateAnswer = () => {
		const formatGuess = this.state.guess
			.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
			.toLowerCase();
		const answerArray = this.state.currentQuestion.answer
			.toLowerCase()
			.split(" ");
		return answerArray.includes(formatGuess);
	};

	renderCorrectAnswer() {
		const formatGuess = this.state.guess
			.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
			.toLowerCase();
		let evaluate = this.evaluateAnswer();
		return (
			<div className="quiz-play-holder">
				<div className="quiz-question">
					{this.state.currentQuestion.question}
				</div>
				<div className={`${evaluate ? "correct" : "wrong"}`}>
					{evaluate ? "You were correct!" : "You were incorrect"}
				</div>
				<div className="quiz-answer">{this.state.currentQuestion.answer}</div>
				<div
					className="next-question button pointer-cursor"
					style={{ width: "120px" }}
					onClick={this.getNextQuestion}
				>
					{" "}
					Next Question{" "}
				</div>
			</div>
		);
	}

	renderPlay() {
		return this.state.previousQuestions.length === questionsPerPlay ||
			this.state.forceEnd ? (
			this.renderFinalScore()
		) : this.state.showAnswer ? (
			this.renderCorrectAnswer()
		) : (
			<div className="quiz-play-holder">
				<div className="quiz-question">
					{this.state.currentQuestion.question}
				</div>
				<form onSubmit={this.submitGuess}>
					<input
						type="text"
						name="guess"
						className="guess"
						onChange={this.handleChange}
					/>
					<input
						className="submit-guess button"
						type="submit"
						value="Submit Answer"
					/>
				</form>
			</div>
		);
	}

	render() {
		return this.state.quizCategory ? this.renderPlay() : this.renderPrePlay();
	}
}

export default QuizView;
