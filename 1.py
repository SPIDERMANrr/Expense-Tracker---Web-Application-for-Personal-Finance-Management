from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'your_strong_secret_key'  # Replace with a strong, random string
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Expense {self.id}>"

@app.route('/')
def index():
    expenses = Expense.query.all()
    total_spent = sum(expense.amount for expense in expenses)
    monthly_limit = request.args.get('monthly_limit', type=float, default=0.0)

    if total_spent > monthly_limit:
        flash(f"You've exceeded your monthly limit of {monthly_limit}!")

    most_used_category = Expense.query.group_by(Expense.category).order_by(db.func.count('*').desc()).first()
    if most_used_category:
        most_used_category = most_used_category.category

    return render_template('index.html', expenses=expenses, total_spent=total_spent, most_used_category=most_used_category, monthly_limit=monthly_limit)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form['date']
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    monthly_limit = float(request.form['monthly_limit'])

    new_expense = Expense(date=date, amount=amount, category=category, description=description)
    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for('index', monthly_limit=monthly_limit))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)