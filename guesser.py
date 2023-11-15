from random import choice
import yaml
from rich.console import Console
import pandas as pd
import collections
import numpy as np
import scipy.stats as stats
from collections import Counter, defaultdict
from itertools import zip_longest



class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain that character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''

    def __init__(self, manual):
        self.word_list = yaml.load(open('./data/wordlist.yaml'), Loader=yaml.FullLoader)
        self._manual = manual
        self.console = Console()
        self.tried = []
        self.WL = pd.read_csv('./data/entirewordlist.csv').word.to_list()
        self.WL2 = pd.read_csv('./data/unigram_final.csv').word.to_list()
        self.pw = self.WL.copy()
        self.tried_edge = []
        self.condition = False
        self.critic = self.WL2.copy()
        

        
    
    def restart_game(self):
        self.tried = []
        self.pw = self.WL.copy()
        self.tried_edge = []
        self.condition = False
        self.critic = self.WL2.copy()
        

    def get_pattern(self,word1,word2): #right
        counts = Counter(word1)
        pattern = []
        for i, letter in enumerate(word2):
            if word2[i] == word1[i]:
                pattern+=word2[i]
                counts[word2[i]]-=1
            else:
                pattern+='+'
        for i, letter in enumerate(word2):
            if word2[i] != word1[i] and word2[i] in word1:
                if counts[word2[i]]>0:
                    counts[word2[i]]-=1
                    pattern[i]='-'
        return ''.join(pattern)

    def get_possible_word(self, word, lista):
        pattern_d = {d: self.get_pattern(d, word) for d in lista}
        out = defaultdict(list)
        for k, v in pattern_d.items():
            out[v].append(k)
        return out

    def edge_case(self, result):
        s = ''
        pos, pos2 = result.index('+'), result.rindex('+')

        if pos == pos2:
            l1 = [i[pos] for i in self.pw]
            s = ''.join(l1)
            if len(s) > 5:
                s = s[:5]
        else:
            
            l1,l2 = list({i[pos] for i in self.pw}) , list({i[pos2] for i in self.pw})
            l2 = [i for i in l2 if i not in l1]
            ll1, ll2 = len(l1), len(l2)
            if ll1 + ll2 > 5:
                if min(ll1, ll2) >= 2:
                    if ll1>ll2:
                        s = ''.join(l1[:3] + l2[:2])
                    else:
                        s = ''.join(l1[:2] + l2[:3])
                else:
                    if ll1>ll2:
                        s = ''.join(l1[:4] + l2[:1])
                    else:
                        s = ''.join(l1[:1] + l2[:4])
            elif ll1 + ll2 == 5:
                s = ''.join(l1 + l2)
            else:
                s = ''.join(l1 + l2)
                s = s.ljust(5, 'y')
        
        if len(s) < 5: #last check 
            s = s.ljust(5, 'x')
        return s
    

    def most_common(self):
        d = [Counter(chars) for chars in list(zip_longest(*self.pw))]
        mc = ''        

        for i in d:
            for j in i.most_common(50):
                if (j[0] not in mc) and (j[0] not in list(''.join(self.tried))):
                    mc += j[0]
                    break
            if len(mc)==5:
                break
        if len(mc)<5:
            if len(mc)==0:
                mc = 'xxxxx'
            else:
                mc = mc.ljust(5, mc[0])
                    
        return mc 

    def dummy_entropy(self):
        d ={}
        for i in self.pw:
            l = [self.get_pattern(i,j) for j in self.pw if j!=i]
            counter = collections.Counter(l)
            prob = [counter[i] / sum(counter.values()) for i in counter]
            entropy = 0
            for k in prob:
                entropy += k * np.log2(1/k)
            d[i] = entropy
        
        return (max(d.values()), [i for i in d if d[i] == max(d.values())])

    def get_guess(self, result):
        '''
        This function must return your guess as a string. 
        '''
        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        else:
            '''
            CHANGE CODE HERE
            '''
            
            if result == '+++++' and self.tried == []:
                guess = 'salet'
            
            elif self.condition is False and self.tried != []:
                self.pw = self.get_possible_word(self.tried[-1], self.pw)[result]
                self.critic = self.get_possible_word(self.tried[-1],self.critic)[result]
                if self.pw != []:
                    if len(self.tried) < 5:
                        c = Counter(result)
                        if (c['+'] == 1 or c['+'] == 2) and c['-'] ==0 and len(self.pw) >= 3 and self.tried_edge == []\
                            or (self.tried[-1] in self.tried_edge and len(self.pw) >= 3) :
                            edge = self.edge_case(result)
                            self.pw.append(self.edge_case(result))
                        self.pw.append(self.most_common())
                        guess = self.dummy_entropy()[1][0]
                    else:
                        guess = self.dummy_entropy()[1][0]
                else:
                    self.condition = True
                    self.pw = self.critic

    
                    if self.pw != []:
                        guess = self.dummy_entropy()[1][0]
                    else:
                        desperate = choice(self.WL)
                        while desperate in self.tried:
                            desperate = choice(self.WL)
                        guess = desperate


            elif self.condition is True:
                
                    
                self.pw = self.get_possible_word(self.tried[-1], self.pw)[result]
                c = Counter(result)
                
                if len (self.pw) != 0:
                    if len(self.tried) < 5:
                        c = Counter(result)
                        if (c['+'] == 1 or c['+'] == 2) and len(self.pw) >= 3 and self.tried_edge == []\
                            or (self.tried[-1] in self.tried_edge and len(self.pw) >= 3) :
                            edge = self.edge_case(result)
                            self.pw.append(self.edge_case(result))
                        self.pw.append(self.most_common())
                        guess = self.dummy_entropy()[1][0]
                    else:
                        guess = self.dummy_entropy()[1][0]
            

                else:
                    desperate = choice(self.WL)
                    while desperate in self.tried:
                        desperate = choice(self.WL)
                    guess = desperate

                

            self.tried.append(guess)            
            self.console.print(guess)
            return guess 



        