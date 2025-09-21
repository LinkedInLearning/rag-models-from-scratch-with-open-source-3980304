from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

# Connect to PostgreSQL                                                                                                                                                                                                                     
def get_psql_session():
    engine = create_engine('postgresql://postgres:postgres@localhost/text_embeddings')
    Base.metadata.create_all(engine)

    # Create a session                                                                                                                                                                                                                      
    Session = sessionmaker(bind=engine)
    return Session()

print(get_psql_session())

class TextEmbedding(Base):
    __tablename__ = 'text_embeddings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    content = Column(String)
    file_name = Column(String)
    sentence_number = Column(Integer)

    def __str__(self):
        return self.content + " " + str(self.id)
    
def insert_embeddings(embeddings, contents, file_names, session):
    for embedding, content, file_name in zip(embeddings, contents, file_names):
        new_embedding = TextEmbedding(embedding=embedding, content=content, file_name=file_name)
        session.add(new_embedding)
    session.commit()
