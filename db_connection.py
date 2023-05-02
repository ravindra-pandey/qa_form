"""
importing all the necessary libraries
"""
import time
from pymongo import MongoClient

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
    def get_qa_by_id(self, q_id):
        """Returns the question associated with the given id"""
        question=list(self.database.questions.find({"_id": q_id}))
        answers=self.get_all_answers(q_id)
        return question,answers
        
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

    def create_user(self,name,email,password,confirm_password):
        """
        This function is called when the user is signinup.
        """
        error=self.validate_signup_credentials(name,email,password,confirm_password)
        if error is None:
            
            try:
                u_id=list(self.database.users.find().sort("_id"))[-1]["_id"]
                u_id+=1
            except:
                u_id=1
            self.database.users.insert_one({"_id": u_id,"name":name, "email":email, "password":password})
            return ""
        return error

    def validate_signup_credentials(self,name,email,password,confirm_password):
        """
        This function is responsible for checking if the user is signed up. or any error in the data.
        """
        match=list(self.database.users.find({"email":email}))
    
        if len(match)>0:
            error="email already exists"
            return error
        if name=="" or name==" ":
            error = "Please enter your name"
            return error
        
        if len(password)<6:
            error="password must be at least 6 characters"
            return error
        if password !=confirm_password :
            error="passwords do not match"
            return error
        return None

    def validate_login_credentials(self,email,password):
        """This function is used to validate the login credentials"""
        match=self.database.users.find({"email":email})
        try:
            if match[0]["password"]==password:
                return True,match[0]["name"]
            else:
                return False,"password mismatch"
        except:
            error="email not found"
            pass
            return False,error
        
# URL = "mongodb://localhost:27017"

# db_operations=DatabaseOperations(URL)

# db_operations.validate_login_credentials("gautammeena@gmail.com","415")