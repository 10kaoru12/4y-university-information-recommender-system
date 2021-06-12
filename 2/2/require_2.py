import sys
import MeCab
from gensim.models.word2vec import Word2Vec
import numpy as np

mt = MeCab.Tagger('')
model_path = 'gensim-model/word2vec.gensim.model'
wv = Word2Vec.load(model_path)

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
    args = sys.argv
    v1 = get_vector(open("./text/"+sys.argv[1],"r",encoding="utf_8").read())
    v2 = get_vector(open("./text/"+sys.argv[2],"r",encoding="utf_8").read())

    print(cos_sim(v1, v2))