from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


class ChatProcessor:
    def __init__(self, retriever, llm):
        self.__defaultPrompt = hub.pull("rlm/rag-prompt")
        self.retriever = retriever
        self.llm = llm

    def __format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __build_questions_chain(self):
        return (
            {
                "context": self.retriever | self.__format_docs,
                "question": RunnablePassthrough(),
            }
            | self.__defaultPrompt
            | self.llm
            | StrOutputParser()
        )

    def __build_summerization_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a concise assistant. You will receive document content and must return ONLY a short title that summarizes it. Do not include any explanations or extra text.",
                ),
                (
                    "Summarize this into a short, clear title. Only output the title. No explanations, no introductions:\n\n{context}"
                ),
            ]
        )

        return prompt | self.llm | StrOutputParser()

    def generate_summerization(self):
        docs = self.retriever.get_relevant_documents("summarize")
        context = self.__format_docs(docs)

        chain = self.__build_summerization_chain()
        result = chain.invoke({"context": context})

        return result

    def ask(self, question):
        chain = self.__build_questions_chain()
        result = chain.invoke(question)
        return result
