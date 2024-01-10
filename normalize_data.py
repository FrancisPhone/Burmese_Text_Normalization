from myanmartools import ZawgyiDetector
from icu import Transliterator
import json
import re


class Normalization(object):
    """
    This object normalizes common errors for Burmese Language.
    Though some of the functions can be used any-level of Burmese text but some are not.
    Some of the function can only be used after the syllable segmentation.
    """
    def __init__(self):
        self.detector = ZawgyiDetector()
        self.converter = Transliterator.createInstance('Zawgyi-my')
        pass
    
    def validate_sequence(self, sent):
        sent = sent.replace('့်', '့်').replace('််', '်').replace('ိိ', 'ိ').replace('ီီ', 'ီ').replace('ံံ', 'ံ').replace('ဲဲ', 'ဲ')
        sent = sent.replace('စျ', 'ဈ').replace('ဥ့်', 'ဉ့်').replace('ဥ်', 'ဉ်')
        sent = sent.replace('ဩော်', 'ဪ').replace('သြော်', 'ဪ').replace('သြ', 'ဩ')
        sent = sent.replace('ဉီ', 'ဦ').replace('ဦ', 'ဦ')
        return sent
    
    def remove_whitespace(self, sent):
        sent = sent.replace('\u200a', '')
        sent = sent.replace('\u200b', '')
        sent = sent.replace('\u200c', '')
        sent = sent.replace('\u200d', '')
        sent = sent.replace('\u200e', '')
        sent = sent.replace('\u200f', '')
        sent = sent.replace('\xa0', '')
        sent = sent.replace('•', '')
        sent = sent.replace('\u202d', '')
        return sent
    
    def walone_to_thonenya(self,matchobj):
        print(matchobj.group())
        return matchobj.group().replace("ဝ", "၀")
        
    def normalize_walone_to_thonenya(self,text):
        myan_encoded = re.sub(r"[၀-၉]+ ဝ+ [၀-၉]+", self.walone_to_thonenya, text)
        return myan_encoded
    
    def thonenya_to_walone(self,matchobj):
        return matchobj.group().replace("၀", "ဝ")

    def normalize_thonenya_to_walone(self, text):
        myan_encoded = re.sub(r'[က-ဪဿ၊-၏]+ [၀]+ [က-ဪဿ၊-၏]+', self.thonenya_to_walone, text)
        return myan_encoded
    
    def zero_to_walone(self, matchobj):
        return matchobj.group().replace("0", "ဝ")

    def normalize_zero_to_walone(self, text):
        myan_encoded = re.sub(r'[က-ဪဿ၊-၏]+ [0]+ [က-ဪဿ၊-၏]+', self.zero_to_walone, text)
        return myan_encoded
    
    def salone_yapint_to_zamyin_zwe(self,matchobj):
        return matchobj.group().replace("စျ", "ဈ")

    def normalize_salone_yapint_to_zamyin_zwe(self,text):
        myan_encoded = re.sub(r'စျ', self.salone_yapint_to_zamyin_zwe, text)
        return myan_encoded

    def colon_to_witsa_nalone_pout(self, matchobj):
        return matchobj.group().replace(":", "း")

    def normalize_colon_to_witsa_nalone_pout(self, text):
        myan_encoded = re.sub(r'[က-ဪဿ၊-၏]+ [:]+ [က-ဪဿ၊-၏]+', self.colon_to_witsa_nalone_pout, text)
        return myan_encoded

    def yagauk_to_khon(self, matchobj):
        return matchobj.group().replace("ရ", "၇")

    def normalize_yagauk_to_khon(self,text):
        myan_encoded = re.sub(r'[၀-၉]+ [ရ]+ [၀-၉]+', self.yagauk_to_khon, text)
        return myan_encoded
    
    def oot_to_nyalay(self, matchobj):
        return matchobj.group().replace("ဥ", "ဉ")

    def normalize_oot_to_nyalay(self,text):
        myan_encoded = re.sub(r'[က-၏]+ဥ', self.oot_to_nyalay, text)
        return myan_encoded
    
    def nyalay_to_oot(self, matchobj):
        return matchobj.group().replace("ဉ", "ဥ")
        
    def normalize_nyalay_to_oot(self, text):
        myan_encoded = re.sub(r'[က-၏]+ ဉ ', self.nyalay_to_oot, text)
        return myan_encoded

    def htar_to_nhar(self, matchobj):
        return matchobj.group().replace("ဌား", "ငှား")

    def normalize_htar_to_nghar(self, text):
        myan_encoded = re.sub(r'ဌား', self.htar_to_nhar, text)
        return myan_encoded
    
    def wa_yaycha_to_ta(self, matchobj):
        return matchobj.group().replace("ဝာ", "တ")

    def normalize_wa_yaycha_to_ta(self, text):
        myan_encoded = re.sub(r'ဝာ', self.oot_to_nyalay, text)
        return myan_encoded

    def eng_num(self, matchobj):
        myan_eng_nums = {
                            "0": "၀",
                            "1": "၁",
                            "2": "၂",
                            "3": "၃",
                            "4": "၄",
                            "5": "၅",
                            "6": "၆",
                            "7": "၇",
                            "8": "၈",
                            "9": "၉"}
        num_list = []
        NUMBER_PATTERN2 = r'[a-zA-Z]+'
        number_match2 = re.split(NUMBER_PATTERN2, matchobj.group())
        print(number_match2)
        for i in number_match2:
            if i != "":
                for k in i:
                    if k in myan_eng_nums.keys():
                        num_list.append(myan_eng_nums[k])
        return "".join(num_list)

    def eng_myan_num_encoder(self,text):
        text_list = []
        for l in text.split():
            text_list.append(re.sub(r'[0-9]+', self.eng_num, l))
            text_list.append(" ")
        encoded_text = "".join(text_list)
        return encoded_text.strip()
    
    def phone_number_encoder(self, text):
        phone_number_encoded = re.sub(r'((09|01|\+?959)\d{6,12})|((၀၉|၀၁|\+?၉၅၉)[၀-၉]{6,12})', "@", text)
        return phone_number_encoded

    def space_numbers(self, matchobj):
        return " ".join([i for i in matchobj.group() if i != " "])

    def find_and_space_numbers(self, text):
        english_number_encoded = re.sub(r'[၀-၉0-9./\-]+', self.space_numbers, text)
        return english_number_encoded
    
    def eng_word_encoder(self, text):
        eng_word_encoded = re.sub(r'[a-zA-Z./\-]+', "#", text)
        return eng_word_encoded
    
    def space_encodings(self, matchobj):
        return " ".join([i for i in matchobj.group() if i != " "])

    def find_and_space_encodings(self, text):
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+@+ [က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, text)
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+ @+[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, space_encoded)
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+@+[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, space_encoded)
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+#+ [က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, space_encoded)
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+ #+[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, space_encoded)
        space_encoded = re.sub(r'[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+#+[က-ဪဿ၊-၏a-zA-Z0-9၀-၉\(\)]+', self.space_encodings, space_encoded)
        return space_encoded
    
    def phone_number_decoder(self, input_text, output_text):
        for match in re.findall(r'((09|01|\+?959)\d{6,12})|((၀၉|၀၁|\+?၉၅၉)[၀-၉]{6,12})', input_text):
            output_text = output_text.replace("@", match[0], 1)
        return output_text
        
    def zawgyi_unicode_converter(self, text):
        score = self.detector.get_zawgyi_probability(text)
        if score > 1e-1:
            text = self.converter.transliterate(text)
        return text

    def normalize_before_syll_break(self, text):
        # This normalizations can be used before syllable break
        text = self.remove_whitespace(text)
        text = self.validate_sequence(text)
        text = self.sent_level_norm(text)
        text = self.zawgyi_unicode_converter(text)
        return text
    
    def normalize_after_syll_break(self,text):
        # This normalizations can be only used after syllable break
        text = text.replace('"', "'")
        text = text.replace(',', ' , ')
        text = self.normalize_walone_to_thonenya(text)
        text = self.normalize_thonenya_to_walone(text)
        text = self.normalize_zero_to_walone(text)
        text = self.normalize_salone_yapint_to_zamyin_zwe(text)
        text = self.normalize_colon_to_witsa_nalone_pout(text)
        text = self.normalize_yagauk_to_khon(text)
        text = self.normalize_oot_to_nyalay(text)
        text = self.normalize_nyalay_to_oot(text)
        text = self.normalize_htar_to_nghar(text)
        text = self.normalize_wa_yaycha_to_ta(text)
        text = self.eng_myan_num_encoder(text)
        return text

    def sent_level_norm(self, sent):

        json_rules = '[{ "from": "([\u102B-\u1035]+)([\u103B-\u103E]+)", "to": "\\\\2\\\\1" }, { "from": "([\u102D\u102E\u1032]{0,})([\u103B-\u103E]{0,})([\u102F\u1030]{0,})([\u1036\u1037\u1038]{0,})([\u102D\u102E\u1032]{0,})", "to": "\\\\2\\\\1\\\\5\\\\3\\\\4" }, { "from": "(^|[^\u1000-\u1021\u103B-\u103E])(\u1031)([\u1000-\u1021])((?:\u1039[\u1000-\u1021])?)([\u103B-\u103E]{0,})", "to": "\\\\1\\\\3\\\\4\\\\5\\\\2" }, { "from": "\u1037\u102C", "to": "\u102C\u1037" }, { "from": "\u103E\u103B", "to": "\u103B\u103E" }, { "from": "([\u102B-\u103E])\\\\1+", "to": "\\\\1" }, { "from": "(\u103D\u103E)+", "to": "\u103D\u103E" }, { "from": "(\u102F\u1036)+", "to": "\u102F\u1036" }, { "from": "([\u102D\u102E])\u1030", "to": "\\\\1\u102F" }, { "from": "([\u1000-\u1021])(\u1036)(\u103D)(\u1037)", "to": "\\\\1\\\\3\\\\2\\\\4" }, { "from": "([\u1000-\u1021])(\u102D)(\u1039)([\u1000-\u1021])", "to": "\\\\1\\\\3\\\\4\\\\2" }, { "from": "([\u1000-\u1021])(\u1036)(\u103E)", "to": "\\\\1\\\\3\\\\2" }, { "from": "\u1037\u102F", "to": "\u102F\u1037" }, { "from": "\u1036\u103D", "to": "\u103D\u1036" }, { "from": "(\u1004)(\u1031)(\u103A)(\u1039)([\u1000-\u1021])", "to": "\\\\1\\\\3\\\\4\\\\5\\\\2" }, { "from": "(\u102D)(\u103A)+", "to": "\\\\1" }, { "from": "([\u1000-\u1021])(\u1031)(\u103D)", "to": "\\\\1\\\\3\\\\2" } , { "from": "([\u1000-\u1021])(\u1031)(\u103E)(\u103B)", "to": "\\\\1\\\\3\\\\4\\\\2" }]'
        rules = json.loads(json_rules)
        for rule in rules:
            sent = re.sub(rule["from"], rule["to"], sent)
        return sent 
    
    def del_miss_char(self, corpus_main_ls):
        fine_sent = []
        fau_sent = []
        for sent in corpus_main_ls:
            if '�' in sent:
                fau_sent.append(sent)
            else:
                fine_sent.append(sent)

        return fine_sent, fau_sent


norm = Normalization()
text = "1သိန္းဖိုး၀၀လင္လင္စားပါ 09777444222 ကိုဆက္ပါ"
norm_text = norm.normalize_before_syll_break(text)
norm_text = norm.normalize_after_syll_break(norm_text)
phone_encoded_text = norm.phone_number_encoder(norm_text)
print("input text:", text)
print("output text:", norm_text)
print("phone encoded text:", phone_encoded_text)