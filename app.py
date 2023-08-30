from flask import Flask, render_template, request

app = Flask(__name__)

fields = [("year", "number"), ("selling_price", "float"), ("km_driven", "float"), ("fuel", "text"),
          ("seller_type", "text")
    , ("transmission", "text"), ("engine", "number"), ("owner", "text"), ("mileage", "float"),
          ("max_power", "float"), ("torque", "text"), ("seats", "number")]
transmission = ["Manual", "Automatic"]


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)  # Printing the form data to the console
    return render_template("index.html", fields=fields, transmissions=transmission)


if __name__ == '__main__':
    app.run(debug=True)
