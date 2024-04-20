from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import database.databaseCheck as dbCheck
import database.databaseActions as dbAction
import database.adeverinta as adeverinta
from datetime import datetime
import os
import glob
from PIL import Image
import re
import io
from werkzeug.utils import secure_filename
import base64
import database.Forum as Forum

app = Flask(__name__)
app.secret_key = 'secretKey123'  # replace with your own secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'logIn'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Ruta pentru pagina principala
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('Welcome.html')

# Ruta pentru pagina de logare
@app.route('/LogIn', methods=['GET', 'POST'])
def logIn():
    if request.method == 'POST':
        username = request.form['UserName']
        password = request.form['pswrd']
        user = dbCheck.logIn(username, password)
        if user != False:
            login_user(User(user[0]))
            return redirect(url_for('homePage'))
        else:
            return render_template('LogIn.html', message='Invalid username or password')
        
    return render_template('LogIn.html', message='')

# Ruta pentru pagina de inregistrare
@app.route('/SignIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['UserName']
        email = request.form['email']
        user_type = request.form['userType']
        password = request.form['pwd']
        user = dbCheck.signInUsernameExists(username)
        emailok = dbCheck.signInEmailExists(email)
        if user == True:
            #TO-DO: implement a message to be displayed on the page
            return render_template('SignIn.html', message='Username already taken!')
        elif emailok == True:
            #TO-DO: implement a message to be displayed on the page
            return render_template('SignIn.html', message='This email adress already has an account!')  
        else:
            # insert the user in the database
            if user_type == 'Patient':
                tip = 'p'
                id_clinica = 0
            elif user_type == 'Doctor':
                # check if the clinic exists in the database only if a doctor tries to sign in
                id_clinica = request.form['clinic']
                clinicok = dbCheck.signInClinicExists(id_clinica)
                if clinicok == False:
                #TO-DO: implement a message to be displayed on the page
                    return render_template('SignIn.html', message='This clinic does not exist in the database!')
                tip = 'd'
            dbAction.addUser(username, password, email, tip, id_clinica)
            return redirect(url_for('logIn'))
    return render_template('SignIn.html')

# Ruta pentru prima pagina dupa conectare
@app.route('/home')
@login_required
def homePage():
    # TODO get the latest blog posts
    postari = dbAction.getPostariBlog()
    list_postari = []
    print(postari)
    for postare in postari:
        post = Forum.Blog(id_postare=postare[0], titlu=postare[1], text = postare[2], data_postare=postare[3], poza=postare[4])  
        if post.poza:
            filename = f'image_{post.id_postare}.png'
            image_path = os.path.join('static', filename)
            with open(image_path, 'wb') as f:
                f.write(post.poza)
            post.image_filename = filename

        list_postari.append(post)

    return render_template('Home.html', posts = list_postari)


@app.route('/post/<id>')
def post(id):
    # Fetch the post data using the id
    postare = dbAction.getBlog(id)
    post = Forum.Blog(id_postare=postare[0], titlu=postare[1], text = postare[2], data_postare=postare[3], poza=postare[4])  
    if post.poza:
            filename = f'image_{post.id_postare}.png'
            image_path = os.path.join('static', filename)
            with open(image_path, 'wb') as f:
                f.write(post.poza)
            post.image_filename = filename
    return render_template('Post.html', post=post)

# Ruta pentru editare profil
@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    user = dbAction.getUser(current_user.get_id())  
    if user.type == 'd':
        if user.data_nasterii != None:
            user.data_nasterii = datetime.strptime(user.data_nasterii, '%d-%m-%Y').strftime('%Y-%m-%d')
    if request.method == 'POST':
        if user.type == 'p':
            doctor_id = request.form['doctor_id']
            if doctor_id != 'None':
                if dbCheck.doctorExists(doctor_id) == False:
                    return render_template('profile.html', user=user, message='Doctor does not exist!')
                else:
                    user.nume = request.form['nume']
                    user.prenume = request.form['prenume']
                    user.data_nasterii = request.form['data_nasterii']
                    user.doctor_id = doctor_id
                    user.weight = request.form['weight']
                    user.height = request.form['height']
                    if request.form['gender'] == 'Female':
                        user.sex = 'f'
                    else:
                        user.sex = 'm'
                    dbAction.updateUser(user=user)
        elif user.type == 'd':
            data_nasterii = datetime.strptime(request.form['data_nasterii'], '%Y-%m-%d').strftime('%d-%m-%Y')
            user.nume = request.form['nume']
            user.prenume = request.form['prenume']
            user.data_nasterii = data_nasterii
            dbAction.updateUser(user=user)
        return redirect(url_for('editProfile', user_id=user.id, user=user, message=''))
    return render_template('profile.html', user=user, message='')

# Ruta pentru generare adeverinta medicala 
@app.route('/medicalCertificate', methods=['GET', 'POST'])
@login_required
def medicalCertificate():
    user = dbAction.getUser(current_user.get_id())
    
    static_dir = os.path.join(app.root_path, 'static')
    for old_image in glob.glob(os.path.join(static_dir, 'image_*.png')):
        os.remove(old_image)

    filenames = {}
    for id, image in image_dir.items():
        filename = f'image_{id}.png'
        image.save(os.path.join(static_dir, filename))
        filenames[id] = filename

    if request.method == 'POST':
        if user.type == 'p':
            nume = user.nume
            prenume = user.prenume
            cnp = request.form['cnp']
            data_nasterii = user.data_nasterii
            adresa = request.form['adresa']
            ocupatie = request.form['ocupatie']
            motiv = request.form['motiv']
            loc = request.form['loc']
            doctor_id = dbCheck.getDoctor(user.doctor_id)
            medic = doctor_id[2] + ' ' + doctor_id[3]
            clinica = dbCheck.signInClinicExists(doctor_id[5])
            png_file = adeverinta.generareAdeverinta(nume, prenume, cnp, data_nasterii,adresa, ocupatie, motiv, loc, medic, clinica[1])    
            dbAction.addAdeverinta(user.id, doctor_id[1], png_file)
            return render_template('adeverinta.html', user=user, message='Medical certificate generated!', images=filenames, utilizator=utilizator)
        else:
            print("\nUPDATE ADEVERINTA CALLED\n")
            data_url = request.form['imageData']
            id = request.form['imageId']
            base64_image = re.sub('^data:image/.+;base64,', '', data_url)
            image = base64.b64decode(base64_image)
            dbAction.updateAdeverinta(id, image)
            return render_template('adeverinta.html', user=user, message='You submitted the medical certificate!', images=filenames)
    return render_template('adeverinta.html', user=user, message='', images=filenames, utilizator=utilizator)

# Ruta pentru forum 
@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    postari = dbAction.getPostari()
    list_postari = []

    for postare in postari:
        utilizator = dbAction.getUserType(postare[1])
        post = Forum.PostareForum(id_postare=postare[0], id_utilizator=postare[1], titlu=postare[2], text = postare[3], data_postare=postare[4], tip_postare=postare[5], poza=postare[6], utilizator=utilizator[1], tip_utilizator=utilizator[4])
        
        if post.poza:
            filename = f'image_{post.id_postare}.png'
            image_path = os.path.join('static', filename)
            with open(image_path, 'wb') as f:
                f.write(post.poza)
            post.image_filename = filename

        raspunsuri = dbAction.getRaspunsPostare(post.id_postare)
        for raspuns in raspunsuri:
            utilizator = dbAction.getUserType(raspuns[2])
            rasp = Forum.RaspunsForum(id_raspuns=raspuns[0], id_postare=raspuns[1], id_utilizator=raspuns[2], text=raspuns[3], tip_postare=raspuns[4], utilizator=utilizator[1], tip_utilizator=utilizator[4])
            post.raspunsuri.append(rasp)

        list_postari.append(post)

    list_postari = sorted(list_postari, key=lambda post: post.data_postare, reverse=True)
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'post':
            print("Form submitted")
            title = request.form['postTitle']
            text = request.form['user_activity']
            tip_postare = 'anonymousCheck' in request.form
            if tip_postare:
                tip_postare = 'a'
            else:
                tip_postare = 'n'
            user = dbAction.getUser(current_user.get_id())
            user_id = user.id
            if 'imageUpload' not in request.files:
                print('No file part')
            file = request.files['imageUpload']
            if file.filename == '':
                print('No selected file')
                png_image = None
            if file:
                print('File received')
                image = Image.open(file.stream)
                png_image_io = io.BytesIO()
                image.save(png_image_io, format='PNG')
                png_image_io.seek(0)
                png_image = png_image_io.read()
            dbAction.addPostare(user_id, title, text, tip_postare, png_image)
        elif form_type == 'new_comment':
            print("Raspuns submitted")
            text = request.form['comment']
            tip_postare = 'anonymousCheck' in request.form
            if tip_postare:
                tip_postare = 'a'
            else:
                tip_postare = 'n'
            user = dbAction.getUser(current_user.get_id())
            user_id = user.id
            post_id = request.form['id_post']
            dbAction.addRaspunsPostare(user_id, post_id, text, tip_postare)
        return redirect(url_for('forum'))
    return render_template('forum.html', posts = list_postari)




# Ruta pentru deconectare
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logIn'))

if __name__ == "__main__":
    app.run(debug=True)