import os
import time
import hashlib
import sqlite3
import re

from app import app
from flask import render_template
from flask import request, jsonify, redirect
import flask
import textract


from app.SETTINGS import ALLOWED_EXTENSIONS

SUPPORTED_LANGUAGES=[
    {"value":"english", "text": "english"},
    {"value":"arabic", "text": "عربي"}
];

SUPPORTED_MODELS=[
    {"value":"boolean model", "text": "Boolean Model"},
    {"value":"extended boolean model", "text": "Extended Boolean Model"},
    {"value":"vector model", "text": "Vector Model"},
];

"""
SELECT * from users WHERE column LIKE "%pineapple%";
"""

"""
SELECT * FROM mytable
WHERE column1 LIKE '%word1%'
   OR column1 LIKE '%word2%'
   OR column1 LIKE '%word3%'
"""

"""
SELECT * FROM mytable
WHERE column1 LIKE '%word1%'
  AND column1 LIKE '%word2%'
  AND column1 LIKE '%word3%'
"""

# database class to make requests to DB
class database:
    pass
DEFAULT_DB = ""

# logs everything happens on the server
class logger:
    pass

def text(file_name):
    text = textract.process(file_name).deconde("utf-8")
    # TODO: process text
    return text

# defines each host with data
class host:
    def __init__(self, 
                 id:str, 
                 ip_address:str, 
                 language:str, 
                 model:str, 
                 session_start_time:time,
                 database_path:str,
                 port_number:str="", 
                ):
        self.id=id;
        self.ip_address=ip_address;
        self.port_number=port_number
        self.language=language;
        self.database_path=database_path;
        self.model=model;
        # when the first time connected to server
        self.session_start_date=session_start_time;
        # the time of the last request sent by host to client
        self.last_request_time=session_start_time;
        self.requests_number=1;
        
        pass
    
    def update(self, language:str, database_path:str, model:str):
        self.language=language;
        self.database_path=database_path;
        self.model=model;
            
    def __str__(self):
        return "<[" + str(self.ip_address) + ":" + str(self.port_number) + "] " + \
                "{" + \
                    "model:\"" + str(self.model) + "\", " + \
                    "language:\"" + str(self.language) + "\"," + \
                    "database:\"" + str(self.database_path) + "\", " + \
                "}>";

# contains all connected hosts, keys are IPs
hosts = {}

def get_all_file_paths(root_folder=os.path.join("app", "static", "IR", "databases")):
    """
    Recursively iterates through a root folder and its subfolders, returning a list of paths of all files.

    :param root_folder: The root folder to start the search from
    :return: A list of paths of all files starting from the root folder
    """
    file_paths = []

    # Walk through all directories and files
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Join the dirpath and filename to get the full file path
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    
    return file_paths

@app.route("/")
@app.route("/index")
def index():
    # allowed files extensions
    allowed_extensions = ",".join(["."+str(ext) for ext in ALLOWED_EXTENSIONS])
    # get all DB
    databases=[file for file in get_all_file_paths() if file.endswith(".db")] 
    return render_template("index.html", SUPPORTED_LANGUAGES=SUPPORTED_LANGUAGES, SUPPORTED_MODELS=SUPPORTED_MODELS, ALLOWED_EXTENSIONS=allowed_extensions, databases=databases)

@app.route('/config', methods=['GET','POST'])
def config():
    host_id=hashlib.sha512(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()
    use_dafault_db=str(flask.request.form.get("use_default_db"))
    host_database_path=None
    host_raw_files_path=None
    host_session_data_folder_id=None
    host_session_start_time=time.asctime()
    host_session_data_folder_id=str("_".join(host_session_start_time.replace(":", "_").split(" ")[2:]))
    if(use_dafault_db=="on"):
        host_database_path=str(flask.request.args.get('database-path')) if flask.request.method == "GET" else str(request.form.get("database-path"))
    else:
        # create new folder under data folder
        # extract text
        # process text
        # create db
        print("creating new raw files")
        files = flask.request.files.getlist("files")
        if(len(files) == 0):
            # no files found, redirect to index with error message
            allowed_extensions = ",".join(["."+str(ext) for ext in ALLOWED_EXTENSIONS])
            return render_template("index.html", SUPPORTED_languageS=SUPPORTED_languageS, SUPPORTED_MODELS=SUPPORTED_MODELS, ALLOWED_EXTENSIONS=allowed_extensions)
        
        # creating raw files folder
        host_raw_files_path=os.path.join("app", "static", "IR", "raw_files", host_session_data_folder_id , str(hashlib.md5(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()))
        if not os.path.exists(host_raw_files_path):
            os.makedirs(host_raw_files_path)
        else:
            #TODO
            os.makedirs(host_raw_files_path)
        # save files
        for file in files:
            if(file.filename.split(".")[-1] in ALLOWED_EXTENSIONS):
                file.save(os.path.join(host_raw_files_path, file.filename))
        
        # extract text from files and set in raw_text
        host_raw_utf_8_files_path=os.path.join("app", "static", "IR", "raw_UTF_8", host_session_data_folder_id , str(hashlib.md5(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()))
        if not os.path.exists(host_raw_utf_8_files_path):
            os.makedirs(host_raw_utf_8_files_path)

        for file in os.listdir(host_raw_files_path):
            # get text
            text = textract.process(os.path.join(host_raw_files_path, file)).decode("utf-8")
            # save text
            print(text, file=open(
                os.path.join(host_raw_utf_8_files_path, ".".join(file.split(".")[:-1])+".txt"), 
                "w",
                encoding="utf-8"))
        

        # process files
        host_processed_utf_8_files_path=os.path.join("app", "static", "IR", "processed_UTF_8", host_session_data_folder_id , str(hashlib.md5(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()))
        if not os.path.exists(host_processed_utf_8_files_path):
            os.makedirs(host_processed_utf_8_files_path)
        for file in os.listdir(host_raw_utf_8_files_path):
            # get text
            # remove white spaces
            if(file.endswith(".txt")):
                raw_text = open(os.path.join(host_raw_utf_8_files_path, file), "r", encoding="utf-8").read()
                processed_text=(re.compile(r'[ ]{2,}', re.VERBOSE)).sub(r' ',raw_text)
                processed_text=(re.compile(r'[\t]{2,}', re.VERBOSE)).sub(r' ',processed_text)
                processed_text=(re.compile(r'[\r]{2,}', re.VERBOSE)).sub(r'\n',processed_text)
                processed_text=(re.compile(r'[\n]{2,}', re.VERBOSE)).sub(r'\n',processed_text)
                # save text
                print(processed_text, file=open(
                    os.path.join(host_processed_utf_8_files_path, ".".join(file.split(".")[:-1])+".txt"), 
                    "w",
                    encoding="utf-8")
                );
            
        # create DB and save results
        host_database_path = os.path.join("app", "static", "IR", "databases", host_session_data_folder_id, str(hashlib.md5(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()));
        print(host_database_path)
        if not os.path.exists(host_database_path):
            os.makedirs(host_database_path)
            host_database_path=os.path.join(host_database_path, "corpus.db")
        if not os.path.exists(host_database_path):
            _ = open(os.path.join(host_database_path),"wb")
            _.close()

        con = sqlite3.connect(os.path.join(host_database_path))
        cur = con.cursor()
        # id is md5 hex hash of raw file
        # content is processd text file content
        # title is the first line of the document
        cur.execute("""CREATE TABLE corpus(
                    id varchar(32) primary key,
                    title text, 
                    content text
                    );"""
        );
        for file in os.listdir(host_raw_files_path):
            # caculate hash
            md5=hashlib.md5();
            BUF_SIZE=65536;  # lets read stuff in 64kb chunks!
            f = open(os.path.join(host_raw_files_path, file), "rb");
            while True:
                data = f.read(BUF_SIZE);
                if not data:
                    break
                md5.update(data);
            id=md5.hexdigest();
            f.close();
            # gen content and title
            content=open(os.path.join(host_processed_utf_8_files_path, ".".join(file.split(".")[:-1])+".txt"), "r", encoding="utf-8").read();
            title=open(os.path.join(host_processed_utf_8_files_path, ".".join(file.split(".")[:-1])+".txt"), "r", encoding="utf-8").readline();
            data = (id, title, content);
            cur.execute("""INSERT INTO corpus VALUES (?, ?, ?)""", data);
            con.commit();
        con.close();

    host_language=str(flask.request.form.get('language'));
    host_ip_address=str(flask.request.environ.get('REMOTE_ADDR'));
    host_port_number=str(flask.request.environ.get('REMOTE_PORT'))
    host_model = str(flask.request.args.get('model')) if flask.request.method == "GET" else str(request.form.get("model"))
    
    # TODO: create new host
    if((host_id) in hosts.keys()):
        # udpate
        print("updating host...")
        hosts[(host_id)].update(
            language=host_language,
            database_path=host_database_path,
            model=host_model,
        );
    else:
        # create new one
        print("creating host...")
        hosts[(host_id)] = host(
            id=host_id,
            ip_address=host_ip_address,
            language=host_language,
            session_start_time=host_session_start_time,
            database_path=host_database_path,
            model=host_model,
            port_number=host_port_number,
        );
    
    
    print(hosts[host_id]);
    
    """
    return "ip_address" + str(flask.request.remote_addr) + "-" + str(flask.request.remote_user) + "-" + str(flask.request.method) + "-" + flask.request.environ.get('HTTP_X_REAL_IP', flask.request.remote_addr) \
        + "- files: [" + ",".join([str(file.filename) for file in flask.request.files.getlist("files")]) + "]"\
        + "- language: " + str(flask.request.form.get('language')) \
        + "- boolean model: " + model
    """
    return redirect("search")

# TODO; save files
# TODO: process files

# TODO: log
# TODO: make db
# TODO: create models

@app.route("/doc=<id>")
def document(id):
    # get document with specific id
    print("Requesting doc: ", id)
    title, head, content= "doc title", "doc header", "doc content......."
    return render_template("doc.html", id=id, title=title, head=head, content=content)

@app.route("/test")
def test():
    # to run flask: $flask --app app run
    global app
    return "<p>Server is on.</p>"

@app.route('/search', methods=['GET', 'POST'])
def search():
    # get the host
    host_id=hashlib.sha512(str(flask.request.environ.get('REMOTE_ADDR')).encode("utf-8")).hexdigest()
    if(not host_id in hosts.keys()):
        # user does notexist, create one first
        return redirect("/")
    
    # if host does not exist, redirect to index again
    host = hosts[host_id]
    host_model=host.model;
    host_language=host.language;
    database_path=host.database_path;

    search_time_sec=time.time()
    search_request=str(flask.request.args.get('search-request')) if flask.request.method == "GET" else str(request.form.get("search-request"))
    print(search_request)
    # TODO: Check user input or print error message
    search_results=[];
    total_results_count=0;
    if(search_request!="" and search_request!= "None"):
        print("get the request: " + search_request)
        #TODO, process request

        tokens=search_request.split(" ")
        # if host model
        if(host_model=="boolean model"):
            # open DB
            con = sqlite3.connect(os.path.join(database_path))
            # get the documenets
            cur = con.cursor()
            # query
            query = "SELECT * FROM corpus WHERE " + " OR ".join(["content LIKE ?"] * len(tokens))
            query_params = ['% ' + token + ' %' for token in tokens]
            print(query)
            print(query_params)
            cur.execute(query, query_params);
            query_results=cur.fetchall();
            con.close();
            for result in query_results:
                content=result[2]
                print(tokens[0] in result[2])
                if(tokens[0] in result[2]):
                    for token in tokens:
                        content=content.replace(token, "<span class=selected>" + token + "</span>")
                    search_results.append(
                        {
                            "document_id" : result[0],
                            "title" : result[1],
                            "content" : content,
                            "url" : "url",
                            "summary" : content[max(0, result[2].find(tokens[0])-100):result[2].find(tokens[0])+len(tokens[0])+100]+"...",
                            "rank" : -1
                        }
                    )

        if(host_model=="extended boolean model"):
            # open DB
            con = sqlite3.connect(os.path.join(database_path))
            # get the documenets
            cur = con.cursor()
            # query
            query = "SELECT * FROM corpus WHERE " + " OR ".join(["content LIKE ?"] * len(tokens))
            query_params = ['% ' + token + ' %' for token in tokens]
            print(query)
            print(query_params)
            cur.execute(query, query_params);
            query_results=cur.fetchall();
            con.close();
            # ranking
            # calculate term frequency in document
            # f0 = [[t1_f_d1, t2_f_d1, t3_f_d1]]
            f = [[result[2].count(token) for token in tokens] for result in query_results]
            tf = [[ f[j][i] / len((re.compile(r'\s+', re.VERBOSE)).sub(r' ',query_results[j][2]).split(" ")) for i in range(len(f[j]))] for j in range(len(query_results))]
            d = [0] * len(tokens)
            for i in range(len(d)):
                for doc in query_results:
                    if doc[2].find(tokens[i]) != -1:
                        d[i] = d[i] + 1

            import math
            idf = [math.log(len(query_results)/d[i]) for i in range(len(d))]

            w = [[ f[j][i] * idf[i] / max(idf) for i in range(len(tokens))] for j in range(len(query_results))]

            # simplification, all ands
            rank = [sum([w_i_doc**len(query_results) for w_i_doc in w_doc])**(1/len(query_results)) for w_doc in w]

            for i in range(len(query_results)):
                result=query_results[i]
                content=result[2]
                print(tokens[0] in result[2])
                if(tokens[0] in result[2]):
                    for token in tokens:
                        content=content.replace(token, "<span class=selected>" + token + "</span>")
                    search_results.append(
                        {
                            "document_id" : result[0],
                            "title" : result[1],
                            "content" : content,
                            "url" : "url",
                            "summary" : content[max(0, result[2].find(tokens[0])-100):result[2].find(tokens[0])+len(tokens[0])+100]+"...",
                            "rank" : round(rank[i],2)
                        }
                    )
            # sorting by rank
            search_results = sorted(search_results, key=lambda d: d['rank'])
            search_results.reverse()
            

        if(host_model=="vector model"):
            # open DB
            con = sqlite3.connect(os.path.join(database_path))
            # get the documenets
            cur = con.cursor()
            # query
            query = "SELECT * FROM corpus WHERE " + " OR ".join(["content LIKE ?"] * len(tokens))
            query_params = ['% ' + token + ' %' for token in tokens]
            print(query)
            print(query_params)
            cur.execute(query, query_params);
            query_results=cur.fetchall();
            con.close();
            # ranking
            # calculate term frequency in document
            # f0 = [[t1_f_d1, t2_f_d1, t3_f_d1]]
            f = [[result[2].count(token) for token in tokens] for result in query_results]
            tf = [[ f[j][i] / len((re.compile(r'\s+', re.VERBOSE)).sub(r' ',query_results[j][2]).split(" ")) for i in range(len(f[j]))] for j in range(len(query_results))]
            d = [0] * len(tokens)
            for i in range(len(d)):
                for doc in query_results:
                    if doc[2].find(tokens[i]) != -1:
                        d[i] = d[i] + 1

            import math
            idf = [math.log(len(query_results)/d[i]) for i in range(len(d))]

            w = [[ f[j][i] * idf[i] / max(idf) for i in range(len(tokens))] for j in range(len(query_results))]

            # simplification, all ands
            rank = [sum([w_i_doc**len(query_results) for w_i_doc in w_doc])**(1/len(query_results)) for w_doc in w]

            for i in range(len(query_results)):
                result=query_results[i]
                content=result[2]
                print(tokens[0] in result[2])
                if(tokens[0] in result[2]):
                    for token in tokens:
                        content=content.replace(token, "<span class=selected>" + token + "</span>")
                    search_results.append(
                        {
                            "document_id" : result[0],
                            "title" : result[1],
                            "content" : content,
                            "url" : "url",
                            "summary" : content[max(0, result[2].find(tokens[0])-100):result[2].find(tokens[0])+len(tokens[0])+100]+"...",
                            "rank" : round(rank[i],2)
                        }
                    )
            # sorting by rank
            search_results = sorted(search_results, key=lambda d: d['rank'])
            search_results.reverse()
        # do not change
        total_results_count=len(search_results)
    
    if(search_request=="None" or search_request==""): search_request="Ask Me Anything..."
    search_time_sec=time.time()-search_time_sec;
    return render_template("search.html", search_request=search_request, total_results_count=total_results_count, search_results=search_results, search_time_sec=round(search_time_sec, 5))

    pass
    if request.method == "POST":
        json_data = request.get_json()
        print(json_data)

    results = {'results count': 10}
    return jsonify(results)