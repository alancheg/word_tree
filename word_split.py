import jieba
import re
import time

fileneedcut = r"D:\0.Inbox\wiki.zh.text.simp"
newfilename = r"D:\0.Inbox\wiki.zh.text.simp.cut"

with open(fileneedcut, 'r', encoding='utf-8') as reader:
    with open(newfilename, 'w', encoding='utf-8') as writer:
        for line in reader:
            words = jieba.cut(line)

            sentence = ''
            for w in words:
                sentence += str(w)
                sentence += ''

            # print(sentence)
            writer.writelines(sentence)
