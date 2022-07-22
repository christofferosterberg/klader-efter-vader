# klader-efter-vader
An application that tells you what clothes to put on for a day

## Installation:

1. Open terminal, navigate to the cloned git-repo and checkout the develop branch (main is used for the deployed version and will not work locally).
```
git checkout origin/main
```
2. Create the virtual environment (python needs to be installed):
```
python3 -m venv venv
```
3. Open the virtual env:
```
source venv/bin/activate
```
4. Install the requirements:
```
pip install -r requirements.txt
```
5. Create the database:
```
python3 fill_db.py
```
6. Run the application:
```
python3 app.py
```
7. Open a web browser and navigate to "localhost:3000"
8. Find out what clothes o wear today! (and if you need pollen medicine or what uv-protection to wear)
