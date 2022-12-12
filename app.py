from flask import Flask, render_template, request, url_for, redirect, session, flash
import mysql
from mysql import connector
import datetime

app = Flask(__name__)


conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='air_ticket')


@app.route('/')
def publicHome():
 return render_template('publicHome.html')

@app.route('/publicSearchFlight', methods=['GET', 'POST'])
def publicSearchFlight():
 departure_airport = request.form['departure_airport']
 arrival_airport = request.form['arrival_airport']
 departure_date = request.form['departure_date']
 arrival_date = request.form['arrival_date']
 departure_city = request.form['departure_city']
 arrival_city =request.form['arrival_city']

 cursor = conn.cursor()

 query = "SELECT flight_number, airline_name, departure_airport, departure_city, departure_time, arrival_airport, arrival_city, arrival_time, price, airplane_id \
   FROM flight \
   WHERE departure_airport = if (\'{}\' = '', departure_airport, \'{}\') AND \
                                 arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') AND status = 'upcoming' AND\
                                 date(departure_time) = if (\'{}\' = '',date(departure_time), \'{}\') AND \
                                date(arrival_time) = if (\'{}\' = '',date(arrival_time), \'{}\') AND\
                                departure_city = if (\'{}\' = '', departure_city, \'{}\') AND\
                                arrival_city = if (\'{}\' = '', arrival_city, \'{}\') "
                                                         
 cursor.execute(query.format(departure_airport, departure_airport, arrival_airport, arrival_airport,  departure_date, departure_date, arrival_date, arrival_date, departure_city, departure_city, arrival_city, arrival_city))
 data = cursor.fetchall() 
 cursor.close()
    
 if (data): 
  return render_template('publicHome.html', upcoming_flights=data)
 else: 
		msg = 'Sorry, we cannot find this flight.'
		return render_template('publicHome.html', error1=msg)



@app.route('/publicSearchStatus', methods=['GET', 'POST'])
def publicSearchStatus():
 airline_name=request.form['airline_name']
 flight_num = request.form['flight_num']
 arrival_date = request.form['arrival_date']
 departure_date = request.form['departure_date']

 cursor = conn.cursor()
 query = "SELECT airline_name, flight_number, departure_airport, departure_city, departure_time, arrival_airport, departure_city, arrival_time, price, status, airplane_id \
   FROM flight \
   WHERE flight_number = if (\'{}\' = '', flight_number, \'{}\') and date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') and date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') and airline_name = if (\'{}\' = '', airline_name, \'{}\') " 
 cursor.execute(query.format(flight_num, flight_num, arrival_date, arrival_date, departure_date, departure_date, airline_name, airline_name))
 data = cursor.fetchall() 
 cursor.close()
 
 if (data): 
  return render_template('publicHome.html', statuses=data)
 else: 
  msg = 'Sorry, we cannot find this flight.'
  return render_template('publicHome.html', error2=msg)

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/cuslogin')

@app.route('/cuslogin')
def cuslogin():
	return render_template('cuslogin.html')


@app.route('/cusregister')
def cusregister():
	return render_template('cusregister.html')

@app.route('/cusloginAuth', methods=['GET', 'POST'])
def cusloginAuth():
	if "email" in request.form and 'password' in request.form:
		email = request.form['email']
		pwd = request.form['password']

		cursor = conn.cursor()
		query = "SELECT * FROM customer WHERE email = \'{}\' and  password = md5(\'{}\')"
		cursor.execute(query.format(email, pwd))
		data1 = cursor.fetchone()
		cursor.close()
		if data1:
			session['email'] = email
			cursor = conn.cursor()
			query = "SELECT ticket_id, airline_name, airplane_id, flight_number, d.airport_city, departure_airport, a.airport_city, arrival_airport, departure_time, arrival_time, status \
				FROM purchase natural join flight natural join ticket, airport as d, airport as a\
					WHERE customer_email = \'{}\' and status = 'upcoming' and \
					d.airport_name = departure_airport and a.airport_name = arrival_airport"
			cursor.execute(query.format(email))
			data2 = cursor.fetchall() 
			cursor.close()
			return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data2)
		else:
			msg = 'The email address or password is not correct!'
			return render_template('cuslogin.html', error=msg)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/cusregisterAuth', methods=['GET', 'POST'])
def cusregisterAuth():
	if "email" in request.form and \
		'name' in request.form and \
		'password' in request.form and \
		'building_number' in request.form and \
		'street' in request.form and \
		'city' in request.form and \
		'state' in request.form and \
		'phone_number' in request.form and \
		'passport_number' in request.form and \
		'passport_expiration' in request.form and \
		'passport_country' in request.form and \
		'date_of_birth' in request.form:
		email = request.form['email']
		name = request.form['name']
		pwd = request.form['password']
		building_number = request.form['building_number']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		phone_number = request.form['phone_number']
		passport_number = request.form['passport_number']
		passport_expiration = request.form['passport_expiration']
		passport_country = request.form['passport_country']
		dob = request.form['date_of_birth']

		cursor = conn.cursor()
		query = "SELECT * FROM customer WHERE email = \'{}\'"
		cursor.execute(query.format(email))
		data1 = cursor.fetchone()
		if data1:
			cursor.close()
			msg = "The email has already existed!"
			return render_template('cusregister.html', error = msg)
		else:

			ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
			cursor.execute(ins.format(email, name, pwd, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, dob))
			conn.commit()
			query = "SELECT ticket_id, airline_name, airplane_id, flight_number, d.airport_city, \
				departure_airport, a.airport_city, arrival_airport, departure_time, arrival_time, status \
					FROM purchase natural join flight natural join ticket, airport as d, airport as a\
						WHERE customer_email = \'{}\' and status = 'upcoming' and \
						d.airport_name = departure_airport and a.airport_name = arrival_airport"
			cursor.execute(query.format(email))
			data2 = cursor.fetchall() 
			cursor.close()
			flash('You have successfully registered! Log in to view your homepage.')
			session['email'] = email
			return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/cushome')
def cushome():
	if session.get('email'):
		email = session['email']

		cursor = conn.cursor()
		query = "SELECT ticket_id, airline_name, airplane_id, flight_number, d.airport_city, \
			departure_airport, a.airport_city, arrival_airport, departure_time, arrival_time, status \
				FROM purchase natural join flight natural join ticket, airport as d, airport as a\
					WHERE customer_email = \'{}\' and status = 'upcoming' and \
					d.airport_name = departure_airport and a.airport_name = arrival_airport"
		cursor.execute(query.format(email))
		data = cursor.fetchall() 
		cursor.close()
		return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data)
	else:
		session.clear()
		return render_template('404.html')
    

@app.route('/agentlogin')
def agentlogin():
	return render_template('agentlogin.html')

@app.route('/agentregister')
def agentregister():
	return render_template('agentregister.html')

@app.route('/agentloginAuth', methods=['GET', 'POST'])
def agentloginAuth():
	if "email" in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']

		cursor = conn.cursor()
		query = "SELECT * FROM booking_agent WHERE email = \'{}\' and password = md5(\'{}\') "
		cursor.execute(query.format(email, password))
		data1 = cursor.fetchone()
		cursor.close()
		if data1:
			session['email'] = email
			cursor = conn.cursor()
			query = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
			cursor.execute(query.format(email))
			data = cursor.fetchall()
			query2 = "SELECT booking_agent_id, ticket_id, customer_email, purchase.date, airline_name, flight_number, \
                departure_city, departure_airport,  departure_time, arrival_city, arrival_airport, \
                    arrival_time, price FROM flight NATURAL JOIN purchase NATURAL JOIN ticket \
                    NATURAL JOIN booking_agent WHERE booking_agent.email = \'{}\' and status = 'upcoming' \
                    and datediff(CURDATE(), DATE(departure_time)) < 30"
			cursor.execute(query2.format(email))
			data2 = cursor.fetchall()            
			cursor.close()
			return render_template('agenthome.html', email=email, emailName=email.split('@')[0], data2=data2, bid=data[0][0])
		else:
			msg = 'The email address or password is not correct!'
			return render_template('agentlogin.html', error=msg)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/agentregisterAuth', methods=['GET', 'POST'])
def agentregisterAuth():
	if "email" in request.form and 'password' in request.form and 'booking_agent_id' in request.form:
		email = request.form['email']
		pwd = request.form['password']
		booking_agent_id = request.form['booking_agent_id']

		cursor = conn.cursor()
		query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
		cursor.execute(query.format(email))
		data1 = cursor.fetchone()
		if data1:
			cursor.close()
			error = "This email has already existed!"
			return render_template('agentregister.html', error = error)
		else:
			ins = "INSERT INTO booking_agent VALUES(\'{}\',md5(\'{}\'), \'{}\')"
			cursor.execute(ins.format(email, pwd, booking_agent_id))
			conn.commit()
			query = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
			cursor.execute(query.format(email))
			data2 = cursor.fetchall()
			cursor.close()
			flash("You have successfully registered! Log in to view your homepage.")
			session['email'] = email
			return render_template('agenthome.html', email=email, emailName=email.split('@')[0], bid=data2[0][0])
	else:
		session.clear()
		return render_template('404.html')


@app.route('/agenthome')
def agentHome():
	if session.get('email'):
		email = session['email']
			
		cursor = conn.cursor()
		query = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
		cursor.execute(query.format(email))
        
		data1 = cursor.fetchall()
		query2 = "SELECT booking_agent_id, ticket_id, customer_email, purchase.date, airline_name, flight_number, \
            departure_city, departure_airport,  departure_time, arrival_city, arrival_airport, \
                arrival_time, price FROM flight NATURAL JOIN purchase NATURAL JOIN ticket \
                NATURAL JOIN booking_agent WHERE booking_agent.email = \'{}\' and status = 'upcoming' \
                and datediff(CURDATE(), DATE(departure_time)) < 30;"
		cursor.execute(query2.format(email))
		data2 = cursor.fetchall()
		cursor.close()
		return render_template('agenthome.html', email=email, emailName=email.split('@')[0], data2=data2, bid=data1[0][0])
	else:
		session.clear()
		return render_template('404.html')
    
    

@app.route('/stafflogin')
def stafflogin():
	return render_template('stafflogin.html')

@app.route('/staffregister')
def staffregister():
	return render_template('staffregister.html')

@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
	if "username" in request.form and 'password' in request.form:
		username = request.form['username']
		pwd = request.form['password']

		cursor = conn.cursor()
		query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = md5(\'{}\')"
		cursor.execute(query.format(username, pwd))
		data1 = cursor.fetchone()
        
		if data1:
			cursor=conn.cursor()            
			session['username'] = username
			query1 = "SELECT username, airline_name, airplane_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, remaining_tickets FROM flight NATURAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(CURDATE(), CURDATE()) < 30 "            
			cursor.execute(query1.format(username))
			data2 = cursor.fetchall()                    
            
			query2 = "select permission, airline_name from airline_staff WHERE username = \'{}\' "   
			cursor.execute(query2.format(username))
			data3 = cursor.fetchall()          
            
			query3 = "select airline_name from airline_staff where username=\'{}\'"               
			cursor.execute(query3.format(username))            
			airline_name = cursor.fetchall() 
            
			query4 = "select username, permission from airline_staff where airline_name=\'{}\'"               
			cursor.execute(query4.format(airline_name[0][0]))
			data4 = cursor.fetchall()                      
            
            
			cursor.close()             
            
			return render_template('staffhome.html', username=username, posts = data2, permission=data3,staffinfo=data4)
		else:
			msg = 'The email address or password is not correct!'
			return render_template('stafflogin.html', error=msg)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffregisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
	if "username" in request.form and \
		"password" in request.form and \
		"first_name" in request.form and \
		"last_name" in request.form and \
		"date_of_birth" in request.form and \
		"airline_name" in request.form:
            
		username = request.form['username']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		date_of_birth = request.form['date_of_birth']
		airline_name = request.form['airline_name']

		cursor = conn.cursor()
        
		query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchone()
		
		msg1 = "This username has already existed!"
		msg2 = "This airline does not exist!"
        
		if data1:
			cursor.close()            
			return render_template('staffregister.html', error = msg1)
		
		query = "SELECT airline_name FROM airline WHERE airline_name = \'{}\'"
		cursor.execute(query.format(airline_name))
		data2 = cursor.fetchone()
		
		if data2:
			ins = "INSERT INTO airline_staff VALUES(\'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', 'staff')"
			cursor.execute(ins.format(username, password, first_name, last_name, date_of_birth, airline_name))
			conn.commit()
			query = "SELECT username, airline_name, airplane_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, remaining_tickets FROM flight NATURAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(DATE(departure_time), CURDATE()) < 30 "
			cursor.execute(query.format(username))
			data3 = cursor.fetchall()

            
			query2 = "select permission, airline_name from airline_staff WHERE username = \'{}\' "   
			cursor.execute(query2.format(username))
			data4 = cursor.fetchall()    

            
			query4 = "select username, permission from airline_staff where airline_name=\'{}\'"               
			cursor.execute(query4.format(airline_name))
			data5 = cursor.fetchall()                     
            
			cursor.close()                 
            
			flash("You have successfully registered! Log in to view your homepage.")
			session['username'] = username
			return render_template('staffhome.html', username=username, posts = data3,permission=data4,staffinfo=data5)
		else:
			cursor.close()
			return render_template('staffregister.html', error =msg2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffhome')
def staffhome():
	if session.get('username'):
		username = session['username']

		cursor = conn.cursor()
		query = "SELECT username, airline_name, airplane_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, remaining_tickets  \
				FROM flight NATURAL JOIN airline_staff \
				WHERE username = \'{}\' and status = 'upcoming' and datediff(CURDATE(), DATE(departure_time)) < 30 "
		cursor.execute(query.format(username))
		data = cursor.fetchall()

		query2 = "select permission, airline_name from airline_staff WHERE username = \'{}\' "   
		cursor.execute(query2.format(username))
		data3 = cursor.fetchall()  

            
		query3 = "select airline_name from airline_staff where username=\'{}\'"               
		cursor.execute(query3.format(username))            
		airline_name = cursor.fetchall() 
            
		query4 = "select username, permission from airline_staff where airline_name=\'{}\'"               
		cursor.execute(query4.format(airline_name[0][0]))
		data4 = cursor.fetchall()         


          
		cursor.close()
            
		return render_template('staffhome.html', username=username, posts=data,permission=data3,staffinfo=data4)
	else:
		session.clear()
		return render_template('404.html')
    

@app.route('/edit_permission', methods=['GET', 'POST'])
def edit_permission():
	if session.get('username'):
		username = session['username'] 
		staff_username = request.form['staff_username']        
		permission = request.form['edit_permission']
    
		

		cursor = conn.cursor()      

		query = "SELECT username, airline_name, airplane_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, remaining_tickets  \
				FROM flight NATURAL JOIN airline_staff \
				WHERE username = \'{}\' and status = 'upcoming' and datediff(CURDATE(), DATE(departure_time)) < 30 "
		cursor.execute(query.format(username))
		data = cursor.fetchall()

        
		query2 = "select permission, airline_name from airline_staff WHERE username = \'{}\' "   
		cursor.execute(query2.format(username))
		data3 = cursor.fetchall()  

		if data3[0][0] == 'admin':
                    upd = "UPDATE airline_staff set permission = \'{}\' WHERE username = \'{}\'"
                    cursor.execute(upd.format(permission,staff_username))
                    conn.commit()
                    msg = 'The status has successfully changed!'
		else:
                    msg = 'Sorry, You can not change staff permission since you are not admin.'
		query3 = "select airline_name from airline_staff where username=\'{}\'"               
		cursor.execute(query3.format(username))            
		airline_name = cursor.fetchall() 
            
		query4 = "select username, permission from airline_staff where airline_name=\'{}\'"               
		cursor.execute(query4.format(airline_name[0][0]))
		data4 = cursor.fetchall()         

		cursor.close()

		return render_template('staffhome.html', username=username, message = msg,posts=data,permission=data3,staffinfo=data4)
	else:
		session.clear()
		return render_template('404.html')
    
    
    
    

@app.route('/staffSearchFlight', methods=['GET', 'POST'])
def staffSearchFlight():
	if session.get('username'):
		departure_city = request.form['departure_city']
		departure_airport = request.form['departure_airport']
		arrival_city = request.form['arrival_city']
		arrival_airport = request.form['arrival_airport']
		departure_date = request.form['departure_date']
		arrival_date = request.form['arrival_date']
		username = session['username']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
				WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()
		query = "SELECT airline_name, airplane_id, flight_number,  departure_airport, departure_city, arrival_airport, arrival_city,  departure_time, arrival_time, status, price\
                    from flight \
                    WHERE departure_city = if (\'{}\' = '', departure_city, \'{}\') AND departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
                    arrival_city = if (\'{}\' = '', arrival_city, \'{}\') and arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') \
                    and date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') \
                    and date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') and airline_name = \'{}\' "
		cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date,arrival_date,data2[0][1]))
		data1 = cursor.fetchall()


		cursor.close()
		
		if data1: 
			return render_template('staffflight.html', username=username, upcoming_flights=data1, posts = data2)
		else:
			msg = 'Sorry, we cannot find this flight.'
			return render_template('staffflight.html', username=username, error1=msg, posts = data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffflight')
def staffflight():
	if session.get('username'):
		username = session['username'] 	
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('staffflight.html', username=username, posts = data)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffaddinfo')
def staffaddinfo():
	if session.get('username'):
		username = session['username'] 
		cursor = conn.cursor()

		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()

		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()
		cursor.close()

		return render_template('staffaddinfo.html', username=username, airplane = data2, posts = data1)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/edit_status', methods=['GET', 'POST'])
def edit_status():
	if session.get('username'):
		username = session['username'] 
		status = request.form['edit_status']
		flight_num = request.form['flight_num']
		cursor = conn.cursor()
		query_permission = "select permission, airline_name from airline_staff WHERE username = \'{}\' "
		cursor.execute(query_permission.format(username))
		permission = cursor.fetchall()
		if permission[0][0] == 'operator':
                    cursor = conn.cursor()
                    upd = "UPDATE flight set status = \'{}\' WHERE flight_number = \'{}\'"
                    cursor.execute(upd.format(status, flight_num))
                    conn.commit()

                    query = "SELECT username, airline_name FROM airline_staff \
                                    WHERE username = \'{}\'"
                    cursor.execute(query.format(username))
                    data = cursor.fetchall()

                    cursor.close()
                    msg = 'The status has successfully changed!'
                    return render_template('staffflight.html', username=username, message = msg, posts = data)
		else:
                    msg = 'Sorry, you can not change flight status beacuse your permission is not operator.'
                    query = "SELECT username, airline_name FROM airline_staff \
                                    WHERE username = \'{}\'"
                    cursor.execute(query.format(username))
                    data = cursor.fetchall()
                    cursor.close()
                    
                    return render_template('staffflight.html', username=username, message = msg, posts = data)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
	if session.get('username'):
		username = session['username']
		flight_num = request.form['flight_num']
		departure_airport = request.form['departure_airport']
		departure_date = request.form['departure_date']
		departure_time = request.form['departure_time']
		arrival_airport = request.form['arrival_airport']
		arrival_date = request.form['arrival_date']
		arrival_time = request.form['arrival_time']
		price = request.form['price']
		number = request.form['number']
		status = request.form['status']
		airplane_id = request.form['airplane_id']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		airline = "SELECT airline_name FROM airline_staff WHERE username = \'{}\'"
		cursor.execute(airline.format(username))

		airline_name = cursor.fetchone()
		airline_name = airline_name[0]


		query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
		cursor.execute(query.format(departure_airport))

		data = cursor.fetchall()
		error1 = None
		if not (data):
			error1 = "Departure airport doesn't exist"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1, posts = data2)

		query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
		cursor.execute(query.format(arrival_airport))
		data = cursor.fetchall()
		error1 = None
		if not (data):
			error1 = "Arrival airport doesn't exist"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1, posts = data2)
		num = "SELECT seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\' and airplane_id = \'{}\'"
		cursor.execute(num.format(username, airplane_id))
		num = cursor.fetchone()
		if int(number) > int(num[0]): 
			numerror = "Not enough seats"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			return render_template('staffaddinfo.html', error1 = numerror, username=username, airplane = data1, posts = data2)

		query = "SELECT airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
		cursor.execute(query.format(airline_name, airplane_id))
		data = cursor.fetchall()
		error1 = None
		if not (data):
			error1 = "Airplane doesn't exist"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1, posts = data2)

		num = "SELECT seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\' and airplane_id = \'{}\'"
		cursor.execute(num.format(username, airplane_id))
		num = cursor.fetchone()


		query = "SELECT airline_name, flight_number FROM flight WHERE airline_name = \'{}\' and flight_number = \'{}\'"
		cursor.execute(query.format(airline_name, flight_num))

		data = cursor.fetchone()
		error1 = None
		
		if(data):
			error1 = "This flight already exists"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			cursor.close()
			return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1, posts = data2)		

		else:
			query_permission = "select permission, airline_name from airline_staff WHERE username = \'{}\' "
			cursor.execute(query_permission.format(username))
			permission = cursor.fetchall()
			if permission[0][0] == 'admin':
                            query="select airport_city from airport where airport_name=\'{}\'"
                            cursor.execute(query.format(departure_airport))            
                            departure_city=cursor.fetchall()[0][0] 

                            query="select airport_city from airport where airport_name=\'{}\'"         

                            cursor.execute(query.format(arrival_airport))           
                            arrival_city=cursor.fetchall()[0][0]


                            ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{},{}\',  \'{},{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\',  \'{}\', \'{}\',\'{}\')"
                            cursor.execute(ins.format(airline_name, flight_num, departure_date, departure_time,arrival_date,arrival_time, price, status, airplane_id, departure_airport, arrival_airport,departure_city,arrival_city,number))

                            conn.commit()
                            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
                            cursor.execute(query.format(username))
                            data1 = cursor.fetchall()
                            cursor.close()
                            msg = "The new flight is successfully added!"

                            return render_template('staffaddinfo.html', message1 = msg, username=username, airplane = data1, posts = data2)
			else:
                            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
                            cursor.execute(query.format(username))
                            data1 = cursor.fetchall()
                            cursor.close()
                            msg = 'Sorry, you can not add flight beacuse your permission is not admin.'
                            return render_template('staffaddinfo.html', message1 = msg, username=username, airplane = data1, posts = data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	if session.get('username'):
		username = session['username']

		airplane_id = request.form['airplane_id']
		seats = request.form['seats']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		airline = "SELECT airline_name \
		FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(airline.format(username))

		airline_name = cursor.fetchone()

		query = "SELECT airline_name, airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
		cursor.execute(query.format(airline_name[0], airplane_id))

		data = cursor.fetchone()

		error2 = None
		if(data):

			error2 = "This airplane already exists"
			query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
			cursor.execute(query.format(username))
			data1 = cursor.fetchall()
			cursor.close()
			return render_template('staffaddinfo.html', error2 = error2, username=username, airplane = data1, posts = data2)
		else:
                    query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
                    cursor.execute(query.format(username))
                    data1 = cursor.fetchall()
                    query_permission = "select permission, airline_name from airline_staff WHERE username = \'{}\' "
                    cursor.execute(query_permission.format(username))
                    permission = cursor.fetchall()
                    if permission[0][0] == 'admin':
                        ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
                        cursor.execute(ins.format(airline_name[0], airplane_id, seats))

                        query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
                        cursor.execute(query.format(username))
                        data1 = cursor.fetchall()

                        conn.commit()
                        cursor.close()
                        msg = "The new airplane has successfully added!"

                        return render_template('staffaddinfo.html', message2 = msg, username=username, airplane = data1, posts = data2)
                    else:
                        cursor.close()
                        msg = 'Sorry, you can not add airplane beacuse your permission is not admin.'
                        return render_template('staffaddinfo.html', message2 = msg, username=username, airplane = data1, posts = data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	if session.get('username'):
		username = session['username']
		airport_name = request.form['airport_name']
		airport_city = request.form['airport_city']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		airport = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
		cursor.execute(airport.format(airport_name))
		airportdata = cursor.fetchone()
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()

		error3 = None
		if(airportdata):
			error3 = "This airport has already exists."
			return render_template('staffaddinfo.html', error3 = error3, username=username, airplane = data1, posts = data2)

		else:
                    query_permission = "select permission, airline_name from airline_staff WHERE username = \'{}\' "
                    cursor.execute(query_permission.format(username))
                    permission = cursor.fetchall()
                    if permission[0][0] == 'admin':
                        cursor = conn.cursor()
                        ins = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
                        cursor.execute(ins.format(airport_name, airport_city))
                        conn.commit()
                        cursor.close()
                        msg = "The new airport has successfully added!"
                        return render_template('staffaddinfo.html', message3 = msg, username=username, airplane = data1, posts = data2)
                    else:
                        cursor.close()
                        msg = 'Sorry, you can not add flight beacuse your permission is not admin.'
                        return render_template('staffaddinfo.html', message3 = msg, username=username, airplane = data1, posts = data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffagent')
def staffagent():
	if session.get('username'):
		username = session['username']
		cursor = conn.cursor()

		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		adata = cursor.fetchall()

		query1 = "SELECT email, booking_agent_id, sum(price) * 0.1 as commission FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN flight NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 365  \
				GROUP BY email, booking_agent_id \
					ORDER BY commission DESC\
						LIMIT 5 "
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()

		query2 = "SELECT booking_agent.email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 30 \
				GROUP BY email, booking_agent_id \
					ORDER BY ticket DESC LIMIT 5 "
		cursor.execute(query2.format(username))
		data2 = cursor.fetchall()

		query3 = "SELECT email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 365 \
				GROUP BY email, booking_agent_id \
					ORDER BY ticket DESC LIMIT 5 "
		cursor.execute(query3.format(username))
		data3 = cursor.fetchall()

		query = "SELECT email, booking_agent_id FROM booking_agent"
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()
		return render_template('staffagent.html', username=username, commission = data1, month = data2, year = data3, posts = data, adata = adata)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
	if session.get('username'):
		username = session['username']
        
		agent_email = request.form['agent_email']


		cursor = conn.cursor()

		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		adata = cursor.fetchall()

		query1 = "SELECT email, booking_agent_id, sum(price) * 0.1 as commission FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN flight NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 365  \
				GROUP BY email, booking_agent_id \
					ORDER BY commission DESC\
						LIMIT 5 "
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()

		query2 = "SELECT booking_agent.email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 30 \
				GROUP BY email, booking_agent_id \
					ORDER BY ticket DESC LIMIT 5 "
		cursor.execute(query2.format(username))
		data2 = cursor.fetchall()

		query3 = "SELECT email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchase \
			NATURAL JOIN ticket AS T, airline_staff \
			WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and datediff(CURDATE(), DATE(date)) < 365 \
				GROUP BY email, booking_agent_id \
					ORDER BY ticket DESC LIMIT 5 "
		cursor.execute(query3.format(username))
		data3 = cursor.fetchall()

		query = "SELECT email, booking_agent_id FROM booking_agent"
		cursor.execute(query)
		data = cursor.fetchall()
        
		query4 = "select airline_name from airline_staff where username=\'{}\'"               
		cursor.execute(query4.format(username))            
		airline_name_staff = cursor.fetchall()
        
        
        
		query5 = "select * from works_for where email=\'{}\' and airline_name=\'{}\'" 
		cursor.execute(query5.format(agent_email,airline_name_staff[0][0]))            
		check = cursor.fetchall()

            
            
       
		if(check):
			cursor.close()            
			msg = "This agent has already worked for your airline."
			return render_template('staffagent.html', error = msg, username=username, commission = data1, month = data2, year = data3, posts = data, adata = adata)

		else:
                    query_permission = "select permission, airline_name from airline_staff WHERE username = \'{}\' "
                    cursor.execute(query_permission.format(username))
                    permission = cursor.fetchall()

                    if permission[0][0] == 'admin':

                        ins = "INSERT INTO works_for VALUES(\'{}\', \'{}\')"
                        cursor.execute(ins.format(agent_email, airline_name_staff[0][0]))
                        conn.commit()
                        cursor.close()
                        msg = "The new agent has successfully added!"
                        return render_template('staffagent.html', error = msg, username=username, commission = data1, month = data2, year = data3, posts = data, adata = adata)
                    else:
                        cursor.close()

                        msg = 'Sorry, you can not add agent beacuse your permission is not admin.'
                        return render_template('staffagent.html', error = msg, username=username, commission = data1, month = data2, year = data3, posts = data, adata = adata)
	else:
		session.clear()
		return render_template('404.html')



@app.route('/staffcus')
def staffcus():
	if session.get('username'):
		username = session['username']
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		query1 = "SELECT email, name, count(ticket_id) as ticket FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
			WHERE email = customer_email AND username = \'{}\' and datediff(CURDATE(), DATE(date)) < 365\
			GROUP BY email, name\
			ORDER BY ticket DESC LIMIT 1"
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('staffcus.html', frequent = data1, username = username, cdata = data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffcusflight', methods=['GET', 'POST'])
def staffcusflight():
	if session.get('username'):
		username = session['username']
		email = request.form['customer_email']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		cdata = cursor.fetchall()

		query2 = "SELECT DISTINCT airplane_id, flight_number, \
			departure_airport, arrival_airport, departure_time, arrival_time, \
				status FROM customer, \
					purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
			WHERE email = \'{}\' and email = customer_email and username = \'{}\'"
		cursor.execute(query2.format(email, username))
		data2 = cursor.fetchall()

		query1 = "SELECT email, name, count(ticket_id) as ticket FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
			WHERE email = customer_email AND username = \'{}\' and datediff(CURDATE(), DATE(date)) < 365\
			GROUP BY email, name\
			ORDER BY ticket DESC LIMIT 1"
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()
		cursor.close()

		msg = None
		if(data2):
			return render_template('staffcus.html', cusflight = data2, frequent = data1, username = username, cdata = cdata)
		else:
			cursor = conn.cursor()
			cus = "SELECT email FROM customer WHERE email = \'{}\'"
			cursor.execute(cus.format(email))
			cus = cursor.fetchone()
			cursor.close()
			if(cus):
				msg = "The customer did not take any flight."
			else:
				msg = "The customer does not exist!"
			return render_template('staffcus.html', error = msg, frequent = data1, username = username, cdata = cdata)
	else:
		session.clear()
		return render_template('404.html')


	
@app.route('/staffDest')
def staffDest():
	if session.get('username'):
		username = session['username']

		cursor = conn.cursor()

		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()

		query1 = "SELECT airport_city, count(ticket_id) AS ticket FROM \
			purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
			WHERE airport_name = arrival_airport and datediff(CURDATE(), DATE(date)) < 90\
			GROUP BY airport_city\
			ORDER BY ticket DESC\
				LIMIT 3"
		cursor.execute(query1)
		month = cursor.fetchall()

		query2 = "SELECT airport_city, count(ticket_id) AS ticket FROM \
			purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
			WHERE airport_name = arrival_airport and datediff(CURDATE(), DATE(date)) < 365\
				GROUP BY airport_city\
			ORDER BY ticket DESC\
				LIMIT 3"
		cursor.execute(query2)
		year = cursor.fetchall()
		cursor.close()
		return render_template('staffDest.html', month = month, year = year, username = username, posts = data1)

	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffReve')
def staffReve():
	if session.get('username'):
		username = session['username']

		cursor = conn.cursor()
		
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		query3 = "SELECT sum(price)\
		FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE username = \'{}\' AND booking_agent_id is NULL AND datediff(CURDATE(), DATE(date)) < 30\
		GROUP BY airline_name"

		cursor.execute(query3.format(username))

		mdirect = cursor.fetchall()
		if(mdirect):
			mdirect = [int(mdirect[0][0])]
		else:
			mdirect = [0]
		

		query4 = "SELECT sum(price)\
		FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE username = \'{}\' AND booking_agent_id is NOT NULL AND datediff(CURDATE(), DATE(date)) < 30\
		GROUP BY airline_name"
		
		cursor.execute(query4.format(username))

		mindirect = cursor.fetchall()
		if(mindirect):
			mindirect = [int(mindirect[0][0])]
		else:
			mindirect = [0]
		mdata = {"Sales Type":"Sales"}
		mdata["Direct Sales"] = mdirect[0]
		mdata["Indirect Sales"] = mindirect[0]
		msum=mdirect[0]+mindirect[0]	    
		query5 = "SELECT sum(price)\
		FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE username = \'{}\' AND booking_agent_id is NULL AND datediff(CURDATE(), DATE(date)) < 365\
		GROUP BY airline_name"
		
		cursor.execute(query5.format(username))

		ydirect = cursor.fetchall()
		if(ydirect):
			ydirect = [int(ydirect[0][0])]
		else:
			ydirect = [0]

		query6 = "SELECT sum(price)\
		FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE username = \'{}\' AND booking_agent_id is NOT NULL AND datediff(CURDATE(), DATE(date)) < 365\
		GROUP BY airline_name"
		
		cursor.execute(query6.format(username))

		yindirect = cursor.fetchall()
		if(yindirect):
			yindirect = [int(yindirect[0][0])]
		else:
			yindirect = [0]

		ydata = {"Sales Type": "Sales"}
		ydata["Direct Sales"] = mdirect[0]
		ydata["Indirect Sales"]= mindirect[0]
		ysum=ydirect[0]+yindirect[0]		
		cursor.close()
		return render_template('staffReve.html', username = username, posts = data2, mdata=mdata, ydata=ydata, msum=msum, ysum=ysum)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staffTickets')
def staffTickets():
	if session.get('username'):
		username = session['username']

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()
		cursor.close()
		
		return render_template('staffTickets.html', username = username, posts = data2)
	else:
		session.clear()
		return render_template('404.html')



@app.route('/staffticket', methods=['GET', 'POST'])
def staffticket():
	if session.get('username'):
		username = session['username']
		start = request.form['start_date']
		end = request.form['end_date']
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airline_staff \
		WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()


		ticket = "SELECT YEAR(date) AS year, MONTH(date) AS month, count(ticket_id) FROM \
				purchase NATURAL JOIN airline_staff NATURAL JOIN flight NATURAL JOIN ticket\
				WHERE date > \'{}\'\
				and date < \'{}\' AND username = \'{}\' \
				GROUP BY year, month\
				ORDER BY year, month"
		cursor.execute(ticket.format(start, end, username))

		allticket = cursor.fetchall()

		cursor.close()
		data={"Month":"Num of Tickets Sold"}

		sumt = 0
		for i in allticket:
                    data[str(i[0])+'-'+str(i[1])] = int(i[2])
                    sumt+=int(i[2])


	else:
		session.clear()
		return render_template('404.html')


@app.route('/cusSearchPurchase')
def cusSearchPurchase():
	if session.get('email'):
		email = session['email'] 
		return render_template('cusSearchPurchase.html', email=email, emailName=email.split('@')[0])
	else:
		session.clear()
		return render_template('404.html')
    

@app.route('/cusSpending', methods=['POST', 'GET'])
def cusSpending():
	if session.get('email'):
		email = session['email']

		duration = request.form.get("duration")
		if duration is None:
			duration = "365"
		cursor = conn.cursor()
		query = "select sum(price)\
					from purchase natural join ticket natural join flight \
					where customer_email = \'{}\' and (date between DATE_ADD(NOW(), INTERVAL - \'{}\' DAY) and NOW())"
		cursor.execute(query.format(email, duration))
		total_spending_data = cursor.fetchone()
		cursor.close()

		period = request.form.get("period")
		if period is None:
			period = '6'
		today = datetime.date.today()
		past_day = today.day
		past_month = (today.month - int(period)) % 12
        
		if past_month == 0:
			past_month = 12
		past_year = today.year + ((today.month - int(period) - 1) // 12)
		past_date = datetime.date(past_year, past_month, past_day) 
        
		cursor = conn.cursor()
		query1 = "select year(date) as year, month(date) as month, sum(price) as monthly_spending \
					from purchase natural join ticket natural join flight \
					where customer_email = \'{}\' and (date between date(\'{}\') and NOW()) \
					group by year(date), month(date)"
		cursor.execute(query1.format(email, past_date))
		monthly_spending_data = cursor.fetchall()
		cursor.close()
		data={"Month":"Money Spent"}


		for i in monthly_spending_data:
                    data[str(i[0])+'-'+str(i[1])] = int(i[2])

		return render_template('cusSpending.html', email=email, emailName=email.split('@')[0], total_spending_data=total_spending_data[0], data = data, duration=duration, period=period, date=past_date)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/cusSearchFlight', methods=['GET', 'POST'])
def cusSearchFlight():
	if session.get('email'):
		email = session['email']
		departure_city = request.form['departure_city']
		departure_airport = request.form['departure_airport']
		arrival_city = request.form['arrival_city']
		arrival_airport = request.form['arrival_airport']
		departure_date = request.form['departure_date']
		arrival_date = request.form['arrival_date']

		cursor = conn.cursor()
		query1 = "SELECT airline_name, airplane_id, flight_number,  departure_city, departure_airport, arrival_city, arrival_airport,  departure_time, arrival_time, price, status, remaining_tickets\
                    from flight \
                    WHERE departure_city = if (\'{}\' = '', departure_city, \'{}\') AND departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
                    arrival_city = if (\'{}\' = '', arrival_city, \'{}\') and arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') \
                    and date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') \
                    and date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\')"
		cursor.execute(query1.format(departure_city,departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date,arrival_date))
		data = cursor.fetchall()
		cursor.close()
		
		if (data):
			return render_template('cusSearchPurchase.html', email = email, emailName=email.split('@')[0], upcoming_flights=data)
		else:
			error = 'The flight does not exist!'
			return render_template('cusSearchPurchase.html', email = email, emailName=email.split('@')[0], error1=error)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/cusBuyTickets', methods=['GET', 'POST'])
def cusBuyTickets():
	if session.get('email'):
		email = session['email']
		airline_name = request.form['airline_name']
		flight_num = request.form['flight_num']

		cursor = conn.cursor()

		query = "SELECT * \
				FROM flight \
				WHERE airline_name = \'{}\' AND flight_number = \'{}\' AND remaining_tickets > 0"
		cursor.execute(query.format(airline_name, flight_num))

		data = cursor.fetchall()

		if(data):
			query_id = "SELECT ticket_id \
						FROM ticket \
						ORDER BY ticket_id DESC \
						LIMIT 1"
			cursor.execute(query_id)
			ticket_id_data = cursor.fetchone() 
			new_ticket_id = int(ticket_id_data[0]) + 1

			ins1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
			cursor.execute(ins1.format(new_ticket_id, airline_name, flight_num))

			ins2 = "INSERT INTO purchase VALUES (\'{}\', \'{}\', NULL, CURDATE())"
			cursor.execute(ins2.format(new_ticket_id, email))
			upd = "UPDATE flight set remaining_tickets = \'{}\' WHERE flight_number = \'{}\'"
			cursor.execute(upd.format(int(data[0][-1])-1, flight_num))
			conn.commit()
			cursor.close()
			msg = 'You have bought successfully the ticket!'
			return render_template('cusSearchPurchase.html', email = email, message1 = msg, data=data)
		else:
			msg = 'Sorry, no ticket left!'
			return render_template('cusSearchPurchase.html', error2=msg, email = email, emailName=email.split('@')[0])
	else:
		session.clear()
		return render_template('404.html')

   
@app.route('/agentSearchPurchase')
def agentSearchPurchase():
	if session.get('email'):
		email = session['email'] 
		return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], )
	else:
		session.clear()
		return render_template('404.html')

@app.route('/agentCommission', methods=['POST', 'GET'])
def agentCommission():
	if session.get('email'):
		email = session['email']

		cursor = conn.cursor()
		duration = request.form.get("duration")
		if duration is None:
			duration = "30"
		query = 'select sum(price * 0.1), avg(price * 0.1), count(price * 0.1) \
                  from flight natural join ticket natural join purchase natural join booking_agent \
                where email = \'{}\' and (date between DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())'
		cursor.execute(query.format(email, duration))
		commission_data = cursor.fetchone()
		total_com, avg_com, count_ticket = commission_data
		cursor.close()
		return render_template('agentCommission.html', email=email, emailName=email.split('@')[0], total_com=total_com, avg_com=avg_com, count_ticket=count_ticket, duration=duration)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/agentTopCustomers')
def agentTopCustomers():
	if session.get('email'):
		email = session['email']

		cursor = conn.cursor()
		query = "select customer_email, count(ticket_id) \
				from flight natural join ticket natural join purchase natural join booking_agent where email = \'{}\' and \
				datediff(CURDATE(), DATE(date)) < 182 \
				group by customer_email \
				order by count(ticket_id) desc"
		cursor.execute(query.format(email))
		ticket_data = cursor.fetchall()
		cursor.close()

		ppl1={'Customer Email':'Num of Tickets Bought'}
		for i in ticket_data:
                    ppl1[str(i[0])] = int(i[1])

		
		cursor = conn.cursor()
		query2 = "select customer_email, sum(price) * 0.1 \
				from flight natural join ticket natural join purchase natural join booking_agent where email = \'{}\' and \
				datediff(CURDATE(), DATE(date)) < 365 \
				group by customer_email \
				order by sum(price) desc"
		cursor.execute(query2.format(email))
		commission_data = cursor.fetchall()
		cursor.close()

		ppl2={'Customer Email':'Commission Spent'}
		for j in commission_data:
                    ppl2[str(j[0])] = int(j[1])
		return render_template('agentTopCustomers.html', email=email, emailName=email.split('@')[0], ppl1=ppl1, ppl2=ppl2, tickets=ticket_data, commissions=commission_data)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/agentSearchFlight', methods=['GET', 'POST'])
def agentSearchFlight():
	if session.get('email'):
		email = session['email']
		departure_city = request.form['departure_city']
		departure_airport = request.form['departure_airport']
		arrival_city = request.form['arrival_city']
		arrival_airport = request.form['arrival_airport']
		departure_date = request.form['departure_date']
		arrival_date = request.form['arrival_date']

		cursor = conn.cursor()
		query = "select booking_agent_id from booking_agent where email = \'{}\'"
		cursor.execute(query.format(email))
		agent_data = cursor.fetchone() 

		cursor.close()

		if not (agent_data):
			agent_id_error = 'The booking agent ID does not exist!'
			return render_template('agentSearchPurchase.html', error1=agent_id_error)

		cursor = conn.cursor()
		query = "SELECT airline_name, airplane_id, flight_number,  departure_airport, departure_city, arrival_airport, arrival_city,  departure_time, arrival_time, status, price, remaining_tickets\
                    from flight \
                    WHERE departure_city = if (\'{}\' = '', departure_city, \'{}\') AND departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
                    arrival_city = if (\'{}\' = '', arrival_city, \'{}\') and arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') \
                    and date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') \
                    and date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') and airline_name in (select airline_name FROM works_for \
				WHERE email = \'{}\')"
		cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date, arrival_date,email))
		data = cursor.fetchall()
		cursor.close()
		
		if (data): 
			return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], upcoming_flights=data)
		else: 
			error = 'The flight does not exist!'
			return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], error1=error)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/agentBuyTickets', methods=['GET', 'POST']) 
def agentBuyTickets():
	if session.get('email'):
		email = session['email']
		airline_name = request.form.get("airline_name")
		flight_num = request.form.get("flight_num")
		customer_email = request.form['customer_email']

		cursor = conn.cursor()
		query = "select booking_agent_id from booking_agent where email = \'{}\'"
		cursor.execute(query.format(email))
		agent_data = cursor.fetchone() 
		booking_agent_id = agent_data[0]
		cursor.close()

		if not (agent_data):
			agent_id_error = 'The booking agent ID does not exist!'
			return render_template('agentSearchPurchase.html', error2=agent_id_error)

		cursor = conn.cursor()
		query = "select * from customer where email = \'{}\'"
		cursor.execute(query.format(customer_email))
		cus_data = cursor.fetchone()
		cursor.close()

		if not (cus_data):
			email_error = 'The customer email does not exist!'
			return render_template('agentSearchPurchase.html', error2=email_error)

		cursor = conn.cursor()
		query = "SELECT * \
				FROM flight \
				WHERE airline_name = \'{}\' AND flight_number = \'{}\' AND remaining_tickets > 0"
		cursor.execute(query.format(airline_name, flight_num))
		flight_data = cursor.fetchall()

		if not (flight_data):
			ticket_error = 'Sorry, no ticket left!'
			return render_template('agentSearchPurchase.html', error2=ticket_error, email=email, emailName=email.split('@')[0])
		else:
                    query_worksfor = "select * from works_for WHERE email = \'{}\' and airline_name = \'{}\'"
                    cursor.execute(query_worksfor.format(email,airline_name))
                    permission = cursor.fetchall()
                    if permission:
                        cursor = conn.cursor()

                        cursor = conn.cursor()
                        query_id = "SELECT ticket_id FROM ticket ORDER BY ticket_id DESC LIMIT 1"
                        cursor.execute(query_id)
                        ticket_id_data = cursor.fetchone()
                        new_ticket_id = int(ticket_id_data[0]) + 1

                        ins1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
                        cursor.execute(ins1.format(new_ticket_id, airline_name, flight_num))

                        ins = "INSERT INTO purchase VALUES (\'{}\', \'{}\', \'{}\', CURDATE())"
                        cursor.execute(ins.format(new_ticket_id, customer_email, booking_agent_id))
                        upd = "UPDATE flight set remaining_tickets = \'{}\' WHERE flight_number = \'{}\'"
                        cursor.execute(upd.format(int(flight_data[0][-1])-1, flight_num, airline_name))
                        conn.commit()
                        cursor.close()
                        message = 'You have bought successfully the ticket!'
                        return render_template('agentSearchPurchase.html', message=message, email=email, emailName=email.split('@')[0])
                    else:
                        cursor.close()
                        message = 'Sorry, you cannot purchase tickets from airlines you are not working for.'
                        return render_template('agentSearchPurchase.html', message=message, email=email, emailName=email.split('@')[0])
                        
	else:
		session.clear()
		return render_template('404.html')
    





app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
 app.run('127.0.0.1', 5000, debug = True)
