import numpy as np
import os

# 打开文件，创建每个字的标签
def make_state(string):
    if (len(string) == 1):
        return "S"
    else:
        return "B" + (len(string) - 2) * "M" + "E"

# 这个函数里面符号被视作一个S
def make_state_file(DataFile_name):
    output_name = DataFile_name[:DataFile_name.find(".")] + "_state.txt"
    if (os.path.exists(output_name)):
        os.remove(output_name)
    data = open(DataFile_name, "r", encoding="utf-8").read().split("\n")
    with open(output_name, "w", encoding="utf-8") as f:
        for index, data_word in enumerate(data):
            if data_word:
                state = ""
                for single in data_word.split(" "):
                    state += make_state(single) + " "
            if (index != len(data)):
                state = state.strip() + "\n"
            f.write(state)
    return output_name


class HMM():
    def __init__(self, inputFile_name, outputFile_name):
        self.Ori_txt = open(inputFile_name, "r", encoding="utf-8").read().split("\n")
        self.Sta_txt = open(outputFile_name, "r", encoding="utf-8").read().split("\n")
        self.Begin_Matrix = np.zeros((4), dtype=int)
        self.Trans_Matrix = np.zeros((4, 4), dtype=float)
        self.Emiss_Matrix = {"B": {}, "M": {}, "S": {}, "E": {}}
        self.txt2num = {"B": 0, "M": 1, "S": 2, "E": 3}  # 代表BMSE
        self.Emiss_Num = [0, 0, 0, 0]
        self.num2txt = ["B", "M", "S", "E"]

    def calculate_begin(self):
        for sentence in self.Sta_txt:
            if len(sentence) > 0:
                self.Begin_Matrix[self.txt2num[sentence[0]]] += 1
        return

    def calculate_trans(self):
        for sentence in self.Sta_txt:
            if len(sentence) > 0:
                sentence = sentence.replace(" ", "")
                for i in range(len(sentence) - 1):
                    self.Trans_Matrix[self.txt2num[sentence[i]]][self.txt2num[sentence[i + 1]]] += 1

    def calculate_emmision(self):
        for ori_sentence, state_sentence in zip(self.Ori_txt, self.Sta_txt):
            for ori, state in zip(ori_sentence, state_sentence):
                if state in ["B", "M", "S", "E"]:
                    if ori not in self.Emiss_Matrix[state]:
                        self.Emiss_Matrix[state][ori] = 0
                    self.Emiss_Matrix[state][ori] += 1
                    self.Emiss_Num[self.txt2num[state]] += 1

    def nomalize(self):
        total = np.sum(self.Begin_Matrix)
        self.Begin_Matrix = self.Begin_Matrix / total
        total2 = np.zeros(4, dtype=float)
        for i in range(4):
            total2[i] = np.sum(self.Trans_Matrix[i])
            self.Trans_Matrix[i] /= total2[i]
        for state in self.Emiss_Matrix:
            for key in self.Emiss_Matrix[state].keys():
                self.Emiss_Matrix[state][key] = \
                    self.Emiss_Matrix[state][key] / self.Emiss_Num[self.txt2num[state]]
                    
    def viterbi(self, text):
        paths = [s for s in self.num2txt]
        scores = [p for p in self.Begin_Matrix]

        for w_index, w in enumerate(text):
            for p_index, path in enumerate(paths):
                if w not in self.Emiss_Matrix:
                    self.Emiss_Matrix[w] = {"B": 1, "M": 1, "S": 1, "E": 1}

                scores[p_index] *= self.Emiss_Matrix[w][path[-1]]
            if w_index == len(text) - 1:
                break
            if text[w_index + 1] not in self.Emiss_Matrix:
                self.Emiss_Matrix[text[w_index + 1]] = {"B": 1, "M": 1, "S": 1, "E": 1}
            new_s = [lp for lp in paths]
            for state in self.num2txt:
                tp_s = []
                for lp in new_s:
                    tp_s.append(
                        self.Trans_Matrix[self.txt2num[lp[-1]], self.txt2num[state]] * self.Emiss_Matrix[
                            text[w_index + 1]][state])
                max_s = self.num2txt[np.argmax(tp_s)]
                max_p = np.max(tp_s)
                paths[self.txt2num[max_s]] += state
                scores[self.txt2num[max_s]] *= max_p
        result_p = paths[np.argmax(scores)]
        cut_result = ""
        for t, p in zip(text, result_p):
            cut_result += t
            if p == "S" or p == "E":
                cut_result += " "
        print(cut_result)
        
        