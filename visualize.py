import streamlit as st
from utils.check_ipo import check_ipo


data_list = check_ipo()

st.sidebar.title("이메일 입력")
st.sidebar.write("이메일 주소를 입력하시면 결과를 이메일로 받아보실 수 있습니다.")
email = st.sidebar.text_input("이메일 주소를 입력하세요", value="")

# 각 데이터 항목에 대해
for data in data_list:
    # 타이틀
    st.title(data['title'])

    # 쿼리
    st.header("LLM Question")
    st.write(data['query'])

    # 긍정적인 의견과 부정적인 의견
    st.header("Result")
    if "부정적인 의견:" in data['result']:
        st.subheader("긍정적인 의견:")
        st.write(data['result'].split("부정적인 의견:")[0])

        st.subheader("부정적인 의견:")
        st.write(data['result'].split("부정적인 의견:")[1])
    else:
        st.write(data['result'])

    # 소스 문서
    st.header("Source Documents")
    for i, doc in enumerate(data['source_documents']):
        st.subheader(f"Document {i+1}")
        st.write(doc)

    # 구분선 추가 (선택 사항)
    st.markdown("---")