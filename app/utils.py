import PyPDF2

def extract_text(path):
    if path.endswith(".pdf"):
        reader = PyPDF2.PdfReader(path)
        return " ".join(p.extract_text() for p in reader.pages)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

def chunk_text(text, size=500, overlap=100):
    
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length > size and current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            overlap_sentences = []
            overlap_length = 0
            for s in reversed(current_chunk):
                s_len = len(s.split())
                if overlap_length + s_len <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_length += s_len
                else:
                    break
            current_chunk = overlap_sentences
            current_length = overlap_length
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks