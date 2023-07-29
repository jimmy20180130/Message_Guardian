import jieba
import wordlist as wl

initScore = 0.5
niceScore = 0.1
badScore = 0.2

 
def getTextScore(text):
    cut_text = list(set(jieba.cut(text)))
    score = initScore
    
    print(score)
    for i in range(len(wl.nice_word)):
        count = cut_text.count(wl.nice_word[i])
        if count > 0:           
            score = score + niceScore #* count
        if score > 1:
            score = 1
        print(wl.nice_word[i], count, score)
            
    print(score)
    for i in range(len(wl.bad_word)):
        count = cut_text.count(wl.bad_word[i])
        if count > 0:
            score = score - badScore #* count
        if score < 0:
            score = 0
        print(wl.bad_word[i], count, score)

    print(score)
    for i in range(len(cut_text)):
        if list(jieba.cut(text)).count(cut_text[i]) > 5:
            score = 0
    print(score)
    return score

def cut_text(text):
    cut_text = list(set(jieba.cut(text)))
    return cut_text

'''
import score as s
 
s.initScore = 0.6
 
score = s.getTextScore("dfdsfasdfsda")
'''