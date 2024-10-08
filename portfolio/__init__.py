from pprint import pprint
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from dotenv import find_dotenv, load_dotenv
import os
import json
from .email_utility import send_simple_email
import uuid
# Example usage:

app = Flask(__name__)
app.secret_key =  uuid.uuid4().hex
load_dotenv(find_dotenv(), override=True)
def check_database(projects):
    if "DATABASE_PATH" in os.environ:
        if os.path.exists(os.environ["DATABASE_PATH"]):
            with open(os.environ["DATABASE_PATH"]) as db:
                projects = json.load(db)
                print("loaded database successfully")
                # pprint(projects)
                # print("the id of the db var",id(projects))
                return projects
        else:
            print("NO DATABASE FILE FOUND")
            return False
    else:
        print(f"FAILED TO LOAD {os.environ['DATABASE_PATH']}")
        return False

def get_related_projects(slug, max_related=3):
    if slug not in projects_index:
        return []

    current_project = projects_index[slug]
    current_categories = set(current_project['categories'])
    
    related_projects = []
    
    for project in projects:
        if project['slug'] != slug:  # Don't include the current project
            project_categories = set(project['categories'])
            common_categories = current_categories.intersection(project_categories)
            
            if common_categories:
                related_projects.append({
                    'name': project['name'],
                    'thumbnail': project['thumbnail'],
                    'description': project['description'],
                    'slug': project['slug'],
                    'common_categories': len(common_categories)
                })
    
    # Sort related projects by the number of common categories (descending)
    related_projects.sort(key=lambda x: x['common_categories'], reverse=True)
    
    # Return the top 'max_related' projects, removing the 'common_categories' key
    return [{k: v for k, v in project.items() if k != 'common_categories'} 
            for project in related_projects[:max_related]]


projects = []
projects = check_database(projects)
projects_index = { project["slug"] : project for project in projects}




@app.route("/")
def index():
    return render_template("pages/home.html", projects=projects)
@app.route("/about")
def about():
    return render_template("pages/about.html")
@app.route("/contact")
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        send_simple_email("yahialinus21alg@gmail.com", "gxto expi xxup fwlk", "yahiameteor@gmail.com", subject, message + f" by {name}: {email}")
        # Here you would typically send an email or save to a database
        saved_messages = []
        if os.path.exists("saved_messages.json"):
            # read the list of dictionaries from the json file
            with open("saved_messages.json", "r") as sm:
                saved_messages = json.load(sm)
            with open("saved_messages.json", "w") as msg_db:
                saved_messages.append(request.form)
                # rewrite the latest list of dictionaries in the json saved messages
                json.dump(saved_messages, msg_db)
                print("saved the message successfully!")
        else:
            with open("saved_messages.json", "w") as msg_db:
                saved_messages.append(request.form)
                # rewrite the latest list of dictionaries in the json saved messages
                json.dump(saved_messages, msg_db)
                print("saved the message successfully!")
        # For now, we'll just print to console
        print(f"New message from {name} ({email}): {subject}")
        
        flash('Thank you for your message! I\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template("pages/contact.html")




# Modify your project route to include related projects
@app.route("/project/<string:slug>")
def project(slug):
    if slug not in projects_index:
        abort(404)
    
    current_project = projects_index[slug]
    related_projects = get_related_projects(slug)
    
    return render_template("posts/details.html", 
                           project=current_project, 
                           related_projects=related_projects)

@app.errorhandler(404)
def page_not_found(e):
    print("error happened: ",e)
    return render_template('404.html'), 404