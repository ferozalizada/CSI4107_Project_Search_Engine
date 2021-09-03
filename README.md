# A Boolean and Vector Model System (VSM) based search engine

Currently the search engine only works on a selected list of course summary from uOttawa.

### Working demo

Working demo available at: https://nooble.herokuapp.com/

### How to use

#### Vector Space Model (VSM) Search

With this, you can perform free-text searches like `data science or web development`.

#### Boolean Retrieval Model (BRM) Search

With this, you can perform boolean searches like `operating AND systems or NOT hardware`.

### Installation

1. Clone the repo and navigate in the root directory of repo
2. run `pip install -r requirements.txt`
3. run `python main.py`

### Docker Installion

1. Install Docker
2. run `docker image build -t myapp .`
3. run `docker run -d -p$PORT:8080 myapp`
4. goto `http://localhost:8080/`

### Running the Project

To run the project simply run `main.py` from the root folder and goto `http://localhost:8080/` on your browser.
