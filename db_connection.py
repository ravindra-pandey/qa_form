"""
importing all the necessary libraries
"""
import time
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class DatabaseOperations():

    """
    This class implements all the operations in the database.
    """

    def __init__(self, url) -> None:
        self.url: str = url
        self.client = MongoClient(url)
        self.database = self.client.forum

    def get_all_questions(self) -> list:
        """Returns all questions in the database"""
        return list(self.database.questions.find())

    def get_all_answers(self, q_id):
        """Returns all answers in the database"""
        return list(self.database.answers.find({"_id": q_id}))

    def get_question_answer_set(self):
        """Returns all questions in the database with corresponding answers"""
        question_answers = []
        questions = self.get_all_questions()

        for question in questions:
            question_answer_set = {}
            question_answer_set["question"] = question
            q_id = question["_id"]
            answers = self.get_all_answers(q_id=q_id)
            question_answer_set["answers"] = answers
            question_answers.append(question_answer_set)
        return question_answers
    @staticmethod
    def prepare_question(q_id, question, user_id):
        """
        This function is used to prepare a question for a given user and database
        """
        question_structure = {
            "_id": q_id,
            "question": question,
            "by": user_id,
            "time": time.strftime("%Y-%m-%"+"d "+"%H:%M:%S", time.localtime())
        }
        return question_structure

    @staticmethod
    def prepare_answers(q_id, ans_id, answer, user_id):
        """
        This function is responsible for preparing the answers for the given question.
        """
        answer_sturucture = {
            "_id": q_id,
            "answers": {
                f"ans{ans_id}": {"answer": answer, "by": user_id,
                                "time": time.strftime("%Y-%m-%"+"d "+"%H:%M:%S", time.localtime())}
            }
        }
        return answer_sturucture

    def feed_question(self, question, user_id):
        """
        feed a question
        """
        idx = None
        try:
            idx = list(self.database.questions.find().sort("_id"))[-1]["_id"]
            idx += 1
        except Exception as error:
            print(error)

        finally:
            if idx is None:
                idx = 1
        print(idx)

        print(f"feedinf question with id {id}")
        prepared_question = self.prepare_question(idx, question, user_id)
        self.database.questions.insert_one(prepared_question)

    # feed_question("this is 3rd ques","user2")

    def feed_answer(self, q_id, answer, user_id):
        """
        feed_answer
        """
        ans_id = None
        try:
            ans_id = int(list(list(self.database.answers.find({"_id": q_id}).sort("answers"))
                            [-1]["answers"].keys())[-1].lstrip("ans"))
            ans_id += 1
        except Exception as error:
            print(error)
        finally:
            if ans_id is None:
                ans_id = 1
        print(ans_id)

        if ans_id > 1:

            self.database.answers.update_one(
                {"_id": q_id}, {"$set": {f"answers.ans{ans_id}.answer": answer}})
            self.database.answers.update_one(
                {"_id": q_id}, {"$set": {f"answers.ans{ans_id}.by": user_id}})
            self.database.answers.update_one({"_id": q_id}, {"$set": {
                f"answers.ans{ans_id}.time":
                    time.strftime("%Y-%m-%"+"d "+"%H:%M:%S", time.localtime())}})
        else:
            prepared_answer = self.prepare_answers(
                q_id, ans_id, answer, user_id)
            self.database.answers.insert_one(prepared_answer)

    def edit_question(self, user_id, question):
        """
        this function is called when the user is editing a question.
        """
        self.database.questions.find({"question": question, "by": user_id})


# db_operations = DatabaseOperations("mongodb://localhost:27017")

# print(db_operations.get_question_answer_set())
