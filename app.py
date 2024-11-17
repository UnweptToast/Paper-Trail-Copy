from flask import Flask, redirect, render_template, request, session
from Model.model import model, label_encoder, vectorizer
from OCR.start import process_image
from datetime import datetime
import os
import sqlite3
import helpers
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/upload_receipt', methods=["GET", "POST"])
def upload_receipt():

    conn = sqlite3.connect("paper_trail.db")
    cursor = conn.cursor()

    if request.method=="POST":

        receipt_image = request.form.get("receipt_image")
        
        if 'receipt_image' not in request.files:
            return render_template("error.html", err_message = "No file part")
        file = request.files['receipt_image']
        if file.filename == '':
            return redirect("/error", err_message = "No selected file")
        if file:
            # print(file.filename)
            # Ensure the file pointer is at the beginning
            copy = helpers.deep_copy(file)
            content,total = process_image(copy)
            pred = label_encoder.inverse_transform(model.predict(vectorizer.transform([content])))
            print(pred)
            if not os.path.exists(f"static//receipts//{pred[0]}"):
                os.mkdir(f"static//receipts//{pred[0]}")
            cursor.execute("SELECT r_key FROM RECEIPTS;")
            try:
                no_of_ele = cursor.fetchall()[-1][0]
            except:
                no_of_ele = 0
            file_path = os.path.join(f"static//receipts//{pred[0]}", f"Bill{no_of_ele + 1}.{file.filename.split(".")[-1]}")
            # print("File path: ", file_path)
            file.save(file_path)

            # Get today's date
            today_date = datetime.today().strftime('%Y-%m-%d')
            # print(today_date)
            #adding the picture to the database
            query = f"INSERT INTO receipts (type, date, total, file_location) VALUES(\'{pred[0]}\', \'{today_date}\', {total}, \'{'/static/receipts/' + pred[0] + '/' + f'Bill{no_of_ele + 1}.{file.filename.split('.')[-1]}'}\');"
            print(query)
            cursor.execute(query)
            conn.commit()
            conn.close()

        return render_template("upload_receipt.html")

    elif request.method=="GET":
        return render_template("upload_receipt.html")
    
@app.route('/receipt_summary', methods=["GET", "POST"])
def receipt_summary():
    conn = sqlite3.connect("paper_trail.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, type, total, r_key FROM receipts")
    receipt_data_list = cursor.fetchall()
    data = dict()
    for i in range(len(receipt_data_list)):
        type = receipt_data_list[i][1]
        if type in list(data.keys()):
            data[type].append(list(receipt_data_list[i]))
        else:
            data[type] = [list(receipt_data_list[i])]

    return render_template("receipt_summary.html",data=data,keys=list(data.keys()))

@app.route('/image/<no>')
def image_page(no):
    try:
        conn = sqlite3.connect("paper_trail.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT file_location FROM RECEIPTS WHERE r_key = {no};")
        path = cursor.fetchall()[0][0]
    except:
        return render_template("error.html", error_message = "KEEP AWAY!!!")
    if path:
        return render_template("image_display.html",path = path)

if __name__ == '__main__':
    app.run(debug=True)