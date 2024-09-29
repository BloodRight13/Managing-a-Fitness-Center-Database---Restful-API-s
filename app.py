# Task 1
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from fitness_databse_connection import get_db_connection
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

#Task 2

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)
    id = fields.String(required=True)
    class Meta:
        feilds = ('id','name', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return 'Welcome to the Coding Fitness Center'

@app.route('/members', methods = ['GET']) 
def get_members():
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary = True)

        query = 'SELECT * FROM Members'

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
@app.route('/members', methods = ["POST"]) 
def add_member():
    try:
        member_data = member_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'], member_data['id'])

        query = "INSERT INTO Members (name, age, id) VALUES (%s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({'message': 'New member added successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods = ["PUT"]) 
def update_member(id):
    try:
        member_data = member_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        updated_member= (member_data['name'], member_data['age'], id)

        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({'message': 'Updated Member successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods = ["DELETE"]) 
def delete_member(id):    

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        member_to_remove = (id,)

        cursor.execute('SELECT * FROM Members where id = %s', member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()
        
        return jsonify({'message': 'Member removed successfully'}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Task 3

class WorkoutSchema(ma.Schema):
    member_id = fields.String(required=True)
    session_id = fields.String(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)
    class Meta:
        feilds = ('member_id','session_id', 'session_date', 'session_time', 'activity')

workout_session_schema = WorkoutSchema()
workout_sessions_schema = WorkoutSchema(many=True)

@app.route('/members/workoutsessions', methods = ["GET"]) 
def get_member_workout_session():
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary = True)

        query = 'SELECT * FROM Workoutsessions'

        cursor.execute(query)

        workout_session = cursor.fetchall()

        return workout_sessions_schema.jsonify(workout_session)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/workoutsessions<int:id>', methods = ["GET"]) 
def specific_member_workout_session(id):    

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        workout_id = (id,)

        cursor.execute('SELECT * FROM Workoutsessions where id = %s', workout_id)
        member = cursor.fetchone()
        if not member:
            return jsonify({'error': 'Workout Session not found'}), 404
        
        query = "Select * FROM Workoutsessions WHERE id = %s"
        cursor.execute(query, workout_id)
        conn.commit()
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members', methods = ["POST"]) 
def add_workout_sessions():
    try:
        workout_data = workout_session_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        new_workout_session = (workout_data['member_id'], workout_data['session_id'], workout_data['session_date'], workout_data['session_time'], workout_data['activity'] )

        query = "INSERT INTO Workoutsessions (member_id, session_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(query, new_workout_session)
        conn.commit()

        return jsonify({'message': 'New workout session added successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_workout_session(session_id):
    try:
        workout_data = member_schema.load(request.json) 
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        updated_session= (workout_data['member_id'], workout_data['session_date'], workout_data['session_time'], workout_data['activity'], session_id)

        query = 'UPDATE Worksessions SET member_id = %s, session_date = %s, session_time= %s, activity = %s WHERE session_id = %s'

        cursor.execute(query, updated_session)
        conn.commit()

        return jsonify({'message': 'Updated Workout Session successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ =='__main__':
    app.run(debug=True)