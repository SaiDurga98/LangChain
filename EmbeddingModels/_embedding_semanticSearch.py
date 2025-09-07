# we have few documents
# User asks a question related to one in the document
# docs -> embeddings
# question -> embeddings
# Now we have 5 vectors of docs in 3D space and now the new vector which is the query we find the similarity score using cosine

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)


documents = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

query = 'tell me about bumrah'
# Creating embeddings of the docs and query using embedding model
doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)
# Cosine similarity measures angle between vectors, independent of magnitude.
# We wrap the query as [query_embedding] to make it 2-D as scikit expects → result shape is (1, N_docs), then [0] gives a simple (N_docs,) array.
#scores[i] is how similar doc i is to the query. Larger = more similar.
scores = cosine_similarity([query_embedding], doc_embeddings)[0] # pass the parameters as 2-D so doc_embeddings already in 2D

# It sorts based on similarity scores and also add index to each 
index, score = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]

print(query)
print(documents[index])
print("Similarity Score is:", score)


