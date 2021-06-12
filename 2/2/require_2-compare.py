import sys
import MeCab
from gensim.models.word2vec import Word2Vec
import numpy as np

mt = MeCab.Tagger('')
model_path = 'gensim-model/word2vec.gensim.model'
wv = Word2Vec.load(model_path)
output_file = open("./text/output.txt","w")

# テキストのベクトルを計算
def get_vector(text):
    try:
        sum_vec = np.zeros(50)
        word_count = 0
        node = mt.parseToNode(text)
        while node:
            fields = node.feature.split(",")
            # 名詞、動詞、形容詞に限定
            if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':
                sum_vec += wv[node.surface]
                word_count += 1
            node = node.next
    except KeyError as error:
        print(error)

    return sum_vec / word_count


# cos類似度を計算
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


if __name__ == "__main__":
    print("文書番号\t",end='',file=output_file)
    for n in range(1,11):
        print("book", n, "\t", end='',file=output_file)
    print("\n",file=output_file)
    for i in range(1, 11):
        comparator = get_vector(open("./text/book"+str(i)+".txt","r",encoding="utf_8").read())
        print("book", i, "\t", end='',file=output_file)
        for j in range(1, 11):
            target = get_vector(open("./text/book"+str(j)+".txt","r",encoding="utf_8").read())
            print("%8.3f"%cos_sim(comparator, target),end="",file=output_file)
        print("\n",file=output_file) 