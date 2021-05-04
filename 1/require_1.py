import MeCab
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = []
output_file = open("./text/output_1.txt","w")

for i in range(1, 11):
    wikifile = open("./text/"+str(i)+".txt","r",encoding="utf_8")
    tagger = MeCab.Tagger()
    for file in wikifile:
        node = tagger.parseToNode(file)
        words = ""
        while node:
            node_features=node.feature.split(",")
            if node_features[0]=="名詞" and (node_features[1]=="一般" or node_features[1]=="固有名詞"):
                words = words+" "+node.surface
            node = node.next
    documents.append(words)

npdocs=np.array(documents)
vectorizer = TfidfVectorizer(norm=None, smooth_idf=False,max_features=100)
vecs = vectorizer.fit_transform(npdocs)

terms = vectorizer.get_feature_names()
print("単語文書行列（TF-IDF)=",file=output_file)
print("単語\t",end='',file=output_file)
for term in terms:
    print("%6s" % term, end='',file=output_file)
print("\n",file=output_file)

tfidfs = vecs.toarray()
for n, tfidf in enumerate(tfidfs):
    print("文書", n+1, "\t", end='',file=output_file)
    for t in tfidf:
        print("%8.4f" % t, end='',file=output_file)
    print("\n",file=output_file) 