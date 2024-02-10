import html
from flask import Flask, render_template, request, redirect, Request
app = Flask(__name__)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']

    title = "Here are your results!"
    
    result = str(search4letters(phrase, letters))

    log_request(request, result)
        
    return render_template("results.html", the_title=title,the_results=result, the_phrase=phrase, the_letters = letters)

def search4letters(phrase: str, letters: str = "aeiou") -> str:
    return set(phrase).intersection(set(letters))

def search4vowels(phrase:str) -> str:
    return set("aeiou").intersection(set(phrase))

def log_request(req: Request, res:str) -> None:
    with open("vsearch.log", 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, sep="|", file=log)
        
@app.route("/viewlog")
def view_the_log() -> html:
    with open("vsearch.log", 'r') as log:
        log_list = list()
        for line in log:
            log_list.append(line.split("|"))

    titles = ("Form Data", "Remmote_addr", "User_agent", "Results")
    return render_template('viewlog.html',
                            the_title="View Log",
                            the_row_titles=titles,
                            the_data=log_list)

if __name__ == "__main__":
    app.run(debug=True)

 