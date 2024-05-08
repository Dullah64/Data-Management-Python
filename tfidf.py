import re
from collections import defaultdict
import math

def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r') as file:
        stopwords = file.read().splitlines()
    return stopwords

def clean_document(document):
    
    cleaned_text = re.sub(r'https?://\S+\s*', '', document)
    
    
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    
   
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
   
    cleaned_text = cleaned_text.lower()
    
    return cleaned_text.strip()  

def remove_stopwords(document, stopwords):
    words = document.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

def reduce_to_root(word):
    
    if word.endswith("ing"):
        return word[:-3]  
    elif word.endswith("ly"):
        return word[:-2]  
    elif word.endswith("ment"):
        return word[:-4]  
    else:
        return word

def preprocess_documents(documents_file, stopwords_file):
    preprocessed_documents = []
    document_filenames = []
    
    
    stopwords = load_stopwords(stopwords_file)
    
    
    with open(documents_file, 'r') as file:
        documents = file.read().splitlines()
    
    
    for doc_name in documents:
        document_filenames.append(doc_name)
        
        with open(doc_name, 'r') as doc_file:
            doc_content = doc_file.read()
        
        
        cleaned_doc = clean_document(doc_content)
        
        
        filtered_doc = remove_stopwords(cleaned_doc, stopwords)
        
        
        reduced_doc = ' '.join(reduce_to_root(word) for word in filtered_doc.split())
        
        
        output_filename = "preproc_" + doc_name
        with open(output_filename, 'w') as output_file:
            output_file.write(reduced_doc)
        
       
        preprocessed_documents.append(reduced_doc)
    
    return preprocessed_documents, document_filenames

if __name__ == "__main__":
   
    preprocessed_docs, document_filenames = preprocess_documents("tfidf_docs.txt", "stopwords.txt")

    num_documents = len(preprocessed_docs)
    idf_scores = defaultdict(int)

    for doc in preprocessed_docs:
        unique_words = set(doc.split())
        for word in unique_words:
            idf_scores[word] += 1

    for word, doc_count in idf_scores.items():
        idf_scores[word] = math.log(num_documents / doc_count) + 1

    
    tfidf_scores = []

    for doc in preprocessed_docs:
        
        words = doc.split()
        total_terms = len(words)
        term_frequency = {word: words.count(word) / total_terms for word in set(words)}

        
        doc_tfidf = {word: round(tf * idf_scores[word], 2) for word, tf in term_frequency.items()}
        
        sorted_tfidf = sorted(doc_tfidf.items(), key=lambda x: (-x[1], x[0]))
        
        top_words = sorted_tfidf[:5]
        
        tfidf_scores.append(top_words)

    for i, doc_tfidf in enumerate(tfidf_scores):
        output_filename = "tfidf_" + document_filenames[i]
        with open(output_filename, "w") as f:
            f.write(str(doc_tfidf))