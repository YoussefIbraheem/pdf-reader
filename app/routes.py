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
    try:
        retriever = PDFProcessor('./samples/gen19.pdf').as_retriever() 
        llm = LLMProcessor().get_llm()
        chatProcessor = ChatProcessor(retriever=retriever,llm=llm)
        summerizer = chatProcessor.generate_summerization()
        answer = chatProcessor.ask("What is The importance of managing wildlife trade?")
        print("Summary:", summerizer)
        print("Answer:", answer)
        return redirect(url_for('main.index'))
    except Exception as e:
        print("ERROR:", e)
        return redirect(url_for('main.index'))


