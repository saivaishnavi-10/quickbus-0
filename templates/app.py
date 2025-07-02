from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy bus data
bus_data = [
    {'id': 1, 'operator': 'APSRTC', 'type': 'Volvo', 'price': 500},
    {'id': 2, 'operator': 'TSRTC', 'type': 'Deluxe', 'price': 400},
    {'id': 3, 'operator': 'Private', 'type': 'AC', 'price': 600},
]

# In-memory user storage
users = {
    'admin@quickbus.com': 'admin123'
}

# Homepage
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def home():
    return render_template('index.html')

# Search results
@app.route('/search', methods=['POST'])
def search():
    from_location = request.form.get('from')
    to_location = request.form.get('to')
    journey_date = request.form.get('travelDate')
    return render_template('search_results.html', buses=bus_data,
                           from_location=from_location, to_location=to_location,
                           journey_date=journey_date)

# Booking/payment route
@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    selected_bus = next((bus for bus in bus_data if bus['id'] == bus_id), None)
    if not selected_bus:
        return "Bus not found", 404

    if request.method == 'POST':
        name = request.form['name']
        seats = int(request.form['seats'])
        student_id = request.form.get('student_id')

        base_price = selected_bus['price'] * seats
        discount = 0.2 * base_price if student_id else 0
        total = base_price - discount

        # You can store this in session/database if needed

        return redirect(url_for('ticket'))

    return render_template('payment.html', bus=selected_bus)

# Ticket confirmation
@app.route('/ticket')
@app.route('/ticket.html')
def ticket():
    return render_template('ticket.html')

# Offers page
@app.route('/offers')
@app.route('/offers.html')
def offers():
    return render_template('offers.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email] == password:
            return redirect(url_for('home'))
        else:
            error = "Invalid email or password"
            return render_template('login.html', error=error)

    return render_template('login.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            error = "User already exists. Try logging in."
            return render_template('register.html', error=error)
        else:
            users[email] = password
            return redirect(url_for('login'))

    return render_template('register.html')

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # You can store/send this message
        return render_template('contact.html', success=True)
    return render_template('contact.html')

# Optional payment route
@app.route('/payment')
@app.route('/payment.html')
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
