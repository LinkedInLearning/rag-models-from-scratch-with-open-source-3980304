import os
from ollama import embed
from nltk.tokenize import sent_tokenize
from database_connect_embeddings import get_psql_session, TextEmbedding
from sentence_transformers import SentenceTransformer

# import nltk
# nltk.download("punkt")
# nltk.download("punkt_tab")

def populate_vector_database(folder_path='all_articles'):

    session = get_psql_session()
    model = SentenceTransformer("SFR-Embedding-Mistral", device="cpu") #https://huggingface.co/Salesforce/SFR-Embedding-Mistral

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print("Trying: {}".format(file_path))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sentences = sent_tokenize(content)
            # embeddings = embed(model="custom_deepseek", input=sentences)["embeddings"]
            embeddings = model.encode(sentences)
            
            for i, (embedding, content) in enumerate(zip(embeddings, sentences)):
                new_embedding = TextEmbedding(embedding=embedding, content=content, file_name=filename, sentence_number=i+1)
                session.add(new_embedding)
            session.commit()

            print("Succesfully generated embeddings for: {}".format(file_path))

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

    return

populate_vector_database()
