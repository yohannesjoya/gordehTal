import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re


stop_words = open('stopwords.txt', encoding='utf-8').read().split()

class CosineModel:

    am_sent_endings = r'\?|\!|\።|\፡፡'
    am_punctuation = '፠፡።፣፤፥፦፧፨“”‘’…‹‹››·•'
    am_numbers = '፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼'
    am_random = '�©\uf0c4\uf0d8\uf0a7\uf066\uf0d8'

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

def find_similarities(sentences, stopwords):
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    trsfm = vectorizer.fit_transform(sentences)
    text_df = pd.DataFrame(trsfm.toarray(), columns=vectorizer.get_feature_names_out(), index=sentences)
    num_sentences = text_df.shape[0]
    num_summary_sentences = int(np.ceil(num_sentences ** .5))
    similarities = cosine_similarity(trsfm, trsfm)
    avgs = []
    for i in similarities:
        avgs.append(i.mean())
    top_idx = np.argsort(avgs)[-num_summary_sentences:]
    return top_idx

def build_summary(sentences):
    sents_for_sum = find_similarities(sentences, stopwords=stop_words)
    sort = sorted(sents_for_sum)
    print('Number of selected sentences', len(sort))
    sent_list = sentences
    print('Total number of sentences', len(sent_list))
    sents = []
    for i in sort:
        sents.append(sent_list[i].replace('\n', '') + '።')
    summary = ' '.join(sents)
    return summary





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
# print(tparser.sentences)
# print(tparser.words)


# print("\n\n")
# print(input_text)
# print("===================")
# print(article_summary)