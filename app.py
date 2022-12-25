import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Create SQLITE Database - myDb
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Library.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)

#Models
class Books(db.Model):
    id = db.Column("book_id",db.Integer, primary_key=True)
    bookName = db.Column(db.String(30))
    author = db.Column(db.String(30))
    yearPublished = db.Column(db.Integer)
    typeLoan = db.Column(db.Integer)
    books= db.relationship('Loans', backref='books')

    def __init__(self, bookName, author, yearPublished, typeLoan):
        self.bookName= bookName
        self.author = author
        self.yearPublished = yearPublished
        self.typeLoan = typeLoan


class Customers(db.Model):
    id = db.Column("customer_id",db.Integer, primary_key=True)
    customerName = db.Column(db.String(80))
    city = db.Column(db.String(120))
    age = db.Column(db.Integer)
    customerStatus = db.Column(db.String(10))
    customers= db.relationship('Loans', backref='customers')
   
    def __init__(self, customerName, city, age,customerStatus):
        self.customerName= customerName
        self.city = city
        self.age = age
        self.customerStatus = customerStatus

class Loans(db.Model):
    id = db.Column("loan_id",db.Integer, primary_key=True)
    CustomerID=db.Column(db.Integer,db.ForeignKey('customers.customer_id'))
    BookID = db.Column(db.Integer,db.ForeignKey('books.book_id'))
    Loandate = db.Column(db.String(50))
    Returndate = db.Column(db.String(50))
    loan_status = db.Column(db.String(50))
    

    def __init__(self,CustomerID, BookID, Loandate, Returndate,loan_status):
        self.CustomerID = CustomerID
        self.BookID = BookID
        self.Loandate = Loandate
        self.Returndate = Returndate
        self.loan_status =loan_status 
       
#Book Views
@app.route('/books/<id>',methods = ['GET','DELETE'])
@app.route('/books/',methods = ['POST','GET'])
def books(id=-1): 
    if request.method == 'POST': 
        request_data = request.get_json()
        bookName = request_data["bookName"]
        author = request_data["author"]
        yearPublished = request_data["yearPublished"]
        typeLoan = request_data["typeLoan"]
        newBook= Books(bookName,author,yearPublished,typeLoan)
        db.session.add (newBook)
        db.session.commit()
        return ("A book was added")
      

    if request.method == 'GET':
        res=[]
        for book in Books.query.all():
              res.append({"book_id":book.id,
              "bookName":book.bookName,
              "author":book.author,
              "yearPublished":book.yearPublished,
              "typeLoan":book.typeLoan})
        return (json.dumps(res))

    if request.method == 'DELETE':
        del_book= Books.query.get(id)
        db.session.delete(del_book)
        db.session.commit()
        return "A book was deleted"


#Customers Views
@app.route('/customers/<id>',methods = ['DELETE','PUT'])
@app.route('/customers/',methods = ['POST','GET'])
def customers(id=-1): 
    if request.method == 'POST': 
        request_data = request.get_json()
        customerName = request_data["customerName"]
        city = request_data["city"]
        age = request_data["age"]
        customerStatus = request_data["customerStatus"]
        newCustomer= Customers(customerName,city,age, customerStatus)
        db.session.add (newCustomer)
        db.session.commit()
        return ("A customer was added")
     

    if request.method == 'GET':
        res=[]
        for customer in Customers.query.all():
            res.append({"customer_id":customer.id,
            "customerName":customer.customerName,
            "city":customer.city,"age":customer.age,
            "customerStatus":customer.customerStatus})
        return (json.dumps(res))

    if request.method == 'DELETE':
        del_customer= Customers.query.get(id)
        db.session.delete(del_customer)
        db.session.commit()
        return "A customer was deleted"

    if request.method == 'PUT':
            request_data = request.get_json()
            updCustomer = Customers.query.get(id)
            if updCustomer:
                updCustomer.customerStatus=request_data["customerStatus"]
                db.session.commit()
            return "A customer was update "


#Loans Views
@app.route('/loans/<id>',methods=['DELETE'])
@app.route('/loans/',methods=['POST','GET'])
def loans(id=-1):
    if request.method == 'POST': 
        request_data = request.get_json()
        CustomerID = request_data["CustomerID"]
        BookID = request_data["BookID"]
        Loandate = request_data["Loandate"]
        Returndate = request_data["Returndate"]
        loan_status = request_data["loan_status"]
        newLoan= Loans(CustomerID,BookID,Loandate,Returndate,loan_status)
        db.session.add (newLoan)
        db.session.commit()
        return ("A loan was added")
       
    if request.method == 'GET': 
       res=[]
       for loan,book,customer in db.session.query(Loans,Books,Customers).join(Books).join(Customers):
                res.append({"loan_id":loan.id,
                        "CustomerID":loan.CustomerID,
                        "BookID":loan.BookID,
                        "typeLoan":book.typeLoan,
                        "bookName":book.bookName,
                        "Loandate":loan.Loandate,
                        "Returndate":loan.Returndate,
                        "loan_status":loan.loan_status,
                        "customerName":customer.customerName})
       return (json.dumps(res))   

        
    if request.method == 'DELETE':
        del_loan= Loans.query.get(id)
        db.session.delete(del_loan)
        db.session.commit()
        return "A book was returned"


if __name__ == '__main__':
     with app.app_context():db.create_all()
     app.run(debug = True)


