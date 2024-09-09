###THIS ENTIRE CODE IMPLEMENTS CODE FROM HW 2 AND MY CLASS NOTES###

import flask
from flask import jsonify, request, render_template, redirect, url_for
from sqlsprint1 import creating_connection, execute_sql_query, execute_update_query
import credssprint
import hashlib

#starts flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

ultimateusername = 'username'
ultimatepassword = "244210e48437b6556980a70249a99369934a352429034cef9d7bd253b3bf2c01"  # Hash value of Password 'project'

# route for the main URL
@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

#route for updating data in the webpage form
@app.route('/update', methods=['GET', 'POST'])
def update_page():
    if request.method == 'POST':
        # Get data from the form
        facility_id = request.form['facility_id']
        classroom_id = request.form['classroom_id']
        teacher_id = request.form['teacher_id']
        child_id = request.form['child_id']
        facility_name = request.form['facilityName']
        classroom_name = request.form['classroomName']
        classroom_capacity = request.form['capacity']
        classroom_facility = request.form['facility']
        teacher_firstname = request.form['firstName']
        teacher_lastname = request.form['lastName']
        teacher_room = request.form['room']
        child_firstname = request.form['childFirstName']
        child_lastname = request.form['childLastName']
        child_age = request.form['age']
        child_room = request.form['childRoom']

        # Insert data into database 
        conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
        
        # Update data in the facilities table
        execute_update_query(conn, f"UPDATE facility SET name = '{facility_name}' WHERE id = {facility_id}")
        
        # Update data in the classrooms table
        execute_update_query(conn, f"UPDATE classroom SET name = '{classroom_name}', capacity = {classroom_capacity}, facility = '{classroom_facility}' WHERE id = {classroom_id}")
        
        # Update data in the teachers table
        execute_update_query(conn, f"UPDATE teacher SET firstname = '{teacher_firstname}', lastname = '{teacher_lastname}', room = '{teacher_room}' WHERE id = {teacher_id}")
        
        # Update data in the children table
        execute_update_query(conn, f"UPDATE child SET firstname = '{child_firstname}', lastname = '{child_lastname}', age = {child_age}, room = '{child_room}' WHERE id = {child_id}")

        # Close the database connection
        conn.close()

        # Redirect to the update page or any other page after data update
        return redirect(url_for('update_page'))

    # Render the update.html template for GET requests
    return render_template('update.html')


# form submission to add data to the database
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get data from the form
        teacher_firstname = request.form['teacher_firstname']
        teacher_lastname = request.form['teacher_lastname']
        teacher_room = request.form['teacher_room']
        facility_name = request.form['facility_name']
        classroom_capacity = request.form['classroom_capacity']
        classroom_name = request.form['classroom_name']
        classroom_facility = request.form['classroom_facility']
        child_firstname = request.form['child_firstname']
        child_lastname = request.form['child_lastname']
        child_age = request.form['child_age']
        child_room = request.form['child_room']

        # Insert data into database 
        conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
        
        # inserting data into the teacher table
        execute_update_query(conn, f"INSERT INTO teacher (firstname, lastname, room) VALUES ('{teacher_firstname}', '{teacher_lastname}', '{teacher_room}')")
        

        # Close the database connection
        conn.close()

        # Redirect to the create page or any other page after data insertion
        return redirect(url_for('create'))

    # Render the create.html template for GET requests
    return render_template('create.html')

#route for read webpage
@app.route('/read', methods=['GET'])
def read_page():
    return render_template('read.html')

# form submission to delete data from the database
@app.route('/delete', methods=['GET', 'POST'])
def delete_data():
    if request.method == 'POST':
        # Get data from the form
        facility_id = request.form.get('facilityId')
        classroom_id = request.form.get('classroomId')
        teacher_id = request.form.get('teacherId')
        child_id = request.form.get('childId')

        # Connect to the database
        conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)

        # Delete data from the tables
        if facility_id:
            execute_update_query(conn, f"DELETE FROM facility WHERE id = {facility_id}")
        if classroom_id:
            execute_update_query(conn, f"DELETE FROM classroom WHERE id = {classroom_id}")
        if teacher_id:
            execute_update_query(conn, f"DELETE FROM teacher WHERE id = {teacher_id}")
        if child_id:
            execute_update_query(conn, f"DELETE FROM child WHERE id = {child_id}")

        # Close the database connection
        conn.close()

        # Redirect to the delete page or any other page after data deletion
        return redirect(url_for('delete_page'))

    # Render the delete.html template for GET requests
    return render_template('delete.html')


#login route to handle both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # login logic for POST requests
        auth = request.authorization
        if auth:
            password_hash = hashlib.sha256(auth.password.encode()).hexdigest()
            if auth.username == ultimateusername and password_hash == ultimatepassword:
                # Redirect to the homepage if login is successful
                return redirect(url_for('index'))
        # Render the login form again with an error message for failed login attempts
        return render_template('login.html', error='Incorrect username or password')

    # Render the login.html template for GET requests
    return render_template('login.html')

#

# Routes to fetch and display data for each table
@app.route('/display_facilities', methods=['GET'])
def display_facilities():
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM facility"
    facilities = execute_sql_query(conn, sql)
    conn.close()
    return render_template('read.html', facilities=facilities)

@app.route('/display_classrooms', methods=['GET'])
def display_classrooms():
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM classroom"
    classrooms = execute_sql_query(conn, sql)
    conn.close()
    return render_template('read.html', classrooms=classrooms)

@app.route('/display_teachers', methods=['GET'])
def display_teachers():
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM teacher"
    teachers = execute_sql_query(conn, sql)
    conn.close()
    return render_template('read.html', teachers=teachers)

@app.route('/display_children', methods=['GET'])
def display_children():
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM child"
    children = execute_sql_query(conn, sql)
    conn.close()
    return render_template('read.html', children=children)


# Memory data for each table
facility = [
    {"id": 5, "name": "Sunshine Daycare"},
    {"id": 6, "name": "Rainbow Academy"}
]

classroom = [
    {"id": 10, "capacity": 20, "name": "Classroom 1", "facility": 5},
    {"id": 11, "capacity": 30, "name": "Classroom 2", "facility": 6}
]

teacher = [
    {"id": 12, "firstname": "Rose", "lastname": "Washington", "room": 1},
    {"id": 13, "firstname": "John", "lastname": "Mack", "room": 2}
]

child = [
    {"id": 12, "firstname": "Naia", "lastname": "Lucky", "age": 3, "room": 5},
    {"id": 13, "firstname": "Bob", "lastname": "Tomball", "age": 4, "room": 6}
]

# Function to check if adding a child to a classroom violates the capacity constraint
def incorrect_amount(classroom_id):
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = f"SELECT COUNT(*) FROM child WHERE classroom_id = {classroom_id}"
    children_count = execute_sql_query(conn, sql)[0][0]
    sql = f"SELECT capacity, teacher_count FROM classroom WHERE id = {classroom_id}"
    result = execute_sql_query(conn, sql)
    if result:
        capacity = result[0][0]
        teacher_count = result[0][1]
        max_children = min(capacity, teacher_count * 10)
        return children_count >= max_children
    return True


                                                                        ##LOCAL APIS##
# POST method for all tables
#Post method for facility 
@app.route('/api/facility', methods=['POST'])
def add_facility_to_list():
    request_information = request.get_json() #gets json data 
    facility.append(request_information)
    return 'The facility name provided was added to the list successfully!' #success message 


#Post method for classroom
@app.route('/api/classroom', methods=['POST'])
def add_classroom_to_list():
    request_information = request.get_json() #gets json data
    classroom.append(request_information)
    return 'The classroom provided was added to the list successfully!'#success message

#Post method for teacher 
@app.route('/api/teacher', methods=['POST'])
def add_teacher_to_list():
    request_information = request.get_json() #gets json data
    teacher.append(request_information)
    return 'The teacher provided was added to the list successfully!' #success message 


#post method for child
@app.route('/api/child', methods=['POST'])
def add_child_to_list():
    request_information = request.get_json() #gets json data
    child.append(request_information)
    return 'The child provided was added to the list successfully!' #success message


# GET method for all tables

#get method for facility 
@app.route('/facilities', methods=['GET'])
def get_facilities():
    return jsonify(facility)

#Get method for classroom
@app.route('/classrooms', methods=['GET'])
def get_classrooms():
    return jsonify(classroom)


#get method for teacher 
@app.route('/teachers', methods=['GET'])
def get_teachers():
    return jsonify(teacher)


#get method for child 
@app.route('/children', methods=['GET'])
def get_children():
    return jsonify(child)

# PUT method for all tables

#Put method for facility 
@app.route('/facilities/update', methods=['PUT']) #updates table 
def update_facility():
    data = request.json
    id = data.get('id')
    if id is None:
        return jsonify({'error message': 'No ID provided'}) #error message 

    for facil in facility:
        if facil['id'] == id:
            facil.update(data)
            return jsonify({'message of completion': 'The facility was updated successfully'}) #success message 

    return jsonify({'error message': 'Unfortunately the facility was not found'}) #error message


#Put method for classroom
@app.route('/classrooms/update', methods=['PUT']) #updates table 
def update_classroom():
    data = request.json
    id = data.get('id')
    if id is None:
        return jsonify({'error message': 'No ID provided'}) # error message 

    for clrm in classroom:
        if clrm['id'] == id:
            clrm.update(data)
            return jsonify({'completion message': 'The classroom was updated successfully'}) #success message 

    return jsonify({'error message': 'Unfortunately, the classroom was not found'}) #error message 


#Put method for teacher 
@app.route('/teachers/update', methods=['PUT']) #updates table 
def update_teacher():
    data = request.json
    id = data.get('id')
    if id is None:
        return jsonify({'error message': 'No ID was provided'}) #error message 
    for teach in teacher:
        if teach['id'] == id:
            teach.update(data)
            return jsonify({'message of completion': 'The teacher was updated successfully'}) #success message 

    return jsonify({'error message': 'Unfortunately the teacher provided was not found'})#error message 


#Put method for child 
@app.route('/children/update', methods=['PUT']) #updates table 
def update_child():
    data = request.json
    id = data.get('id')
    if id is None:
        return jsonify({'error message': 'No ID was provided'})# error message 

    for chld in child:
        if chld['id'] == id:
            chld.update(data)
            return jsonify({'message of completion': 'The child was updated successfully'}) #success message 

    return jsonify({'error message': 'Unfortunately, the child was not found'}) #error message 

#Delete method for each table 

# DELETE method for facility table 

@app.route('/facilities/delete', methods=['DELETE']) #deletes info 
def delete_facility():
    request_data = request.get_json()
    name_to_delete = request_data.get('name')
    if name_to_delete:
        for facil in facility:
            if facil['name'] == name_to_delete:
                facility.remove(facil)
                return jsonify({'message of completion': 'The facility was deleted successfully'}) #success message 
        return jsonify({'error message': 'Unfortunately, the facility was not found'}) # error message 
    else:
        return jsonify({'error message': 'Please provide the name of the facility to delete this information'}) #error message 


#Delete method for classroom
@app.route('/classrooms/delete', methods=['DELETE']) #deletes info 
def delete_classroom():
    request_data = request.get_json()
    name_to_delete = request_data.get('name')
    if name_to_delete:
        for clrm in classroom:
            if clrm['name'] == name_to_delete:
                classroom.remove(clrm)
                return jsonify({'message of completion': 'The classroom was deleted successfully'}) # success message 
        return jsonify({'error message': 'Unfortunately, the classroom was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the name of the classroom to delete this information'}) #error message 


#Delete method for teacher 
@app.route('/teachers/delete', methods=['DELETE']) #deletes info 
def delete_teacher():
    request_data = request.get_json()
    firstname_to_delete = request_data.get('firstname')
    lastname_to_delete = request_data.get('lastname')
    if firstname_to_delete and lastname_to_delete:
        for teach in teacher:
            if teach['firstname'] == firstname_to_delete and teach['lastname'] == lastname_to_delete:
                teacher.remove(teach)
                return jsonify({'message of completion': 'The teacher was deleted successfully'}) #sucess message 
        return jsonify({'error message': 'Unfortunately, the teacher was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the firstname and lastname of the teacher to delete this information'}) #error message 


#Delete method for child 
@app.route('/children/delete', methods=['DELETE']) #deletes info 
def delete_child():
    request_data = request.get_json()
    firstname_to_delete = request_data.get('firstname')
    lastname_to_delete = request_data.get('lastname')
    if firstname_to_delete and lastname_to_delete:
        for chld in child:
            if chld['firstname'] == firstname_to_delete and chld['lastname'] == lastname_to_delete:
                child.remove(chld)
                return jsonify({'message of completion': 'The child was deleted successfully'}) #success message
        return jsonify({'error message': 'Unfortunately, the child was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the firstname and lastname of the child to delete this information'}), #error message 



                                                        ##APIS for database##
# POST method for all tables in my database 

#Post method for facility in my database (Need to provide body for facility in postman)
@app.route('/api/facility/db', methods=['POST'])
def add_facility_to_db():
    #connecting to database 
    request_information = request.get_json()
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    name = request_information['name']
    sql = f"INSERT INTO facility(name) VALUES ('{name}')"
    execute_update_query(conn, sql)
    return 'The facility name provided was added to the database successfully!' #success message 


#Post method for classroom in my database (Need to provide body for classroom in postman)
@app.route('/api/classroom/db', methods=['POST'])
def add_classroom_to_db():
    #connecting to database 
    request_information = request.get_json()
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    capacity = request_information['capacity']
    name = request_information['name']
    facility = request_information['facility']
    sql = f"INSERT INTO classroom (capacity, name, facility) VALUES ('{capacity}', '{name}', {facility})"
    execute_update_query(conn, sql)
    return 'The classroom provided was added to the database successfully!' #success message 


#Post method for teacher in my database (Need to provide body for teacher in postman)
@app.route('/api/teacher/db', methods=['POST'])
def add_teacher_to_db():
    #connecting to database 
    request_information = request.get_json()
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    firstname = request_information['firstname']
    lastname = request_information['lastname']
    room = request_information['room']
    sql = f"INSERT INTO teacher (firstname, lastname, room) VALUES ('{firstname}', '{lastname}', {room})"
    execute_update_query(conn, sql)
    return 'The teacher provided was added to the database successfully!' #success message 


#Post method for child in my database (Need to provide body for child in postman)
@app.route('/api/child/db', methods=['POST'])
def add_child_to_db():
    #connecting to database 
    request_information = request.get_json()
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    firstname = request_information['firstname']
    lastname = request_information['lastname']
    age = request_information['age']
    room = request_information['room']
    sql = f"INSERT INTO child (firstname, lastname, age, room) VALUES ('{firstname}', '{lastname}', {age}, {room})"
    execute_update_query(conn, sql)
    return 'The child provided was added to the database successfully!' #success message 


#GET methods for all tables in my database


#Get method for facility table in my database
@app.route('/facilities/db', methods=['GET'])
def get_facilities_from_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM facility"
    facility_info = execute_sql_query(conn, sql)
    return jsonify(facility_info)


#GET  method for classrooom in my database 
@app.route('/classrooms/db', methods=['GET'])
#connecting to database 
def get_classrooms_from_db():
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM classroom"
    classroom_info = execute_sql_query(conn, sql)
    return jsonify(classroom_info)

#Get method for teacher in my database 
@app.route('/teachers/db', methods=['GET'])
def get_teachers_from_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM teacher"
    teacher_info = execute_sql_query(conn, sql)
    return jsonify(teacher_info)

#Get method for child in my database 
@app.route('/children/db', methods=['GET'])
def get_children_from_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = "SELECT * FROM child"
    child_info = execute_sql_query(conn, sql)
    return jsonify(child_info)


#PUT method for all tables in my database 

# PUT method for facility in my database (Need to provide body for facility in postman)
@app.route('/facilities/update/db', methods=['PUT'])
def update_facility_in_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    data = request.json
    id = data.get('id')  
    name = data.get('name')
    if id is None or name is None:
        return jsonify({'error': 'ID and name are required'})
    sql = f"UPDATE facility SET name = '{name}' WHERE id = {id}"
    execute_update_query(conn, sql)
    return jsonify({'message of completion': 'The facility was updated successfully'}) #success message 

# PUT method for classroom in my database (Need to provide body for classroom in postman)
@app.route('/classrooms/update/db', methods=['PUT'])
def update_classroom_in_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    data = request.json
    id = data.get('id')
    capacity = data.get('capacity')
    name = data.get('name')
    facility = data.get('facility')
    if id is None or capacity is None or name is None or facility is None:
        return jsonify({'error': 'ID, capacity, name, and facility are required'})
    sql = f"UPDATE classroom SET capacity = '{capacity}', name = '{name}', facility = {facility} WHERE id = {id}"
    execute_update_query(conn, sql)
    return jsonify({'message of completion': 'The classroom was updated successfully'}) #success message 

# PUT method for teacher in my database (Need to provide body for teacher in postman)
@app.route('/teachers/update/db', methods=['PUT'])
def update_teacher_in_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    data = request.json
    id = data.get('id')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    room = data.get('room')
    if id is None or firstname is None or lastname is None or room is None:
        return jsonify({'error message': 'ID, firstname, lastname, and room are required'})
    sql = f"UPDATE teacher SET firstname = '{firstname}', lastname = '{lastname}', room = {room} WHERE id = {id}"
    execute_update_query(conn, sql)
    return jsonify({'message of completion': 'The teacher was updated successfully'}) #success message 

# PUT method for child in my database (Need to provide body for child in postman)
@app.route('/children/update/db', methods=['PUT'])
def update_child_in_db():
    #connecting to database 
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    data = request.json
    id = data.get('id')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    room = data.get('room')
    if id is None or firstname is None or lastname is None or age is None or room is None:
        return jsonify({'error message': 'ID, firstname, lastname, age, and room are required'})
    sql = f"UPDATE child SET firstname = '{firstname}', lastname = '{lastname}', age = {age}, room = {room} WHERE id = {id}"
    execute_update_query(conn, sql)
    return jsonify({'message of completion': 'The child was updated successfully'}) #success message 



#Delete methods for all tables in my database
#delete method for facility (Put facility info in postman to delete)
@app.route('/facilities/delete/db', methods=['DELETE'])
def delete_facility_in_db():
    #connecting to database 
    request_data = request.get_json()
    name_to_delete = request_data.get('name')
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = f"DELETE FROM facility WHERE id = {id}"
    execute_update_query(conn, sql)
    if name_to_delete:
        for facil in facility:
            if facil['name'] == name_to_delete:
                facility.remove(facil)
                return jsonify({'message of completion': 'The facility was deleted successfully'}) #success message 
        return jsonify({'error message': 'Unfortunately, the facility was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the name of the facility to delete this information'}) #error message 


#Delete method for classroom (Put classroom info in postman to delete)
@app.route('/classrooms/delete/db', methods=['DELETE'])
def delete_classroom_in_db():
    #connecting to database 
    request_data = request.get_json()
    name_to_delete = request_data.get('name')
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = f"DELETE FROM classroom WHERE id = {id}"
    execute_update_query(conn, sql)
    if name_to_delete:
        for clrm in classroom:
            if clrm['name'] == name_to_delete:
                classroom.remove(clrm)
                return jsonify({'message of completion': 'The classroom was deleted successfully'}) #success message 
        return jsonify({'error message': 'Unfortunately, the classroom was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the name of the classroom to delete this information'}) #error message 


#Delete method for teacher (Put teacher info in postman to delete)
@app.route('/teachers/delete/db', methods=['DELETE'])
def delete_teacher_in_db():
    #connecting to datanase 
    request_data = request.get_json()
    firstname_to_delete = request_data.get('firstname')
    lastname_to_delete = request_data.get('lastname')
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = f"DELETE FROM teacher WHERE id = {id}"
    execute_update_query(conn, sql)
    if firstname_to_delete and lastname_to_delete:
        for teach in teacher:
            if teach['firstname'] == firstname_to_delete and teach['lastname'] == lastname_to_delete:
                teacher.remove(teach)
                return jsonify({'message of completion': 'The teacher was deleted successfully'}) #success message
        return jsonify({'error message': 'Unfortunately, the teacher was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the firstname and lastname of the teacher to delete this information'}) #error message 

#Delete method for child (Put child info in postman to delete)
@app.route('/children/delete/db', methods=['DELETE'])
def delete_child_in_db():
    #connecting to database 
    request_data = request.get_json()
    firstname_to_delete = request_data.get('firstname')
    lastname_to_delete = request_data.get('lastname')
    conn = creating_connection(credssprint.Creds.myhostname, credssprint.Creds.username, credssprint.Creds.pwd, credssprint.Creds.dbname)
    sql = f"DELETE FROM child WHERE id = {id}"
    execute_update_query(conn, sql)
    if firstname_to_delete and lastname_to_delete:
        for chld in child:
            if chld['firstname'] == firstname_to_delete and chld['lastname'] == lastname_to_delete:
                child.remove(chld)
                return jsonify({'message of completion': 'The child was deleted successfully'}) #success message 
        return jsonify({'error message': 'Unfortunately, the child was not found'}) #error message 
    else:
        return jsonify({'error message': 'Please provide the firstname and lastname of the child to delete this information'}) #error message 

app.run()


###THIS CODE IMPLEMENTS CODE FROM HW 2 AND MY CLASS NOTES###
