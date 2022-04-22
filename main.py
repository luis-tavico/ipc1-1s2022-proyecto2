from datetime import date
from flask import Flask, jsonify, request
from database import bankDatabase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def principal():
    return "<h1>Creando biblioteca web</h1>"

#########CREATE_BOOK########################
@app.route('/book', methods=['POST'])
def addBook():
    body = request.get_json()
    isbnLibroExistente = []
    try:
        if body.__class__ == list:
            for i in range(len(body)):
                book = body[i]
                if ('isbn' in book and 'author' in book and 'title' in book and 'year' and 'no_copies' in book and 'no_available_copies' in book):
                    if (bankDatabase.bookExists(book['isbn']) == None):
                        bankDatabase.addBook(book)
                    else:
                        isbnLibroExistente.append(book['isbn'])
                else:
                    return jsonify({'msg': '¡Error de sintaxis! Puede que algunos libros no se agregaron'}), 206
            if len(isbnLibroExistente) == 0:
                return jsonify({'msg': 'Libros agregado exitosamente'}), 200
            else:
                msg = {
                    'msg': f'El isbn {isbnLibroExistente} no se agrego, debido a que ya existe'}
                return jsonify(msg), 206
        elif body.__class__ == dict:
            book = body
            if ('isbn' in book and 'author' in book and 'title' in book and 'year' and 'no_copies' in book and 'no_available_copies' in book):
                if (bankDatabase.bookExists(book['isbn']) == None):
                    bankDatabase.addBook(book)
                    return jsonify({'msg': 'Libro agregado exitosamente'}), 200
                else:
                    msg = {'msg': f'El isbn {book["isbn"]} ya existe'}
                    return jsonify(msg), 400
            else:
                return jsonify({'msg': '¡Error de sintaxis! Libro no agregado'}), 400
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500

#########UPDATE_INFORMATION#################
@app.route('/book', methods=['PUT'])
def updateBook():
    body = request.get_json()
    try:
        if ('isbn' in body and ('author' in body or 'title' in body or 'year' in body)):
            if (bankDatabase.updateBook(body)):
                return jsonify({'msg': 'Libro actualizado exitosamente'}), 201
            else:
                return jsonify({'msg': 'No existe libro con ese isbn'}), 404
        else:
            return jsonify({'msg': '¡Error de sintaxis! Libro no actualizado'}), 400
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500

#########CONSULT_INFORMATION########################
@app.route('/book', methods=['GET'])
def getSpecificBook():
    Data = []
    añoActual = date.today().year
    author = request.args.get('author')
    title = request.args.get('title')
    year_from = request.args.get('year_from')
    year_to = request.args.get('year_to')

    try:
        Data = bankDatabase.getBooks()

        if (author != None):
            Data = bankDatabase.filterByAuthor(Data, author)
        if (title != None):
            Data = bankDatabase.filterByTitle(Data, title)
        if (year_from != None):
            Data = bankDatabase.filterByYear(Data, int(year_from), añoActual)
        if (year_to != None):
            Data = bankDatabase.filterByYear(Data, 0, int(year_to))
        
        return(jsonify(Data)), 200
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500

#########CREATE LENDER########################
@app.route('/person', methods=['POST'])
def addLender():
    cuiPrestamistaExistente = []
    body = request.get_json()
    try:
        if body.__class__ == dict:
            if ('cui' in body and 'last_name' in body and 'first_name' in body):
                if (bankDatabase.lenderExists(body['cui']) == None):
                    bankDatabase.addLender(body)
                    return jsonify({'msg': 'Prestamista agregado exitosamente'}), 200
                else:
                    return jsonify({'msg': 'Ya existe prestamista con ese cui'}), 400
            else:
                return jsonify({'msg': '¡Error de sintaxis! Prestamista no agregado'}), 400
        elif body.__class__ == list:
            for i in range(len(body)):
                lender = body[i]
                if ('cui' in lender and 'last_name' in lender and 'first_name' in lender):
                    if (bankDatabase.lenderExists(lender['cui']) == None):
                        bankDatabase.addLender(lender)
                    else:
                        cuiPrestamistaExistente.append(lender['cui'])
                else:
                    return jsonify({'msg': '¡Error de sintaxis! Puede que algunos prestamistas no se agregaron'}), 206
            if len(cuiPrestamistaExistente) == 0:
                return jsonify({'msg': 'Prestamistas agregado exitosamente'}), 200
            else:
                msg = {
                    'msg': f'El cui {cuiPrestamistaExistente} no se agrego, debido a que ya existe'}
                return jsonify(msg), 206
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500

#########CONSULT_INFORMATION########################
@app.route('/person/<string:cui>', methods=['GET'])
def getLender(cui):
    try:
        object = bankDatabase.getLender(cui)

        if object != None:
            return(jsonify(object)), 200
        else:
            msg = {'msg': '¡Error! no existe prestamista con ese cui'}
            return(jsonify(msg)), 404
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500


#########CREATE_LOAN########################
@app.route('/borrow', methods=['POST'])
def newLoan():
    body = request.get_json()
    try:
        if ('cui' in body and 'isbn' in body):
            lenderPosition = bankDatabase.lenderExists(body['cui'])
            bookPosition = bankDatabase.bookExists(body['isbn'])
            if (lenderPosition != None):
                if (bookPosition != None):
                    if (bankDatabase.borrowedBook(lenderPosition)):
                        return(jsonify({'msg': 'El prestamista tiene un libro pendiente de devolver'})), 403
                    if (bankDatabase.NoAvailableCopies(bookPosition)):
                        uuid = bankDatabase.newRecord(
                            lenderPosition, bookPosition)
                        return(jsonify({'uuid': uuid})), 200
                    else:
                        return(jsonify({'msg': 'Sin copias disponibles'})), 200
                else:
                    return(jsonify({'msg': 'El isbn no existe'})), 404
            else:
                return(jsonify({'msg': 'El cui no existe'})), 404
        else:
            return jsonify({'msg': '¡Error de sintaxis! Prestamo no realizado'}), 206
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500

#########CONSULT_LOAN########################
@app.route('/borrow/<int:uuid>', methods=['PATCH'])
def returnBook(uuid):
    try:
        recordPosition = bankDatabase.recordExists(uuid)
        if(recordPosition != None):
            if (bankDatabase.returnedDate(recordPosition)):
                bankDatabase.retunBook(recordPosition)
                return(jsonify({'msg': 'Libro devuelto'})), 200
            else:
                return(jsonify({'msg': 'El libro ya ha sido devuelto'})), 200
        return jsonify({'msg': 'El uuid no existe'}), 404
    except:
        return {'msg': 'Ocurrio un error en el servidor'}, 500


if __name__ == "__main__":
    app.run(debug=True)