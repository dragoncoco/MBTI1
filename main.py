
import streamlit as st

st.set_page_config(
    page_title="MBTI로 포켓몬 찾기",
    page_icon="🌼",
    layout="centered",
)

# -------------------------------
# 디자인 CSS
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background: linear-gradient(180deg, #fff8e8, #fff4cf);
    color: #594326;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, div, button {
    font-family: 'Noto Sans KR', sans-serif;
}
.hero-pill {
    display: inline-block;
    background: #ffedb6;
    color: #805b1d;
    border-radius: 999px;
    padding: 8px 16px;
    font-size: 15px;
    font-weight: 800;
}
.hero-title {
    color: #604622;
    text-align: center;
    font-size: clamp(2.1rem, 6vw, 3.5rem);
    line-height: 1.25;
    font-weight: 900;
    margin: 16px 0 8px;
}
.hero-subtitle {
    text-align: center;
    color: #806f56;
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.4rem;
}
.section-card {
    background: rgba(255,255,255,.88);
    border: 2px solid #f0dfb7;
    border-radius: 24px;
    padding: 22px;
    margin: 10px 0 20px;
}
div.stButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 14px;
    border: 2px solid #f0dfb7;
    background: #fffaf0;
    color: #654b27;
    font-size: 1.05rem;
    font-weight: 800;
    transition: all .15s ease-in-out;
}
div.stButton > button:hover {
    border-color: #d69b32;
    background: #ffedb6;
    color: #594326;
    transform: translateY(-2px);
}
.result-card {
    background: linear-gradient(145deg, #fff0b9, #fff7dc);
    border: 2px solid #efd46d;
    border-radius: 28px;
    padding: 26px;
    text-align: center;
    animation: appear .55s ease-out;
    box-shadow: 0 12px 30px rgba(130, 99, 37, .10);
}
@keyframes appear {
    0% {opacity: 0; transform: translateY(16px) scale(.98);}
    70% {opacity: 1; transform: translateY(-2px) scale(1.01);}
    100% {opacity: 1; transform: translateY(0) scale(1);}
}
.result-tag {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: #fffaf0;
    color: #89621d;
    font-weight: 800;
    font-size: .95rem;
}
.pokemon-ko {
    font-size: clamp(2rem, 5vw, 2.8rem);
    color: #533d1d;
    font-weight: 900;
    margin: 8px 0 0;
}
.pokemon-en {
    color: #8a6b37;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 2px 0 12px;
}
.type-chip {
    display: inline-block;
    padding: 7px 13px;
    margin: 3px;
    border-radius: 999px;
    background: #fffaf0;
    border: 1px solid #f0dfb7;
    color: #75551f;
    font-weight: 800;
}
.info-card {
    background: rgba(255,255,255,.82);
    border: 1px solid #f1e2bb;
    border-radius: 18px;
    padding: 17px 19px;
    margin-top: 14px;
    text-align: left;
}
.info-card h3 {
    color: #604622;
    font-size: 1.12rem;
    margin: 0 0 8px;
}
.info-card p {
    color: #62523c;
    font-size: 1rem;
    line-height: 1.85;
    margin: 0;
}
.footer-note {
    color: #9a8767;
    text-align: center;
    font-size: .85rem;
    line-height: 1.8;
    margin-top: 26px;
}
div[data-testid="stImage"] img {
    object-fit: contain;
    max-height: 270px;
    filter: drop-shadow(0 9px 7px rgba(100,70,25,.13));
}
@media (max-width: 600px) {
    .block-container {padding-left: 1rem; padding-right: 1rem;}
    div.stButton > button {font-size: .92rem; min-height: 48px;}
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 포켓몬 데이터
# -------------------------------
POKEMON = {
    "ISTJ": {
        "ko": "거북왕", "en": "Blastoise", "number": "009",
        "types": ["물"],
        "features": "침착하고 든든하며, 강력한 물대포로 팀을 지켜요.",
        "reason": "맡은 일을 끝까지 해내는 성실함이 ISTJ와 닮았어요.\n차분하게 상황을 살피고 책임감 있게 행동하는 모습도 잘 어울려요.",
        "match": "ESFP",
    },
    "ISFJ": {
        "ko": "해피너스", "en": "Blissey", "number": "242",
        "types": ["노말"],
        "features": "상냥한 마음으로 다른 포켓몬을 돌보고 행복을 나눠요.",
        "reason": "주변 사람들을 세심하게 챙기는 모습이 ISFJ와 닮았어요.\n다른 사람에게 안정감과 따뜻함을 주는 점도 잘 어울려요.",
        "match": "ESFP",
    },
    "INFJ": {
        "ko": "뮤", "en": "Mew", "number": "151",
        "types": ["에스퍼"],
        "features": "신비로운 분위기를 지녔고 다양한 기술을 배울 수 있어요.",
        "reason": "깊이 생각하고 자신만의 가치관을 소중히 여기는 점이 INFJ와 닮았어요.\n풍부한 내면과 따뜻한 마음을 가진 이미지도 잘 어울려요.",
        "match": "ENFP",
    },
    "INTJ": {
        "ko": "뮤츠", "en": "Mewtwo", "number": "150",
        "types": ["에스퍼"],
        "features": "뛰어난 지능과 강력한 초능력을 지닌 포켓몬이에요.",
        "reason": "목표를 세우고 효율적인 방법을 찾는 모습이 INTJ와 닮았어요.\n복잡한 문제를 분석하고 전략을 세우는 이미지도 잘 어울려요.",
        "match": "ENFP",
    },
    "ISTP": {
        "ko": "메타몽", "en": "Ditto", "number": "132",
        "types": ["노말"],
        "features": "몸의 형태를 바꾸어 다른 포켓몬으로 변신할 수 있어요.",
        "reason": "상황에 맞게 유연하게 대응하는 점이 ISTP와 닮았어요.\n정해진 방식에 얽매이지 않고 실용적인 해결책을 찾는 모습도 어울려요.",
        "match": "ESTJ",
    },
    "ISFP": {
        "ko": "이브이", "en": "Eevee", "number": "133",
        "types": ["노말"],
        "features": "환경에 따라 여러 모습으로 진화할 수 있는 포켓몬이에요.",
        "reason": "자신만의 취향과 감성을 소중히 여기는 점이 ISFP와 닮았어요.\n여러 가능성을 지니고 자연스럽게 자신을 표현하는 모습도 어울려요.",
        "match": "ENFJ",
    },
    "INFP": {
        "ko": "피카츄", "en": "Pikachu", "number": "025",
        "types": ["전기"],
        "features": "볼의 전기 주머니에 전기를 모았다가 방출해요.",
        "reason": "소중한 관계와 진심을 중요하게 여기는 점이 INFP와 닮았어요.\n상상력이 풍부하고 자신만의 마음을 지키는 모습도 잘 어울려요.",
        "match": "ENFJ",
    },
    "INTP": {
        "ko": "후딘", "en": "Alakazam", "number": "065",
        "types": ["에스퍼"],
        "features": "매우 높은 지능과 강력한 초능력을 지닌 포켓몬이에요.",
        "reason": "궁금한 것을 깊이 파고들고 원리를 이해하려는 점이 INTP와 닮았어요.\n논리적으로 분석하고 독창적인 생각을 떠올리는 모습도 어울려요.",
        "match": "ENTJ",
    },
    "ESTP": {
        "ko": "루카리오", "en": "Lucario", "number": "448",
        "types": ["격투", "강철"],
        "features": "파동을 감지해 주변 상황과 상대의 움직임을 알아차려요.",
        "reason": "생각에만 머무르지 않고 직접 행동하는 모습이 ESTP와 닮았어요.\n상황에 빠르게 대응하고 기회를 포착하는 점도 잘 어울려요.",
        "match": "ISFJ",
    },
    "ESFP": {
        "ko": "푸린", "en": "Jigglypuff", "number": "039",
        "types": ["노말", "페어리"],
        "features": "노래를 불러 상대를 잠들게 하는 사랑스러운 포켓몬이에요.",
        "reason": "분위기를 즐기고 주변에 활기를 더하는 모습이 ESFP와 닮았어요.\n감정을 솔직하게 표현하고 순간을 즐기는 점도 잘 어울려요.",
        "match": "ISTJ",
    },
    "ENFP": {
        "ko": "토게피", "en": "Togepi", "number": "175",
        "types": ["페어리"],
        "features": "행복한 기운을 나누는 작고 귀여운 포켓몬이에요.",
        "reason": "새로운 가능성을 발견하고 다양한 경험을 즐기는 점이 ENFP와 닮았어요.\n주변에 희망과 즐거움을 전하는 밝은 이미지도 잘 어울려요.",
        "match": "INFJ",
    },
    "ENTP": {
        "ko": "팬텀", "en": "Gengar", "number": "094",
        "types": ["고스트", "독"],
        "features": "그림자 속에 숨어 장난을 치는 재치 있는 포켓몬이에요.",
        "reason": "기존 방식에 의문을 품고 새로운 생각을 즐기는 점이 ENTP와 닮았어요.\n재치 있는 발상과 예측하기 어려운 매력도 잘 어울려요.",
        "match": "INTJ",
    },
    "ESTJ": {
        "ko": "윈디", "en": "Arcanine", "number": "059",
        "types": ["불꽃"],
        "features": "용맹하고 충성심이 강하며 빠르게 달릴 수 있어요.",
        "reason": "체계적으로 일을 진행하고 맡은 역할을 지키는 점이 ESTJ와 닮았어요.\n주변을 이끌고 약속을 중요하게 여기는 모습도 잘 어울려요.",
        "match": "ISTP",
    },
    "ESFJ": {
        "ko": "파치리스", "en": "Pachirisu", "number": "417",
        "types": ["전기"],
        "features": "전기를 모으고 나누는 다람쥐를 닮은 포켓몬이에요.",
        "reason": "주변 사람들과 잘 어울리고 관계를 소중히 여기는 점이 ESFJ와 닮았어요.\n작은 일에도 마음을 쓰고 함께하는 즐거움을 만드는 모습도 어울려요.",
        "match": "ISFP",
    },
    "ENFJ": {
        "ko": "가디안", "en": "Gardevoir", "number": "282",
        "types": ["에스퍼", "페어리"],
        "features": "소중한 사람을 지키려는 마음이 강한 포켓몬이에요.",
        "reason": "다른 사람의 마음을 살피고 도움을 주려는 모습이 ENFJ와 닮았어요.\n사람들에게 용기를 주고 함께 성장하려는 점도 잘 어울려요.",
        "match": "INFP",
    },
    "ENTJ": {
        "ko": "리자몽", "en": "Charizard", "number": "006",
        "types": ["불꽃", "비행"],
        "features": "강력한 불꽃을 내뿜으며 하늘을 날아다녀요.",
        "reason": "뚜렷한 목표를 세우고 적극적으로 나아가는 모습이 ENTJ와 닮았어요.\n어려운 상황에서도 주도적으로 해결책을 찾는 이미지가 잘 어울려요.",
        "match": "INTP",
    },
}

MATCH_REASON = {
    "ESFP": "활기찬 에너지와 차분한 계획성이 서로 다른 관점을 나누는 데 도움이 될 수 있어요.",
    "ENFP": "새로운 가능성을 즐기는 ENFP와 깊이 생각하는 유형은 서로의 세계를 넓혀 줄 수 있어요.",
    "ESTJ": "체계적인 실행력과 실용적인 문제 해결 능력이 서로를 보완할 수 있어요.",
    "ENFJ": "따뜻한 소통과 진솔한 감성이 만나 서로를 이해하는 데 도움이 될 수 있어요.",
    "ENTJ": "논리적인 분석과 추진력이 만나 아이디어를 계획으로 발전시키는 데 도움이 될 수 있어요.",
    "ISFJ": "적극적인 행동력과 세심한 배려가 서로 다른 강점을 살릴 수 있어요.",
    "ISTJ": "활기찬 에너지와 안정감이 만나 서로에게 새로운 경험과 균형을 줄 수 있어요.",
    "INFJ": "활발한 아이디어와 깊이 있는 시선이 만나 의미 있는 대화를 나눌 수 있어요.",
    "INTJ": "다양한 발상과 전략적인 사고가 만나 흥미로운 아이디어를 발전시킬 수 있어요.",
    "ISTP": "조직력과 실용적인 판단이 만나 문제를 효율적으로 해결할 수 있어요.",
    "ISFP": "적극적인 배려와 섬세한 감성이 만나 따뜻하고 편안한 관계를 만들 수 있어요.",
    "INFP": "다정한 소통과 진솔한 마음이 만나 서로를 깊이 이해할 수 있어요.",
}

TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# -------------------------------
# 페이지 제목
# -------------------------------
st.markdown(
    '<div style="text-align:center">'
    '<span class="hero-pill">🌼 나만의 포켓몬 찾기</span>'
    '<div class="hero-title">MBTI로<br>단짝 포켓몬 찾기!</div>'
    '<div class="hero-subtitle">나의 MBTI를 고르면 찰떡궁합 포켓몬이 나타나요.<br>'
    '두근두근, 나의 단짝을 만나 보세요! ✨</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### 🍯 나의 MBTI는?")
st.write("16가지 유형 중 하나를 선택해 보세요.")

cols = st.columns(4, gap="small")

for index, mbti in enumerate(TYPES):
    with cols[index % 4]:
        if st.button(mbti, key=f"mbti_{mbti}", use_container_width=True):
            st.session_state["selected_mbti"] = mbti
            st.session_state["just_selected"] = True

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 선택 결과
# -------------------------------
selected = st.session_state.get("selected_mbti")

if selected:
    data = POKEMON[selected]

    # 새로 선택했을 때 풍선 축하 효과
    if st.session_state.pop("just_selected", False):
        st.balloons()

    st.markdown(
        f'<div class="result-card">'
        f'<span class="result-tag">🎉 나의 MBTI · {selected}</span>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#8a6b37;margin-top:15px">'
        f'축하해요! 단짝 포켓몬을 찾았어요!</div></div>',
        unsafe_allow_html=True,
    )

    # 포켓몬 공식 사이트 이미지
    image_url = (
        "https://assets.pokemon.com/assets/cms2/img/pokedex/full/"
        + data["number"] + ".png"
    )
    st.image(image_url, width=250)

    # 이름, 타입, 특징
    st.markdown(
        f'<div style="text-align:center">'
        f'<div class="pokemon-ko">{data["ko"]}</div>'
        f'<div class="pokemon-en">{data["en"]}</div>'
        + "".join(
            f'<span class="type-chip">{pokemon_type} 타입</span>'
            for pokemon_type in data["types"]
        )
        + f'<p style="color:#806f56;font-size:1rem;line-height:1.7;margin-top:14px">'
        f'{data["features"]}</p></div>',
        unsafe_allow_html=True,
    )

    # 매칭 이유
    st.markdown(
        '<div class="info-card">'
        '<h3>💛 이 포켓몬이 어울리는 이유</h3>'
        f'<p>{data["reason"].replace(chr(10), "<br>")}</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # 궁합 유형
    match = data["match"]
    match_reason = MATCH_REASON.get(
        match,
        "서로 다른 장점을 나누며 좋은 관계를 만들어 갈 수 있어요."
    )

    st.markdown(
        '<div class="info-card">'
        '<h3>🤝 잘 맞는 MBTI 궁합</h3>'
        f'<p><strong>{match}</strong><br>{match_reason}</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("↩ 다른 MBTI 골라 보기", use_container_width=True):
        st.session_state.pop("selected_mbti", None)
        st.session_state.pop("just_selected", None)
        st.rerun()

# -------------------------------
# 하단 안내
# -------------------------------
st.markdown(
    '<div class="footer-note">'
    '포켓몬 이미지는 Pokémon 공식 사이트에서 불러옵니다. '
    '이미지를 표시하려면 인터넷 연결이 필요해요.<br>'
    'MBTI와 포켓몬의 매칭은 재미를 위한 콘텐츠이며, '
    '공식 성격 검사나 궁합 판정이 아닙니다.'
    '</div>',
    unsafe_allow_html=True,
)
