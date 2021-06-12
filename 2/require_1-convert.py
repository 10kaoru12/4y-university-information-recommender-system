def convert(input_file_name):
    """
    'ユーザID アイテムID 評価値'のフォーマットへ変換してファイルに出力する
    """
    output_file_name = input_file_name + '_converted' # 変換後のファイル名
    output = ''
    
    with open(input_file_name, mode='r') as f:
        lines = f.readlines()
        
        user_id = 0
        for line in lines:
            words = line.strip().split(' ')
            for item_id, word in enumerate(words):
                score = int(word)
                if score != -1:
                    if score != 0:
                        output += '{0:04d} {1:02d} {2:01d}\n'.format(user_id, item_id, score)
                    
            user_id += 1
    
    with open(output_file_name, mode='w') as f:
        f.write(output)
    
    return output_file_name


file_name = convert('./sushi3-2016/sushi3b.5000.10.score')