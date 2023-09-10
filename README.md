# Test Instructions:
1. Navigate to folder to contain project directory
2. Clone the HHack repository:
- HTTPS: `git clone https://github.com/RW-77/HHack.git`
- SSH: `git clone git@github.com:RW-77/HHack.git`
3. navigate to project directory `cd HHack`
4. switch to main branch: `git checkout main`
5. create virtual environment: `python3 -m venv hhvenv`
6. activate virtual environment:

- Windows: `hhvenv/scripts/activate`
- Mac: `source hhvenv/bin/activate`
7. install dependencies: `pip install -r requirements.txt`
8. run `flask run` to start the flask application hosted at `http://127.0.0.1:5000`