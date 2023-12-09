from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'job_portal',
}

@app.route('/')
def index():
    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs')
        job_listings = cursor.fetchall()
    return render_template('index.html', job_listings=job_listings)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        employer = request.form.get('employer')
        email = request.form.get('email')

        with mysql.connector.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO jobs (title, category, description, employer, email) VALUES (%s, %s, %s, %s, %s)',
                           (title, category, description, employer, email))
            connection.commit()
        message = 'Job posted successfully!'
        return redirect(url_for('index'))

    return render_template('post_job.html')

@app.route('/job/<int:job_id>')
def job_details(job_id):
    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs WHERE id = %s', (job_id,))
        job = cursor.fetchone()
    return render_template('job_details.html', job=job)

@app.route('/all_jobs')
def all_jobs():
    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs')
        all_jobs = cursor.fetchall()
    return render_template('all_jobs.html', all_jobs=all_jobs)

if __name__ == '__main__':
    app.run(debug=True)
