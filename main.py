from utils.crawl import crawl_ipo38, crawl_naver_blog
from utils.search import search_naver_blog
from utils.txt_writer import write_txt
from utils.translate import translate_korean_to_english
from utils.llm import call_langchain
from utils.create_ipo import create_ipo
from utils.check_ipo import check_ipo

def run(kor_stock_name, eng_stock_name, query):
    ipo_name = search_naver_blog(kor_stock_name)

    naver_blog_url_list = [
        doc["url"] for doc in ipo_name["documents"] if "blog.naver" in doc["url"]
    ]

    contents = crawl_naver_blog(naver_blog_url_list)

    is_success = write_txt(contents, eng_stock_name)

    if is_success == "Success":
        result = call_langchain(eng_stock_name, query)

        create_ipo(kor_stock_name, result)

if __name__ == "__main__":
    exists_ipos = check_ipo()
    exists_ipo_list = [ipo["title"] for ipo in exists_ipos]
    df = crawl_ipo38()
    recent_stock_list = df["종목명"][:6].tolist()

    for kor_stock_name in recent_stock_list:
        eng_stock_name = "_".join(translate_korean_to_english(kor_stock_name).split(" "))
        query = f"""{kor_stock_name} IPO 투자에 대한 적절성에 대해 긍정적인 의견 최대 3가지와 부정적인 의견 최대 3가지를 작성해주세요."""

        if kor_stock_name not in exists_ipo_list:
            run(kor_stock_name, eng_stock_name, query)

        print(kor_stock_name, "is done")