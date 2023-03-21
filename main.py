from PIL import Image
from werkzeug.utils import secure_filename
import extcolors
import easydev
from colormap import rgb2hex
from flask import render_template, Flask, request
import os
from dotenv import load_dotenv

load_dotenv("C:\\Users\\sharm\\PycharmProject\\todo-list\\.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/show_palette', methods=['GET', 'POST'])
def show_palette():
    image = request.files['filename']
    filename = secure_filename(image.filename)
    extension = filename.split(".")[-1]
    image_name = filename.split('.')[0]
    saved_img = "static/" + image_name + "." + extension

    image.save(saved_img)
    try:
        img = Image.open(saved_img)
        width_percent = 900 / float(img.size[0])
        height = float(img.size[1]) * width_percent
        resized_img = img.resize((900, int(height)))
        new_path = "static/" + image_name + "resized." + extension
        resized_img.save(new_path)
        color = extcolors.extract_from_image(resized_img)

        rgb_color_list = [i[0] for i in color[0][:10]]
        top10_colors = []
        for rgb in rgb_color_list:
            hexcode = rgb2hex(rgb[0], rgb[1], rgb[2])
            top10_colors.append(hexcode)
        print(top10_colors)
        return render_template('index.html', hex=top10_colors, im=new_path)
    except:
        error = "Error!! please provide a '.png' or '.jpg' or '.jpeg' type image."
        return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
