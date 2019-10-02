## Install instructions for Ubuntu

#### Installing Python3 and SqLite3

In order to run the app locally, you need Python3 (which comes with pip) and SQLite3. Run the following commands in the terminal:

```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install sqlite3
pip install --upgrade pip
```

#### Running the app locally

1. Download the ZIP-file from [here](https://github.com/tommise/AppointmentSystem) by pressing "Clone or download".
2. Extract the file to desired folder.
3. Within terminal, navigate to the root folder.
4. Create a Python virtual environment with a command:
```
python -m venv venv
```
5. Start the virtual environment by typing: 
```
source venv/bin/activate
```
6. Install Flask and project dependencies:
```
pip install Flask
pip install -r requirements.txt
```
7. And finally in order to run the app type in the terminal: 
```
python run.py
```
8. The database tables are created automatically and the application can be run locally from http://localhost:5000/

#### Running the app globally in Heroku

1. Make an account to [Heroku](https://www.heroku.com).
2. Follow the installation steps above (excluding steps 7 & 8).
3. Make sure requirements.txt does not contain a row "pkg-resources==0.0.0".
4. Download heroku from the command line with:
```
sudo snap install heroku --classic
```
5. Navigate to the project root and type:
```
heroku create name_of_the_project
```
6. Commit the changes to the version control:
```
git remote add heroku https://git.heroku.com/name_of_the_project.git
git add .
git commit -m "Installing Heroku"
git push heroku master 
```
7. Initiate PostgeSQL with Heroku:
```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```
8. Navigate to name_of_the_project.herokuapp.com
