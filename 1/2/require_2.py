import MeCab
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = []
output_file = open("./text/output_2.txt","w")

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
vectorizer = TfidfVectorizer(norm=None, smooth_idf=False)
vecs = vectorizer.fit_transform(npdocs)

terms = vectorizer.get_feature_names()

tfidfs = vecs.toarray()

print("文書番号\t",end='',file=output_file)
for n in range(1,11):
    print("文書", n, "\t", end='',file=output_file)
print("\n",file=output_file)

similarity = cosine_similarity(tfidfs)
for n, simi in enumerate(similarity):
    print("文書", n+1, "\t", end='',file=output_file)
    for t in simi:
        print("%8.4f" % t, end='',file=output_file)
    print("\n",file=output_file) 
