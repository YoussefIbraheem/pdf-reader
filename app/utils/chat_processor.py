from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class ChatProcessor:
    def __init__(self, retriever, llm):
        self.__prompt = hub.pull("rlm/rag-prompt")
        self.retriever = retriever
        self.llm = llm

    def __format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __build_chain(self, retriever):
        return (
            {
                "context": retriever | self.__format_docs,
                "question": RunnablePassthrough(),
            }
            | self.__prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):
        chain = self.__build_chain(self.retriever)
        result = chain.invoke(question)
        return result
