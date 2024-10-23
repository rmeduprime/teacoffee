from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
#MAKE NECESSARY CHANGES MADAM
# Initialize database
def init_db():
    with sqlite3.connect('drink_counts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drink_counts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drink_type TEXT UNIQUE,
                count INTEGER
            )
        ''')
        conn.commit()
def display():
    conn = sqlite3.connect('drink_counts.db')

# Step 2: Create a cursor object
    cursor = conn.cursor()

# Step 3: Write a query to select all data from the "users" table
    query = "SELECT * FROM drink_counts"

# Step 4: Execute the query
    cursor.execute(query)

# Step 5: Fetch all the rows from the result
    rows = cursor.fetchall()

# Step 6: Display the data
# Print the column headers (optional)
    column_names = [description[0] for description in cursor.description]
    print(column_names)

# Loop through the rows and print each one
    for row in rows:
        print(row)

# Step 7: Close the connection
    conn.close()
# Function to get drink counts from the database
def get_drink_counts():
    with sqlite3.connect('drink_counts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT drink_type, count FROM drink_counts')
        rows = cursor.fetchall()
        return {drink: count for drink, count in rows}

# Function to update or insert drink counts in the database
def update_drink_count(drink_type):
    with sqlite3.connect('drink_counts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT count FROM drink_counts WHERE drink_type = ?', (drink_type,))
        row = cursor.fetchone()
        
        if row:
            # Update existing count
            cursor.execute('UPDATE drink_counts SET count = count + 1 WHERE drink_type = ?', (drink_type,))
        else:
            # Insert new drink type with count 1
            cursor.execute('INSERT INTO drink_counts (drink_type, count) VALUES (?, ?)', (drink_type, 1))
        
        conn.commit()

# Initialize database on startup
init_db()
display()


# List to store orders
orders = []

drink_counts = {
    'Full Tea': 0,
    'Half Tea': 0,
    'Full Coffee': 0,
    'Half Coffee': 0,
    'Full Lemon': 0,
    'Half Lemon': 0

}
 
@app.route('/')
def index():
    return render_template('index.html', orders=orders, drink_counts=drink_counts)

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    drink_type = request.form['drink_type']
   
    
    order = {
        'Name': name,
        'Drink': drink_type,
       
    }
    
    orders.append(order)
    if 'fulltea' in drink_type:
        drink_counts['Full Tea'] += 1
    
    if 'halftea' in drink_type:
        drink_counts['Half Tea'] += 1

    if 'fullcoffee' in drink_type:
        drink_counts['Full Coffee'] += 1

    if 'halfcoffee' in drink_type:
        drink_counts['Half Coffee'] += 1

    if 'fulllemontea' in drink_type:
        drink_counts['Full Lemon'] += 1

    if 'halflemontea' in drink_type:
        drink_counts['Half Lemon'] += 1  


    #halflemontea  
    #do for all drinks
    update_drink_count(drink_type)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
