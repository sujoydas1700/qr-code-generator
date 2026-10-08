import qrcode
from flask import Flask,render_template,request
from io import BytesIO
import base64

app = Flask(__name__)

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(back_color=(255, 195, 235), fill_color=(255, 0, 255))
    return img


@app.route("/details",methods = ["GET","POST"])
def get_details():
    # pass
    if request.method == "GET":
        return render_template("get_details.html")
    else:
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        address = request.form["address"]
        profession = request.form["profession"]


        result = f'''
            Name : {name}
            Phone : {phone}
            Email : {email}
            Age : {age}
            Blood Group : {blood_group}
            Address : {address}
            Profession : {profession}'''
        
        image = generate_qr(result)
        img_io = BytesIO()
        image.save(img_io, format="PNG")

        img_io.seek(0)

        image_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

        return render_template(
            "show_qr.html",
            qr_image=image_base64
        )

        

@app.route("/data",methods = ["GET","POST"])
def get_data():
    if request.method == "GET":
        return render_template("get_data.html")
    else:
        data = request.form["data"]

        image = generate_qr(data)

        img_io = BytesIO()
        image.save(img_io, format="PNG")

        img_io.seek(0)

        image_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

        return render_template(
            "show_qr.html",
            qr_image=image_base64
        )

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)