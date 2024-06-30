import string
import re
import sys


class ExtractiveModel:

    am_sent_endings = r'\?|\!|\።|\፡፡'
    am_punctuation = '፠፡።፣፤፥፦፧፨“”‘’…‹‹››·•'
    am_numbers = '፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼'
    am_random = '�©\uf0c4\uf0d8\uf0a7\uf066\uf0d8'
    stop_words = open('stopwords.txt', encoding='utf-8').read().split()

    def __init__(self, text):
        self.raw_text = text
        self.clean_text = None
        self.sentences = None
        self.words = None

        self.process_text()

    def process_text(self):
        self.clean_text = self.clean_minimized(self.raw_text)
        self.sentences = self.extract_sentences(self.clean_text)
        self.sentences = self.remove_duplicate_sentence(self.sentences)
        self.words = self.extract_words(self.clean_text)

    def extract_sentences(self, text=None):
        if text is None:
            text = self.raw_text
        sentences = re.split(self.am_sent_endings, text)
        return sentences

    def extract_words(self, text):
        return text.split()

    def clean_minimized(self, text):
        words = text.split()
        to_clean = string.punctuation + self.am_numbers + self.am_random + string.ascii_letters + string.digits + self.am_punctuation
        to_clean = re.sub(self.am_sent_endings, '', to_clean)
        table = str.maketrans('', '', to_clean)
        stripped = [w.translate(table) for w in words]
        clean_txt = list(filter(None, stripped))
        return ' '.join(clean_txt)

    def remove_duplicate_sentence(self, sentences):
        duplicates = []
        cleaned = []
        for s in sentences:
            if s in cleaned:
                if s in duplicates:
                    continue
                else:
                    duplicates.append(s)
            else:
                cleaned.append(s)
        return cleaned
    

def _create_dictionary_table(words) -> dict:
    frequency_table = dict()

    for wd in words:
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table

def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount_without_stop_words = 0
        words = sentence.split()
        for word in words:
            if word in frequency_table:
                sentence_wordcount_without_stop_words += frequency_table[word]

        sentence_weight[sentence] = sentence_wordcount_without_stop_words

    return sentence_weight

def _calculate_average_score(sentence_weight) -> int:
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    average_score = (sum_values / len(sentence_weight))

    return average_score

def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    # print(threshold)

    

    for sentence in sentences:
        # print(sentence_weight)
        if sentence in sentence_weight and sentence_weight[sentence] >= threshold//2:
            article_summary += sentence + '።'
            sentence_counter += 1

    article_summary = re.sub(r'((\b\w+\b.{1,2}\w+\b)+).+\1', r'\1', article_summary, flags=re.I)

    return article_summary


def _get_summary(tparser, threshold_parameter=1.5):
    sentences = tparser.sentences

    frequency_table = _create_dictionary_table(tparser.words)

    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    threshold = _calculate_average_score(sentence_scores)

    return _get_article_summary(sentences, sentence_scores, threshold_parameter * threshold)




# input_text = '''
# ከተለያዩ የትግራይ አካባቢዎች በመምጣት ኑሯቸውን በመቀሌ ያደረጉ በርካታ ወጣቶች፣ በከተማዋ ምንም ዓይነት የሥራ ዕድል ባለመኖሩና ከሥራ ውጪ በመሆናቸው  ከጠዋት እስከ ማታ ጊዜያቸውን ቁማር ቤት እንደሚያሳልፉ ይናገራሉ።

# ወጣቶቹ በተለይ በጦርነቱ ምክንያት ወላጀ አልባ ለሆኑ ሕፃናትና ጧሪ ቀባሪዎቻቸውን ላጡ አቅመ ደካማ አረጋውያን ብቸኛ አስተዳዳሪ በመሆናቸው፣ የእነሱን እጅ የሚጠብቁ ቤተሰቦቻቸውን ሠርተው በቀን አንዴ እንኳን መመገብ አለመቻላቸው፣ ቤት ውስጥ ተቀምጠው የቤተሰቦቻቸውን መራብ ማየት ከባድ ስለሆነባቸው ውሏቸውን በቢንጎ፣ በፑል ቤት፣ በካርታ፣ በስፖርታዊ ጨዋታዎች ውርርድና በሌሎች የቁማር ዓይነቶች ለማድረግ መገደዳቸውን ገልጸዋል።

# የመቀሌ ከተማ ነዋሪ የሆነው ወጣት ልዑል ኃይለ፣ ‹‹በትግራይ የጥይት ድምፅ ጠፋ እንጂ ረሃብና የኑሮ ውድነት ከሥራ አጥነት ጋር ተዳምሮ ወጣቱ ተስፋ በመቁረጡ፣ ለስርቆትና ለቁማር እየተዳረገ ስለሆነ የፌዴራል መንግሥት ሊያየን ይገባል፤›› ብሏል።

# ወጣቱ አክሎም ትግራይ ክልል ከጦርነቱ ማግሥት አንፃራዊ ሰላም ቢገኝም፣ ጦርነቱ ባስከተለው ጉዳት ምክንያት አብዛኞቹ ፋብሪካዎች ከሥራ ውጪ በመሆናቸው፣ የሚጀመሩ የኮንስትራክሽን ሥራዎች ባለመኖራቸውና የተጀመሩትም ባሉበት በመቆማቸው የቀን ሥራ ማግኘት እንኳን ለወጣቱ ብርቅ እንደሆነበት ተናግሯል።

# መቀሌን ጨምሮ በክልሉ የተለያዩ ከተሞች የሚታዩ የሌብነትና የዘረፋ ወንጀሎች ከዚሁ ከሥራ አጥነትና ተስፋ መቁረጥ ጋር ተያይዘው እየተስፋፉ ነው ብሏል።
# '''




# input_text = "ተዘግቶ የነበረው መጋረጃ ሲገለጥ የሚል ርእስ የሰጠሁበት ዋናው ምክንያት እነ ሻምበል አምሃ አበበና የመሳሰሉት በመቶዎች የሚቆጠሩ ብዙ ወጣት መኮንኖች የበታች ሹሞችና ወታደሮች በኮርስ ወይም በቅርብ ጓደኞቻቸው የሀሰት ጥቆማ ተካሂዶባቸው ህይወታቸው የተቀጨበት አካለ ስንኩላን የሆኑበት ምክንያት ብዙ ሚስጢር መውጣት በመጀመሩ ነው። ኮሎኔል መርሻ ወዳጆ በመጽሐፉ ሽፋን ላይ ስለመጽሐፉ የሚከተለውን አስተያየት ሰጥተዋል። ጄኔራል አማን የጦር አለቆችን ማነጋገር መጀመራቸው የደርግ አባላቱ ሲረዱ የፍርሃትና የጭንቀት ብርድ ውስጥ ከተታቸው። ደህንነቱ ልዩ ልዩ የጦር ክፍሎችና ከፖሊስ ሠራዊት ተዛውረን የመጣን ሲሆን ከመሥሪያ ቤቴ የሰው ኃይል ሲነፃፀር ብዛት ባይኖራቸውም በተለያዩ የትምህርት ዘርፎች በዶክትሬት በማስትሬት በባችለር ዲግሪ ከዚያም ዝቅ ሲል በዲፕሎማ የተመረቁ በተጨማሪ ብዛት ያላቸው ሠራተኞች ወደ ተለያዩ ሶሻሊስት አገሮች ተልከው የመረጃና የሶሻሊስት ርእዮተ ዓለም ትምህርት የተክታተሉ አባሎች እንደነበሩ እሙን ነው። በሰሜን በኩል የነበረው የኢትዮጵያ ጦር መፈረካከስና መበተን የጀመረው ከግንቦት ቀን በኋላ እንደሆነ ግልጽ ነው። አስተያየት በእርግጥም የውጭ መረጃ ሠራተኞች ጂቡቲ ሆነው የሱማሌን መንግሥት የጦር ቢሮ ቦርቡረው ውጤት አስገኝተዋል የሚለው እውነትነት ካለው ሁላችንንም ማለትም በደህነነት መቤት ውስጥ የነበርነውን ሠራተኞች ሁሉ የሚያኮራን ነው። ከ ዓም ወዲህ የሻዕቢያና የ ወያኔ ቡድን አባሎች በጋራና በተናጠል አገር ውስጥ በስውር ይንቀሳቀሱ እንደነበር በተመሳሳይ ጂቡቲ ኬኒያ ሱማሌና በተለይም ሱዳን ውስጥ ጽሕፈት ቤቶቻቸውን ከፍተው በከፍተኛ ደረጃ ፀረ ኢትዮጵያ እንቅስቃሴ ሲያደርጉ እንደነበር ይታወቃል። ሻምበል ተስፋዬ ርስቴ በጻፉት መጽሐፍ በገጽ የውጭ አገሮች ጥናትና ምርምር ድርጅት ውስጥ እየተገናኙ ውይይት ያደርጉ እንደነበር ገልጸዋል። ስለዚህ የፕሬዚዳንት መንግሥቱ ኃማርያም ማንነትና የሚስጥር አማካሪዎቻቸው እነማን እንደነበሩ ከላይ የተገለጸው ጥሩ ማስረጃ ነው እላለሁ። በእርግጥ ከላይ ስማችሁ የተገለጸው መኮንኖች የአንድ ኮርስ መኮንኖች መሆናችሁን በወቅቱ ሻምበል ቁምላቸው ተካና ሻምበል አመሀ አበበ አንድ ቤት ውስጥ ተከራይተው ይኖሩ እንደነበር ይነገራል።"
# input_text = "በኢትዮጵያ በጥሬ ገንዘብ የሚደረጉ የገንዘብ እንቅስቃሴዎች እየቀነሱ መሆኑን መረጃዎች እያመለከቱ ነው፡፡ በአብዛኛዎቹ የኢትዮጵያ ባንኮች የሚደረጉ የገንዘብ እንቅስቃሴዎች በተለያዩ የዲጂታል አማራጮች እየተተገበሩ ነው፡፡ በተለይ በ2015 ሒሳብ ዓመት እንደ ሪከርድ የሚቆጠር አፈጻጸም መታየቱም ይገልጻል፡፡ በ2016 ሒሳብ ዓመትም ቢሆን በዲጂታል ባንክ አገልግሎት የሚንቀሳቀሱ የገንዘብ መጠን እያደገ ስለመምጣቱ እየወጡ ያሉ መረጃዎች እያመላከቱ ነው፡፡ በጥሬ ገንዘብ የሚደረግ ግብይት በከፍተኛ ደረጃ እየቀነሰ መምጣቱ ተጠቆመ:: የኢትዮጵያ ብሔራዊ ባንክ ይፋዊ መረጃ እንደሚያሳየውም፣ በተጠናቀቀው የ2015 ሒሳብ ዓመት በዲጂታል የክፍያ አማራጮች የተንቀሳቀሰው የገንዘብ መጠን ከ4.7 ትሪሊዮን ብር በላይ ደርሷል፡፡ ይህ የገንዘብ መጠን ከቀዳሚው ዓመት የ2014 የሒሳብ ዓመት ጋር ሲነፃፀር፣ ከ3.1 ትሪሊዮን ብር በላይ ብልጫ አለው፡፡ በግብይት መጠንም ቢሆን በ2014 የሒሳብ ዓመት የተፈጸመው ትራንዛክሽን ወይም ግብይት 345.7 ሚሊዮን ሲሆን፣ በ2015 ሒሳብ ዓመት ግን 1.24 ቢሊዮን ደርሷል፡፡ "
# input_text = "በኢትዮጵያ ንግድ ባንክ መረጃ መሠረት በ2016 የሒሳብ ዓመት ግማሽ ዓመት ብቻ ከ2.8 ትሪሊዮን ብር በላይ በዲጂታል የባንክ አገልግሎት ገንዘብ ማንቀሳቀስ ችሏል፡፡ ይህ ገንዘብ እንቅስቃሴ ከ494 ሚሊዮን ብር በላይ በሚሆኑ ግብይቶች ወይም ትራንዛሽኖች የተፈጸመ ነው፡፡ ይህ አፈጻጸም ከቀዳሚው ዓመት ተመሳሳይ ወቅት ጋር ሲነፃፀር፣ በግብይት የ35 በመቶ በገንዘብ መጠን ደግሞ የ118 በመቶ ዕድገት የታየበት ነው፡፡ በቀዳሚው ዓመት በሙሉ የሒሳብ ዓመት 3.2 ትሪሊዮን ብር ማንቀሳቀስ ችሎ የነበረው የኢትዮጵያ ንግድ ባንክ፣ የስድስት ወራት 2.8 ቢሊዮን ብር ማንቀሳቀስ የቻለው ከ12 ሚሊዮን በላይ የኤቲኤም ተጠቃሚ፣ ከዘጠኝ ሚሊዮን በላይ የሞባይል ባንክና ከ20 ሚሊዮን ብር በላይ በሚሆኑ ደንበኞች በመያዝ እንደሆነ ታውቋል፡፡"
# tparser = TextParser(input_text)
# # print(tparser.sentences)
# # print(tparser.words)
# article_summary = _get_summary(tparser)

# print("\n\n")
# print(input_text)
# print("===================")
# print(article_summary)