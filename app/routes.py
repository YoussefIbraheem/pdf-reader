from app import render_template , Blueprint , blueprint , redirect, url_for
from app.utils.llm_processor import LLMProcessor
from app.utils.pdf_processor import PDFProcessor
from app.utils.chat_processor import ChatProcessor



@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/chat')
def chat():
    return render_template('chat.html')

@blueprint.route('/pdf-test')
def pdfTest():  
    retriever = PDFProcessor('./test.pdf').as_retriever() 
    llm = LLMProcessor().get_llm()

    answer = ChatProcessor(retriever=retriever,llm=llm).ask('summerize this file content')
    print('-----')  
    print(answer)
    print('-----')
    return redirect(url_for('main.index'))


