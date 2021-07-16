import sys
import json  
# import jsonurl 
import jieba
import jieba.posseg as pseg
import jieba.analyse

from random import sample

from config import *

class TextAnalyzer():
    def __init__(self, raw_text: str, KGB: dict, followup: bool):
        self.raw_text = raw_text
        self.KGB = KGB
        self.followup = followup

    def run(self) -> list:
        if not self.followup:
            kept_entities, kept_nouns, kept_time = self.split_entities()
            entities, attrs = self.process_entities(kept_entities, kept_nouns, kept_time)
            if not entities:
                return self.send_message('NoEntity')

            json_results = self.trigger_json(entities, attrs)
            web_queries = self.json_to_web_query(json_results)

            return web_queries, True
        else:
            return [''], True

    def split_entities(self):
        # 初始化Jiaba分词器
        jieba.load_userdict(DICT_PATH)

        # 词性提取
        segments = pseg.cut(self.raw_text)

        kept_entities = list()
        kept_nouns = list()
        kept_time = list()

        # 重要性提取
        sig_word = jieba.analyse.extract_tags(self.raw_text)
        
        # 检查是否是英语单词
        def isEnglish(s):
            try:
                s.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                return False
            else:
                return True

        def isStopWord(s):
            return s in STOP_WORDS
                
        eng_entity = ''

        for word in sig_word:
            if isEnglish(word) and not isStopWord(word):
                eng_entity += ' '+word

        if not eng_entity:
            kept_nouns.append(eng_entity[1:].lower())
        
        # 提取数量词、名词以及事先保存好的实体名词
        for w in segments:
            if w.flag == 'x' and w.word in self.KGB['entity_relations']:
                kept_entities.append(self.KGB['entity_relations'][w.word]['entity_name'])
            elif w.flag == 'n':
                kept_nouns.append(w.word)
            elif w.flag in ['m',' t']:
                kept_time.append(w.word)
            
        return kept_entities, kept_nouns, kept_time

    def process_entities(self, entities: list, nouns: list, time: list):
        attrs = dict()
        
        #先处理时间
        concat_time = ''.join(time)
        attrs['time_unit'] = 'default'
        attrs['period'] = 'default'

        for char_ in concat_time:
            if char_ in self.KGB['time_unit_relations']:
                attrs['time_unit'] = self.KGB['time_unit_relations'][char_]
            elif char_ in self.KGB['number_relations']:
                attrs['period'] = self.KGB['number_relations'][char_]
            else:
                pass
        
        #再处理名词
        attrs['visual_type'] = 'default'
        attrs['company'] = 'default'

        for noun in nouns:
            if noun.lower() in self.KGB['chart_relations']:
                attrs['chart_relations'] = self.KGB['chart_relations'][noun]
            elif noun.upper() in self.KGB['company_relations']:
                attrs['company'] = self.KGB['company_relations'][noun]
            else:
                pass
            
            if not entities:
                for ent in self.KGB['entity_relations']:
                    if noun.lower() in ent or ent in noun.lower():
                        entities.append(self.KGB['entity_relations'][ent]['entity_name'])

        # 最后返回独立实体及附属特征
        return list(set(entities)), attrs

        # if not entities:
        #     return send_message('NoEntity')
        # else:
        #     return json_to_web_query(trigger_json(entities, attrs))

    def trigger_json(self,entities: list,attrs: dict):
        json_results = []

        for ent in entities:
            reqs = self.KGB['entity_relations'][ent]['requirement'].keys()

            result = dict()

            # To confirm
            result['entity'] = ent

            for req in reqs:
                if req in attrs:
                    if attrs[req] == 'default':
                        result[req] = self.KGB['entity_relations'][ent]['requirement'][req]
                    else:
                        result[req] = attrs[req]
                else:
                    result[req] = self.KGB['entity_relations'][ent]['requirement'][req]

            # Convert dict to json
            json_result = json.dumps(result, indent = 4)
        
            json_results.append(json_result)

        return json_results
    
    def json_to_web_query(self, jsons):
        queries = []

        for json in jsons:
            queries.append(json)

        return queries

    def send_message(self, message_type):
        if message_type == 'NoEntity':
            return_msg = "没找到合适的请求。您想看的是否是："
            for ent in sample(self.KGB['entity_relations'].keys(),3):
                return_msg += ' ' + ent
            return_msg += '?'
            return return_msg, False
        else: # TODO: Messages for follow-up questions
            return '', False


        
