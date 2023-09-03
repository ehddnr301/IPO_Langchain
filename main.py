from utils.crawl import crawl_ipo38, crawl_naver_blog
from utils.search import search_naver_blog
from utils.txt_writer import write_txt
from utils.translate import translate_korean_to_english
from utils.llm import call_langchain

if __name__ == "__main__":
    df = crawl_ipo38()

    kor_stock_name = df["종목명"].iloc[2]
    eng_stock_name = "_".join(translate_korean_to_english(kor_stock_name).split(" "))
    query = (
        f"""{kor_stock_name} IPO 투자에 대한 적절성을 Yes Or No 로 만 표시해준 뒤에 다음 줄에 근거를 이야기 해줘"""
    )

    ipo_name = search_naver_blog(kor_stock_name)

    naver_blog_url_list = [
        doc["url"] for doc in ipo_name["documents"] if "blog.naver" in doc["url"]
    ]

    contents = crawl_naver_blog(naver_blog_url_list)

    is_success = write_txt(contents, eng_stock_name)

    if is_success:
        result = call_langchain(eng_stock_name, query)

        print(result)
