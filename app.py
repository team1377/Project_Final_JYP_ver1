import streamlit as st
import google.generativeai as genai

# Streamlit secrets에서 Gemini API 키 가져오기
GOOGLE_API_KEY = st.secrets["GOOGLE"]["api_key"]

# Google Gemini 설정
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# CSS 스타일 주입
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f0;
        font-family: 'Arial', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow-y: auto; /* 세로 스크롤바 표시 */
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        margin-top: 100px;
        width: 100%;
        background-color: #4CAF50;
        padding: 10px 0;
    }
    .header img {
        width: 100px;
        margin-right: 20px;
    }
    .header h1 {
        color: white;
        margin: 0;
    }
    .input-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }
    .stTextInput > div > div > input {
        padding: 10px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        width: 50%;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
        margin-left: 130px; /* 전송 버튼을 입력 필드의 오른쪽으로 */
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stMarkdown {
        font-size: 18px;
    }
    .menu-container {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 페이지 상단에 배너 이미지 추가
st.markdown('<div class="header"><img src="3.jpeg"><h1>현지 데이터 기반 로컬 맛집</h1></div>', unsafe_allow_html=True)

# 일본 지역 목록
japan_regions = [
    "홋카이도", "아오모리", "이와테", "미야기", "아키타", "야마가타", "후쿠시마",
    "이바라키", "토치기", "군마", "사이타마", "치바", "도쿄", "카나가와",
    "니가타", "도야마", "이시카와", "후쿠이", "야마나시", "나가노", "기후",
    "시즈오카", "아이치", "미에", "시가", "교토", "오사카", "효고", "나라",
    "와카야마", "돗토리", "시마네", "오카야마", "히로시마", "야마구치",
    "도쿠시마", "가가와", "에히메", "고치", "후쿠오카", "사가", "나가사키",
    "구마모토", "오이타", "미야자키", "가고시마", "오키나와"
]

# 목적지 입력 받기
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)
destination_input = st.selectbox("여행지를 선택해주세요", japan_regions, key="destination_input")
st.markdown('</div>', unsafe_allow_html=True)

# "메뉴를 선택해주세요" 출력
st.markdown('<div class="menu-container">', unsafe_allow_html=True)
st.markdown('<p>메뉴를 선택후 체크해주세요</p>', unsafe_allow_html=True)

# 메뉴 체크박스 추가 
st.markdown('<div class="menu-container">', unsafe_allow_html=True)
menu_options = ["라멘", "스시", "오코노미야키", "규동"]
selected_menus = []
for menu in menu_options:
    selected = st.checkbox(menu)
    if selected:
        selected_menus.append(menu)
# 사용자 입력을 위한 텍스트 필드 추가
custom_menu = st.text_input("이외에 원하는 메뉴가 있다면 직접 입력 해보세요")
if custom_menu:
    selected_menus.append(custom_menu)
st.markdown('</div>', unsafe_allow_html=True)

# 사용자 입력 및 버튼 클릭 처리
if st.button("전송"):
    destination = st.session_state.destination_input
    menu_query = ", ".join(selected_menus)
    query = f"\"{menu_query}\" {destination} tabelog.com 사이트를 기반으로 일본 지역에 위치한 현재 영업중인 별 점수가 5점에 가까운 랭킹 1위~5위 맛집, 가게 리뷰, 상세 정보와 가게 정보(주소,전화번호,영업시간,가격대) 함께 추천 해주세요"
    
    # "로컬 찐 맛집을 찾고 있어요. 조금만 기다려주세요" 문구 출력
    loading_text = st.empty()
    loading_text.markdown("로컬 찐 맛집을 찾고 있어요. 조금만 기다려주세요...")
    
    # spin.gif 이미지 출력
    spinner = st.image("spin.gif", width=200)
    
    # 모델에 사용자 입력 전달하여 응답 생성
    response = gemini_model.generate_content(query)
    # 생성된 응답 출력 (스크롤 가능한 텍스트 상자에)
    response_text = response.candidates[0].content.parts[0].text
    
    # 응답을 표시하기 전에 loading_text를 클리어합니다.
    loading_text.empty()
    spinner.empty()
    
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    st.text_area("쩝쩝박사gemini의 답변입니다", value=response_text, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # main div 마감
