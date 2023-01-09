#coding: utf-8
#Windowsコマンドプロンプト対応
                              
FILEPATHs = ["sudachidict/small_lex.csv", "sudachidict/core_lex.csv", "sudachidict/notcore_lex.csv"]
OUTFILE = "docs/data.js"

import csv
import codecs
import random, re
import sudachipy, sudachipy.tokenizer

tokenizer = sudachipy.Dictionary().create()

def n_mora(yomi):
    #NFCかNFKCを前提
    #カタカナの読みからァィゥェォャュョを削除して文字数を数える
    #trans = str.maketrans("", "", "ァィゥェォャュョ")
    #return len(yomi.translate(trans))

    #ァアカガサザタダナハバパマャヤラワ
    #ィイキギシジチヂニヒビピミリヰ
    #ゥウクグスズツヅヌフブプムュユルヴ
    #ェエケゲセゼテデネヘベペメレヱ
    #ォオコゴソゾトドノホボポモョヨロヲ
    
    txt = re.sub(r"[キシチニヒミリギジビピ]ャ|[キシチニヒミリギジビピデテフヴ]ュ|[キシチニヒミリギジビピ]ョ|[ツフクグヴ]ァ|[テフデウクツヴ]ィ|[トド]ゥ|[シチツフジイウクヴ]ェ|[ツフウクヴ]ォ", "1", yomi)
    return len(txt)
    

def word2mora(word):
    words = tokenizer.tokenize(word, sudachipy.tokenizer.Tokenizer.SplitMode.C)
    #print([t.reading_form() for t in words])
    yomi = "".join([t.reading_form() for t in words])
    return n_mora(yomi)
    
def iskatakana(text):
    return re.match(r'^[ァ-ヾ]+$', text) is not None

def katakanize(text):
    def trans(m):
        c = m.group(0)
        return chr(ord(c)+96) #96 = -ord(ぁ)+ord(ァ)
    return re.sub(r"[ぁ-ゖ]", trans, text)
def hiraganize(text):
    def trans(m):
        c = m.group(0)
        return chr(ord(c)-96) #-96 = -ord(ァ)+ord(ぁ)
    return re.sub(r"[ァ-ヶ]", trans, text)

単語2拍 = set()
単語3拍 = set()
単語5拍 = set()
for filepath in FILEPATHs:
    with codecs.open(filepath, "r", "utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            見出し = row[4]
            品詞1 = row[5]
            品詞2 = row[6]
            品詞3 = row[7]
            読み = row[11]
            正規化表記 = row[12]
            拍数 = n_mora(読み)
            if "|" in 見出し:
                print(見出し)
            if 品詞1 != "名詞":
                continue
            # if 品詞3 in ["人名", "地名"]:
                # continue
            if 品詞2 == "固有名詞":
                continue
            if not iskatakana(読み):
                continue
            if 拍数 == 2:
                if katakanize(見出し) == 読み:
                    単語2拍.add(見出し)
                else:
                    if 見出し.isascii():
                        単語2拍.add(見出し + "|" + 読み)
                    else:
                        単語2拍.add(見出し + "|" + hiraganize(読み))
                #print(拍数, 読み, 見出し, 品詞1, 品詞2, 品詞3, 正規化表記)
            elif 拍数 == 3:
                if 読み=="キゴウ": 
                    continue
                if katakanize(見出し) == 読み:
                    単語3拍.add(見出し)
                else:
                    if 見出し.isascii():
                        単語3拍.add(見出し + "|" + 読み)
                    else:
                        単語3拍.add(見出し + "|" + hiraganize(読み))
                #print(拍数, 読み, 見出し, 品詞1, 品詞2, 品詞3, 正規化表記)
            elif 拍数 == 5:
                if katakanize(見出し) == 読み:
                    単語5拍.add(見出し)
                else:
                    if 見出し.isascii():
                        単語5拍.add(見出し + "|" + 読み)
                    else:
                        単語5拍.add(見出し + "|" + hiraganize(読み))
                #print(拍数, 読み, 見出し, 品詞1, 品詞2, 品詞3, 正規化表記)

単語2拍 = sorted(list(単語2拍))
単語3拍 = sorted(list(単語3拍))
単語5拍 = sorted(list(単語5拍))
with codecs.open(OUTFILE, "w", "utf-8") as w:
    w.write("words_2mora=[")
    w.write(",".join(['"{}"'.format(word) for word in 単語2拍]))
    w.write("];\n")
    w.write("words_3mora=[")
    w.write(",".join(['"{}"'.format(word) for word in 単語3拍]))
    w.write("];\n")
    w.write("words_5mora=[")
    w.write(",".join(['"{}"'.format(word) for word in 単語5拍]))
    w.write("];\n")
    
    
print("{}と{}と{}".format(random.choice(単語2拍), random.choice(単語3拍), random.choice(単語5拍)))