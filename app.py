from flask import Flask, request, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
# from pymongo.errors import DuplicateKeyError
# from werkzeug.utils import secure_filename
import os
import datetime


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Quizz'
mongo_q = PyMongo(app)

UPLOAD_FOLDER = 'static'  # Folder to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}  # Allowed file extensions for images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# API's supporter functions
def get_entities(collection_name, dbinitialize):
    all_entities = list(dbinitialize.db[collection_name].find())
    return jsonify(all_entities)


def get_entity(collection_name, entity_id, dbinitialize):
    entity = dbinitialize.db[collection_name].find_one({"_id": entity_id})
    return entity


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload_image', methods=['POST'])
def upload_image(image):
    # image = request.files.get('image')
    if image and allowed_file(image.filename):
        filename = f"{ObjectId()}.{image.filename}"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Image uploaded successfully.", "filename": filename}), 200
    else:
        return jsonify({"message": "Invalid image or file format."}), 400

@app.route('/get_all_subject_quizz', methods = ['GET'])
def get_all_subject_quizz():
    return get_entities('quizz_subjects', mongo_q)

# Create and update a route to add subjects, topics, or subtopics
@app.route('/add_Subject_quizz', methods=['POST'])
def add_Subject_quizz():
    subject_name = request.form.get('subject')
    subject_document = mongo_q.db.quizz_subjects.find_one({'subject': subject_name})
    
    if subject_document is None:
        # Subject doesn't exist in the database, create it
        subject_document = {'subject': subject_name, 'topics': {}}
        mongo_q.db.quizz_subjects.insert_one(subject_document)

    topic_name = request.form.get('topic')
    subtopic_name = request.form.get('subtopic')

    if topic_name:
        if topic_name not in subject_document['topics']:
            subject_document['topics'][topic_name] = []  # Create an empty list for subtopics
            # Update the subject document in the database to include the new topic
            mongo_q.db.quizz_subjects.update_one({'subject': subject_name}, {'$set': {'topics': subject_document['topics']}})

    if subtopic_name:
        if not topic_name:
            return jsonify({"message": "Cannot add subtopic without a topic."}), 400

        if topic_name not in subject_document['topics']:
            return jsonify({"message": "Topic does not exist in the subject."}), 400

        # Check if the subtopic already exists in the topic's subtopics
        if subtopic_name not in subject_document['topics'][topic_name]:
            subject_document['topics'][topic_name].append(subtopic_name)
            # Update the subject document in the database to include the new subtopic
            mongo_q.db.quizz_subjects.update_one({'subject': subject_name}, {'$set': {'topics': subject_document['topics']}})

    return jsonify({"message": "Data added successfully."}), 200


# Quizz CRUD operations
# Get all quizes
@app.route('/get_all_quizz', methods = ['GET'])
def get_all_quizz():
    return get_entities('quizes', mongo_q)

# Get single quiz using its id
@app.route('/get_quizz/<string:quiz_id>', methods = ['GET'])
def get_quizz(quiz_id):
    return get_entity('quizes', quiz_id, mongo_q)

# Create new Quiz requires creator user id
@app.route('/create_quizz/<string:creator_id>', methods=['POST'])
def create_quizz(creator_id):
    try:
        language = request.form.get('language')
        class_name = request.form.get('class')
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        subtopic = request.form.get('subtopic')
        level = request.form.get('level')
        quiz_type = request.form.get('quiz_type')
        questions = request.form.get('question_container')  # This contains question, its image, and all options and their image if required

        options = []  # Getting all options with image
        val = 1
        for opt in questions['options']:
            variable = "option" + str(val)
            image = ''
            if 'image' in opt:
                image = opt['image']
                try:
                    image, filename = upload_image(image)
                except Exception as e:
                    return jsonify({"message": "Error uploading option image.", "error": str(e)}), 500

            data = {
                variable: questions['options'][variable],
                'image': filename,
                'answer': opt['answer']
            }
            options.append(data)
            val += 1

        question_image = questions['question_image']
        if question_image:
            try:
                question_image, que_image = upload_image(question_image)
            except Exception as e:
                return jsonify({"message": "Error uploading question image.", "error": str(e)}), 500

        new_quiz = {
            "_id": str(ObjectId()),
            "creator_id": creator_id,
            "quizz_add_time": datetime.now(),  # this will help in sort quiz for real time update
            "language": language,
            "class": class_name,
            "subject": subject,
            "topic": topic,
            "subtopic": subtopic,
            "level": level,
            "quiz_type": quiz_type,
            'question_container': {
                "question": questions['question'],
                "question_image": que_image,
                "options": options
            },
            "blocked": False      # if it is False, then show to all, if True then hide from everybody also from creator
        }

        inserted_id = mongo_q.db.quizes.insert_one(new_quiz)
        inserted = mongo_q.db.quizes.find_one({"_id": inserted_id})
        return jsonify({"message": "Subject created successfully", "_id": str(inserted["_id"])}), 201

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500

# Update quiz requires quiz id and creator id
@app.route('/update_quizz/<string:quiz_id>/<string:creator_id>', methods=['PUT'])
def update_quizz(quiz_id, creator_id):
    try:
        quiz = mongo_q.db.quizes.find_one({"_id": quiz_id})

        if quiz:
            if quiz["creator_id"] != creator_id:
                return jsonify({"message": "Unauthorized access. You do not have permission to update this quiz."}), 403

            # Get the updated quiz data from the request
            updated_data = request.form

            # Update language, class, subject, topic, subtopic, level, and quiz_type if provided
            if 'language' in updated_data:
                quiz["language"] = updated_data['language']
            if 'class' in updated_data:
                quiz["class"] = updated_data['class']
            if 'subject' in updated_data:
                quiz["subject"] = updated_data['subject']
            if 'topic' in updated_data:
                quiz["topic"] = updated_data['topic']
            if 'subtopic' in updated_data:
                quiz["subtopic"] = updated_data['subtopic']
            if 'level' in updated_data:
                quiz["level"] = updated_data['level']
            if 'quiz_type' in updated_data:
                quiz["quiz_type"] = updated_data['quiz_type']

            # Update question, question_image, and options if provided
            if 'question_container' in updated_data:
                question_container = updated_data['question_container']

                if 'question' in question_container:
                    quiz["question_container"]["question"] = question_container['question']

                if 'question_image' in question_container:
                    try:
                        question_image, que_image = upload_image(question_container['question_image'])
                        quiz["question_container"]["question_image"] = que_image
                    except Exception as e:
                        return jsonify({"message": "Error uploading question image.", "error": str(e)}), 500

                if 'options' in question_container:
                    options = []
                    val = 1
                    for opt in question_container['options']:
                        variable = "option" + str(val)
                        image = ''
                        if 'image' in opt:
                            image = opt['image']
                            try:
                                image, filename = upload_image(image)
                            except Exception as e:
                                return jsonify({"message": f"Error uploading {variable} image.", "error": str(e)}), 500

                        data = {
                            variable: opt[variable],
                            'image': filename,
                            'answer': opt['answer']
                        }
                        options.append(data)
                        val += 1

                    quiz["question_container"]["options"] = options

            # Save the updated quiz
            mongo_q.db.quizes.update_one({"_id": quiz_id}, {"$set": quiz})

            return jsonify({"message": "Quiz updated successfully."}), 200

        else:
            return jsonify({"message": "Quiz not found."}), 404

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500


# Delete quiz requires quiz id and creator id, we are not deleting quiz for real we just make it to not show to any one
@app.route('/delete_quizz/<string:quiz_id>/<string:creator_id>', methods = ['DELETE'])
def delete_quizz(quiz_id, creator_id):
    try:
        result = mongo_q.db.quizes.find_one({"_id": quiz_id})
        if result:
            if result["creator_id"] == creator_id:
                mongo_q.db.quizes.update_one({"_id": quiz_id}, {"$set": {"blocked": True}})
                return jsonify({"message": "Quiz deleted successfully."}), 200
            else:
                return jsonify({"message": "Unauthorized access. You do not have permission to delete this quiz."}), 403
        else:
            return jsonify({"message": "Quiz not found."}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)