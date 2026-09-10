import base64
import os
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(
    page_title="Trade-MBTI | 무역 직무 적합성 진단 테스트",
    page_icon="🚢",
    layout="centered"
)

# 로컬 폰트 (에이투지체-4Regular.otf) base64 로딩 함수
def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as font_file:
            return base64.b64encode(font_file.read()).decode("utf-8")
    return None

font_b64 = get_font_base64("에이투지체-4Regular.otf")
font_face_css = f"""
@font-face {{
    font-family: 'A2Z';
    src: url(data:font/otf;charset=utf-8;base64,{font_b64}) format('opentype');
    font-weight: normal;
    font-style: normal;
}}
""" if font_b64 else ""

# 2. 반응형 & 에이투지체 CSS 적용
st.markdown(f"""
<style>
    {font_face_css}
    
    /* 기본 폰트 적용 */
    html, body, [class*="css"], .stMarkdown, .stButton, button {{
        font-family: 'A2Z', 'Pretendard', sans-serif !important;
    }}
    
    /* 반응형 메인 컨테이너 */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 680px;
    }}

    /* 반응형 버튼 UI */
    div.stButton > button {{
        width: 100%;
        border-radius: 12px;
        padding: 14px 16px;
        font-size: clamp(13px, 2.5vw, 15px);
        font-weight: 500;
        text-align: left;
        line-height: 1.5;
        border: 1.5px solid #E2E8F0;
        background-color: #FFFFFF;
        color: #1E293B;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        white-space: pre-wrap !important;
        word-break: keep-all;
    }}
    div.stButton > button:hover {{
        border-color: #3B82F6;
        background-color: #EFF6FF;
        color: #1D4ED8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }}

    /* 반응형 타이틀 */
    .gradient-title {{
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: clamp(1.8rem, 5vw, 2.4rem);
        letter-spacing: -0.5px;
    }}
    
    .result-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background-color: #DBEAFE;
        color: #1E40AF;
        font-weight: 700;
        font-size: clamp(11px, 2vw, 13px);
        margin-bottom: 8px;
    }}

    /* 모바일 최적화 여백 */
    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 1rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# 20개 문항 데이터[cite: 1]
QUESTIONS = [
    {"stage": "STAGE 1. 시장 조사 & 전략 수립", "q": "올해 새로운 해외 시장 진출 전략을 세워야 한다. 내가 먼저 하고 싶은 업무는?", "a": ("일단 부딪혀보자! 잠재 바이어 리스트를 확보해 콜드메일과 전화로 반응을 살핀다.", "S"), "b": ("기반부터 탄탄히! 해당 국가의 수입 규제, 관세율(FTA), 통관 요건부터 꼼꼼히 정리한다.", "O")},
    {"stage": "STAGE 1. 시장 조사 & 전략 수립", "q": "신규 진출 국가를 선정할 때 나의 기준은?", "a": ("진입 장벽과 규제가 다소 까다롭더라도, 경쟁자가 적고 마진율이 높은 신흥 블루오션 시장.", "A"), "b": ("경쟁은 치열하지만 대금 결제 시스템이 투명하고 법적 분쟁 리스크가 낮은 안정적인 시장.", "C")},
    {"stage": "STAGE 1. 시장 조사 & 전략 수립", "q": "연간 물류 예산 및 수출입 계획을 세울 때 나의 접근 방식은?", "a": ("과거 3개년 운임 추이, 환율 시나리오, FTA 절감액을 종합 분석한 엑셀 모델링을 만든다.", "P"), "b": ("포워더 및 선사 담당자들과 직접 미팅을 잡고 현장 스페이스 상황과 실시간 운임을 파악한다.", "L")},
    {"stage": "STAGE 1. 시장 조사 & 전략 수립", "q": "해외 시장 트렌드 보고서를 작성할 때 내가 집중하는 파트는?", "a": ("현지 소비자의 니즈, 경쟁사 영업 방식, 바이어를 사로잡을 셀링 포인트.", "N"), "b": ("현지 인증 기준, 성분 규제 가이드라인, 필수 수입 서류 체크리스트.", "D")},
    
    {"stage": "STAGE 2. 바이어 발굴 & 전시회", "q": "독일 프랑크푸르트 국제 박람회 부스에 참가했다. 부스 운영 중 나의 주된 모습은?", "a": ("지나가는 모든 관람객에게 다가가 카탈로그를 건네며 명함을 쓸어 담고 적극적으로 설명한다.", "S"), "b": ("부스를 찾은 바이어의 질문에 정확한 제품 규격, 포장 사양(CBM), 납기 가능일을 오차 없이 안내한다.", "O")},
    {"stage": "STAGE 2. 바이어 발굴 & 전시회", "q": "전시회에서 유망해 보이지만 검증되지 않은 바이어가 파격적인 조건으로 샘플 오더를 요구한다면?", "a": ("기회를 놓칠 수 없다! 빠른 시장 선점을 위해 적극적으로 샘플을 보내고 관계를 튼다.", "A"), "b": ("사업자등록증, 신용도 조사(K-SURE 등) 및 기업 배경을 먼저 검증한 후 결정한다.", "C")},
    {"stage": "STAGE 2. 바이어 발굴 & 전시회", "q": "현장에서 바이어가 긴급 미팅을 요청했으나 부스 일정표가 꽉 차 있다면?", "a": ("정해진 타임테이블을 변경하기보다는, 사전 예약된 바이어와의 약속을 원칙대로 지킨다.", "P"), "b": ("점심시간을 쪼개거나 커피 브레이크를 활용해 즉석에서 15분 번개 미팅을 만들어낸다.", "L")},
    {"stage": "STAGE 2. 바이어 발굴 & 전시회", "q": "전시회 종료 후 귀국 비행기에 오르기 전 나의 행동은?", "a": ("만난 핵심 바이어들에게 감사의 인사와 미팅 대화 요약을 담아 즉시 팔로업 메일을 보낸다.", "N"), "b": ("수집한 수십 장의 명함을 등급별로 분류하고, 상담 일지를 데이터시트에 누락 없이 입력한다.", "D")},

    {"stage": "STAGE 3. 가격 협상 & 계약 체결", "q": "바이어가 경쟁사보다 단가가 7% 비싸다며 깎아주지 않으면 발주하지 않겠다고 압박할 때?", "a": ("대신 MOQ(최소주문수량)를 늘려주시면 맞춰보겠습니다! 역제안을 던져 딜을 성사시킨다.", "S"), "b": ("원부자재 가격, 해상 운임, 환율 변동 폭을 계산해 우리가 감당 가능한 최저 마진 한계선을 지킨다.", "O")},
    {"stage": "STAGE 3. 가격 협상 & 계약 체결", "q": "바이어가 결제 조건을 우리에게 다소 불리한 외상(D/A, Open Account)으로 요구할 때?", "a": ("초기 신뢰 구축을 위해 이번 첫 발주만 과감히 수용하고 수주를 확정 짓는다.", "A"), "b": ("대금 회수 리스크는 타협 불가! 100% 사전 송금(T/T)이나 취소불능 신용장(L/C)을 고수한다.", "C")},
    {"stage": "STAGE 3. 가격 협상 & 계약 체결", "q": "본 계약서 작성 시 내가 가장 심혈을 기울이는 부분은?", "a": ("독점권 범위, 클레임 발생 시 상호 협의 조건, 양사 간 파트너십 유지 조항.", "N"), "b": ("인코텀즈(Incoterms) 조건 명시, 불가항력 조항, 준거법 및 중재지 명시 등 법적 문구 완결성.", "D")},
    {"stage": "STAGE 3. 가격 협상 & 계약 체결", "q": "환율 변동성이 극심한 시기, 가격 책정 전략은?", "a": ("향후 6개월간 환율 변동 시나리오를 바탕으로 통화 헤징 및 고정 환율 마진 버퍼를 설계한다.", "P"), "b": ("단기 유효기간(2주) 견적서를 발행하고, 발주 시점마다 실시간 외환 시장을 반영해 유연하게 책정한다.", "L")},

    {"stage": "STAGE 4. 생산·선적 & 통관·물류", "q": "공장 출고가 지연되어 예정된 선박(Vessel)을 놓칠 위기에 처했을 때?", "a": ("포워더에게 전화해 인근 항만 대체 선박을 수배하고 필요시 항공 특송(Air) 분할 선적을 실행한다.", "L"), "b": ("바이어에게 공정 지연 사유서를 명확히 전달하고, 전체 공급망 스케줄을 재조정해 2차 오더 납기를 맞춘다.", "P")},
    {"stage": "STAGE 4. 생산·선적 & 통관·물류", "q": "목적국 세관에서 HS Code 해석 차이로 화물이 보류(Hold)되었다는 연락을 받았다면?", "a": ("현지 관세사 및 대리인과 협상하여 우선 통관을 진행시키고 사후 정정하는 방안을 모색한다.", "A"), "b": ("원산지증명서(C/O), 성분표, 제조공정도 등 공인 서류를 보강하여 세관 기준에 완벽히 부합하도록 소명한다.", "C")},
    {"stage": "STAGE 4. 생산·선적 & 통관·물류", "q": "선적 서류(B/L, Invoice, Packing List)를 작성할 때 나의 작업 방식은?", "a": ("세부 숫자나 철자 하나라도 L/C 조건과 다르면 하자(Discrepancy)가 나므로 글자 하나하나 대조·검증한다.", "D"), "b": ("포워더 및 선사와 지속적으로 소통하며 B/L 발행 일정과 특약 문구가 바이어 요청대로 반영되었는지 확인한다.", "N")},
    {"stage": "STAGE 4. 생산·선적 & 통관·물류", "q": "물류 창고 현장에서 파레트 포장 규격이 약간 달라 컨테이너 적재 공간이 남는 상황이라면?", "a": ("남는 공간(Dead Space)에 바이어에게 홍보할 수 있는 판촉물이나 서브 제품을 채워 넣을 방법을 찾는다.", "S"), "b": ("적재 중량 및 CBM 계산서를 수정하고 수화물 파손 방지를 위한 에어백 완충재 보강을 지시한다.", "O")},

    {"stage": "STAGE 5. 정산 & 클레임 사후관리", "q": "도착한 제품 일부에 스크래치가 발생했다며 바이어가 거센 클레임(Claim)을 제기할 때?", "a": ("바이어의 불만을 경청하며 감정을 달래고, 다음 오더 할인 쿠폰이나 무상 수량을 제공하는 선에서 합의한다.", "N"), "b": ("선적 전 검사 보고서(PSI), 보험 증권, 사진 증빙을 토대로 책임 소재(제조 vs 운송)를 명확히 규명한다.", "D")},
    {"stage": "STAGE 5. 정산 & 클레임 사후관리", "q": "프로젝트 수출 건이 무사히 납품 완료되었다. 이후 내가 가장 중요하게 챙기는 것은?", "a": ("바이어에게 만족도 피드백을 요청하며 다음 시즌 신제품을 소개하고 재발주(Re-order)를 유도한다.", "S"), "b": ("수출 실적 증명서 발급, 관세 환급 신청, 입금 확인 및 외환 차손익 정산 보고서를 마감한다.", "O")},
    {"stage": "STAGE 5. 정산 & 클레임 사후관리", "q": "이번 수출 건에서 예상치 못한 추가 보관료(Demurrage)가 발생해 수익률이 떨어졌다면?", "a": ("현장에서 언제든 생길 수 있는 변수로 보고, 다음 운송 시 더 빠른 내륙 운송사를 섭외해 만회한다.", "L"), "b": ("물류 단계별 체류 시간을 전수 조사하여 보관료 발생 원인을 분석하고 '표준 물류 가이드'를 개정한다.", "P")},
    {"stage": "STAGE 5. 정산 & 클레임 사후관리", "q": "무역 프로젝트 전 과정을 마치고 내가 가장 큰 보람을 느끼는 순간은?", "a": ("수많은 변수와 위험을 뚫고 불가능해 보였던 대형 계약을 성공적으로 완수해 냈을 때.", "A"), "b": ("단 한 건의 법적 분쟁, 관세 벌금, 대금 미수금 없이 모든 서류와 정산이 완벽하게 끝났을 때.", "C")}
]

# 16가지 페르소나 데이터[cite: 1]
PERSONAS = {
    "SALN": {
        "title": "글로벌 프런티어 (해외영업 개척가)",
        "summary": "과감한 결단력과 뛰어난 친화력, 현장 순발력으로 신흥 시장을 개척하고 바이어를 설득해내는 행동파 무역 전문가입니다.",
        "strengths": ["탁월한 네고 감각과 역제안 능력", "물류/선적 돌발 상황 시 현장 중심 즉각 해결", "높은 마진 확보를 위한 과감한 신시장 진출"],
        "cautions": ["신용장(L/C) 세부 조항 및 계약서 오탈자 검토 습관 필요", "대금 미회수 방지를 위한 무역보험 확인 필수"],
        "jobs": "소비재/원자재 해외영업, 신시장 개척(BD), 종합상사 영업",
        "certs": "국제무역사, 무역영어 1급, OPIc AL",
        "best": "OCPD (퍼펙트 디펜더) - 서류와 리스크를 완벽 방어해주는 파트너",
        "worst": "OCPN (원칙주의 플래너) - 모든 검증이 끝날 때까지 출발을 막는 파트너"
    },
    "SALD": {
        "title": "테크니컬 세일즈 (기술기반 영업가)",
        "summary": "정확한 제품 스펙과 계약 조항을 완벽히 숙지하고 현장 대응력까지 갖춘 실무형 기술영업 전문가입니다.",
        "strengths": ["스펙 기반의 탄탄한 제안력", "현장 바이어 기술 질의 즉각 대응", "하자 없는 계약서 작성 능력"],
        "cautions": ["지나치게 보수적인 조건 설정으로 인한 협상 장기화 주의"],
        "jobs": "기계/플랜트/IT 해외영업, 기술영업팀",
        "certs": "국제무역사, 원산지관리사",
        "best": "OAPN (SCM 기획가)", "worst": "SCLN (관계형 해결사)"
    },
    "SAPN": {
        "title": "무역 전략가 (글로벌 소싱/기획)",
        "summary": "글로벌 트렌드를 읽고 공급망을 기획하며 공격적인 포지셔닝으로 시장을 장악하는 브레인형 무역가입니다.",
        "strengths": ["글로벌 소싱처 발굴 및 마진 구조 최적화", "전략적 바이어 관계 형성"],
        "cautions": ["현장 돌발 변수에 대한 유연한 대처력 보완"],
        "jobs": "해외 상품기획(MD), 글로벌 전략기획팀",
        "certs": "국제무역사, 유통관리사",
        "best": "OCLD (수출입 통관스페셜리스트)", "worst": "OALN (현장 해결사)"
    },
    "SAPD": {
        "title": "글로벌 마케터 (데이터기반 세일즈)",
        "summary": "철저한 시장 데이터와 관세 규정 분석을 기반으로 글로벌 타깃 시장을 정밀 타격하는 마케팅 세일즈형입니다.",
        "strengths": ["데이터 기반 시장 분석력", "오차 없는 수출입 채널 기획"],
        "cautions": ["지나친 분석으로 인한 초기 시장 진입 지연"],
        "jobs": "글로벌 마케팅, 수출입 전략기획",
        "certs": "무역영어 1급, 데이터분석 준전문가(ADsP)",
        "best": "OCLN (포워딩 트러블슈터)", "worst": "SALN (글로벌 프런티어)"
    },
    "SCLN": {
        "title": "관계형 해결사 (장기 파트너십 세일즈)",
        "summary": "규정과 원칙을 지키면서도 뛰어난 공감 능력과 현장 대응력으로 바이어와 끈끈한 신뢰를 맺는 영업가입니다.",
        "strengths": ["장기 바이어 락인(Lock-in) 능력", "클레임 발생 시 원만한 조율"],
        "cautions": ["새로운 블루오션 시장 진출에 대한 소극성"],
        "jobs": "고객관리(AM), OEM/ODM 해외영업",
        "certs": "무역영어 1급, 비즈니스 외국어",
        "best": "OAPD (공급망 데이터분석가)", "worst": "SALD (테크니컬 세일즈)"
    },
    "SCLD": {
        "title": "계약 협상가 (법무·인증 전문 영업)",
        "summary": "완벽한 계약서와 리스크 헷징을 최우선으로 두며 차분하게 계약을 성사시키는 안정형 영업 전문가입니다.",
        "strengths": ["법적 분쟁 제로화", "원칙에 기반한 단가 및 결제 조건 방어"],
        "cautions": ["유연한 역제안 부재로 계약 성사율 저하 가능성"],
        "jobs": "방산/의약품 해외영업, 라이선스 계약팀",
        "certs": "국제무역사 1급, 무역영어 1급",
        "best": "OALN (현장 해결사)", "worst": "SAPN (무역 전략가)"
    },
    "SCPN": {
        "title": "글로벌 파트너십 (정부/공공 프로젝트)",
        "summary": "장기적인 규정 준수와 체계적인 네트워크를 바탕으로 대형 공공 및 인프라 무역 사업을 이끄는 플래너입니다.",
        "strengths": ["정부 입찰(Tender) 및 대형 프로젝트 조율", "체계적 파트너십 관리"],
        "cautions": ["단기적인 시장 기회 포착 속도 다소 느림"],
        "jobs": "해외 공공조달, 대형 인프라 수출팀",
        "certs": "국제무역사, PMP",
        "best": "OALD (물류 오퍼레이터)", "worst": "SALN (글로벌 프런티어)"
    },
    "SCPD": {
        "title": "리스크 관리형 영업 (방어형 세일즈)",
        "summary": "모든 수출입 규제와 손익 시나리오를 검증한 후에만 딜을 진행하는 완벽주의 영업 전문가입니다.",
        "strengths": ["무역 사기 및 미수금 발생률 0%", "완벽한 FTA 및 관세 혜택 계산"],
        "cautions": ["공격적인 매출 확대 한계"],
        "jobs": "화학/원자재 무역, 종합상사 관리영업",
        "certs": "원산지관리사, 국제무역사",
        "best": "SALN (글로벌 프런티어)", "worst": "OALN (현장 해결사)"
    },
    "OALN": {
        "title": "현장 해결사 (포워딩 긴급대응팀)",
        "summary": "물류와 통관 현장에서 벌어지는 모든 돌발 상황을 빠른 결단과 인맥으로 처리하는 베테랑 오퍼레이터입니다.",
        "strengths": ["항만 파업/선적 취소 시 초고속 대체 루트 확보", "현장 협상력"],
        "cautions": ["규정 서류 작업에 대한 꼼꼼함 보강 필요"],
        "jobs": "복합운송 포워딩 오퍼레이션, 항공화물 긴급수송",
        "certs": "물류관리사, 무역영어",
        "best": "SCLD (계약 협상가)", "worst": "SAPN (무역 전략가)"
    },
    "OALD": {
        "title": "물류 오퍼레이터 (실행형 물류관리)",
        "summary": "적재 공간 계산, 선적 서류 발행, 빠른 현장 대응을 오차 없이 완수하는 물류의 허브입니다.",
        "strengths": ["적재 효율(CBM) 극대화", "신속 정확한 B/L 서류 작성"],
        "cautions": ["전체 공급망을 조망하는 전략적 시야 보강"],
        "jobs": "포워딩 선적 서류 파트, 수출입 창고 운영",
        "certs": "물류관리사, 국제무역사",
        "best": "SCPN (글로벌 파트너십)", "worst": "SAPN (무역 전략가)"
    },
    "OAPN": {
        "title": "SCM 기획가 (공급망 최적화 전문가)",
        "summary": "비용과 리스크를 감수하더라도 가장 효율적인 글로벌 공급망 루트를 새롭게 설계하는 기획형 관리자입니다.",
        "strengths": ["물류 경로 다변화 및 리드타임 단축", "공급망 병목 해결"],
        "cautions": ["기존 계약 관계자와의 마찰 조율 필요"],
        "jobs": "글로벌 SCM 기획팀, 해외물류 기획",
        "certs": "CPIM, 물류관리사",
        "best": "SALD (테크니컬 세일즈)", "worst": "SCLN (관계형 해결사)"
    },
    "OAPD": {
        "title": "공급망 데이터분석가 (물류 데이터사이언스)",
        "summary": "글로벌 물류 데이터와 운임 추이를 분석하여 최적의 선적 시점과 루트를 찾아내는 데이터 기반 관리자입니다.",
        "strengths": ["물류비 시뮬레이션 모델링", "통관 및 입출고 데이터 정확성"],
        "cautions": ["현장 실무자의 감정적 피로도 고려"],
        "jobs": "물류 빅데이터 분석, SCM 운영분석",
        "certs": "ADsP, 물류관리사",
        "best": "SCLN (관계형 해결사)", "worst": "SALN (글로벌 프런티어)"
    },
    "OCLN": {
        "title": "포워딩 트러블슈터 (현장형 물류스페셜리스트)",
        "summary": "관세법과 규정을 철저히 지키면서도 현장 파트너들과 소통하여 문제를 부드럽게 해결하는 조율사입니다.",
        "strengths": ["세관 및 선사와의 원활한 소통", "안전한 화물 인도 프로세스 구축"],
        "cautions": ["변수 발생 시 과감한 결단력 강화"],
        "jobs": "포워딩 영업/CS, 수출입 통관 관리",
        "certs": "무역영어 1급, 보세사",
        "best": "SAPD (글로벌 마케터)", "worst": "SALN (글로벌 프런티어)"
    },
    "OCLD": {
        "title": "수출입 통관스페셜리스트 (원산지/관세 전문가)",
        "summary": "복잡한 HS코드와 원산지 판정, 세관 서류를 완벽하게 방어하는 무역 컴플라이언스의 스페셜리스트입니다.",
        "strengths": ["HS코드 분류 및 FTA 특혜관세 적용", "통관 보류 및 과태료 리스크 제로화"],
        "cautions": ["지나치게 경직된 업무 방식으로 인한 영업 부서와의 갈등"],
        "jobs": "사내 관세팀, 통관법인, 원산지 심사팀",
        "certs": "원산지관리사, 보세사, 관세사",
        "best": "SAPN (무역 전략가)", "worst": "SALN (글로벌 프런티어)"
    },
    "OCPN": {
        "title": "원칙주의 플래너 (무역 프로세스 총괄)",
        "summary": "수출입 표준 프로세스(SOP)를 정립하고 규제와 결제 안전을 시스템으로 통제하는 조직의 기둥입니다.",
        "strengths": ["수출입 통제 시스템 구축", "외환 거래 규정 및 대금 정산 완벽 마감"],
        "cautions": ["신시장 진출 시 유연성 결여 주의"],
        "jobs": "무역 지원 총괄, 외환정산팀, 무역 감사",
        "certs": "국제무역사 1급, 무역영어 1급",
        "best": "SALD (테크니컬 세일즈)", "worst": "SALN (글로벌 프런티어)"
    },
    "OCPD": {
        "title": "퍼펙트 디펜더 (무역외환/통관 최종수문장)",
        "summary": "단 1자의 서류 오타도 허용하지 않으며, 무역 결제 및 외환 리스크를 완벽하게 통제하는 최고의 백오피스 전문가입니다.",
        "strengths": ["신용장(L/C) Discrepancy 제로", "외환 차손익 방어 및 완벽한 수출입 서류 정산"],
        "cautions": ["돌발 변수 발생 시 대안 수립 속도 보완"],
        "jobs": "무역 결제/정산팀, 은행 외환계, 관세사무소",
        "certs": "CDCS(국제신용장전문가), 외환전문역, 국제무역사",
        "best": "SALN (글로벌 프런티어) - 최고의 영업 파트너",
        "worst": "OALN (현장 해결사) - 즉흥적인 파트너"
    }
}

# 세션 상태 관리
if "step" not in st.session_state:
    st.session_state.step = "start"
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"S": 0, "O": 0, "A": 0, "C": 0, "L": 0, "P": 0, "N": 0, "D": 0}

def handle_choice(type_code):
    st.session_state.scores[type_code] += 1
    if st.session_state.current_q + 1 < len(QUESTIONS):
        st.session_state.current_q += 1
    else:
        st.session_state.step = "result"
    st.rerun()

def restart_test():
    st.session_state.step = "start"
    st.session_state.current_q = 0
    st.session_state.scores = {"S": 0, "O": 0, "A": 0, "C": 0, "L": 0, "P": 0, "N": 0, "D": 0}
    st.rerun()

# -------------------------------------------------------------
# 1. 시작 화면
# -------------------------------------------------------------
if st.session_state.step == "start":
    st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.markdown('<span style="font-size: clamp(40px, 8vw, 56px);">🌍</span>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-title">Trade-MBTI</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; font-size: clamp(14px, 3vw, 16px); margin-top: 6px;">무역 실무 기반 직무 적합성 진단 테스트</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**💬 \"지구 반대편에서도 계약서를 들고 오는 당신, 어떤 무역 전문가인가요?\"**")
        st.caption("시장 조사부터 바이어 네고, 선적, 통관, 정산까지 무역 실무 라이프사이클에서 나의 본능적인 의사결정 방식을 진단합니다.")
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric(label="총 문항 수", value="20문항")
        c2.metric(label="예상 소요 시간", value="약 3분")

    st.write("")
    if st.button("🚀 나의 무역 페르소나 확인하기", use_container_width=True, type="primary"):
        st.session_state.step = "quiz"
        st.rerun()

# -------------------------------------------------------------
# 2. 퀴즈 진행 화면
# -------------------------------------------------------------
elif st.session_state.step == "quiz":
    q_idx = st.session_state.current_q
    q_data = QUESTIONS[q_idx]
    progress = (q_idx + 1) / len(QUESTIONS)
    
    st.markdown(f'<span class="result-badge">{q_data["stage"]}</span>', unsafe_allow_html=True)
    st.progress(progress, text=f"진행 상황 ({q_idx + 1} / {len(QUESTIONS)})")
    st.write("")
    
    st.markdown(f"<h3 style='font-size: clamp(16px, 3.5vw, 19px); line-height: 1.5; color: #0F172A; font-weight: 700; margin-bottom: 20px;'>Q{q_idx + 1}. {q_data['q']}</h3>", unsafe_allow_html=True)

    if st.button(f"A.  {q_data['a'][0]}", key=f"q_{q_idx}_a", use_container_width=True):
        handle_choice(q_data['a'][1])
        
    st.write("")
    if st.button(f"B.  {q_data['b'][0]}", key=f"q_{q_idx}_b", use_container_width=True):
        handle_choice(q_data['b'][1])

# -------------------------------------------------------------
# 3. 결과 화면
# -------------------------------------------------------------
# -------------------------------------------------------------
# 3. 결과 화면
# -------------------------------------------------------------
elif st.session_state.step == "result":
    # 💥 순수 CSS 기반 무조건 터지는 컨페티 애니메이션
    st.markdown("""
    <style>
    @keyframes confetti-fall {
        0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    .confetti-box {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 999999;
        overflow: hidden;
    }
    .c-piece {
        position: absolute;
        width: 10px;
        height: 16px;
        top: -20px;
        opacity: 0.9;
        animation: confetti-fall 3.5s ease-out forwards;
    }
    </style>
    <div class="confetti-box">
        <div class="c-piece" style="left:5%; background:#3B82F6; animation-delay:0s; transform:rotate(15deg);"></div>
        <div class="c-piece" style="left:12%; background:#EF4444; animation-delay:0.2s; transform:rotate(45deg);"></div>
        <div class="c-piece" style="left:20%; background:#10B981; animation-delay:0.1s; transform:rotate(110deg);"></div>
        <div class="c-piece" style="left:28%; background:#F59E0B; animation-delay:0.4s; transform:rotate(20deg);"></div>
        <div class="c-piece" style="left:35%; background:#8B5CF6; animation-delay:0.15s; transform:rotate(80deg);"></div>
        <div class="c-piece" style="left:42%; background:#EC4899; animation-delay:0.3s; transform:rotate(160deg);"></div>
        <div class="c-piece" style="left:50%; background:#3B82F6; animation-delay:0.05s; transform:rotate(30deg);"></div>
        <div class="c-piece" style="left:58%; background:#10B981; animation-delay:0.25s; transform:rotate(95deg);"></div>
        <div class="c-piece" style="left:65%; background:#F59E0B; animation-delay:0.35s; transform:rotate(140deg);"></div>
        <div class="c-piece" style="left:72%; background:#EF4444; animation-delay:0.1s; transform:rotate(200deg);"></div>
        <div class="c-piece" style="left:80%; background:#8B5CF6; animation-delay:0.45s; transform:rotate(60deg);"></div>
        <div class="c-piece" style="left:88%; background:#3B82F6; animation-delay:0.2s; transform:rotate(130deg);"></div>
        <div class="c-piece" style="left:95%; background:#EC4899; animation-delay:0.3s; transform:rotate(75deg);"></div>
        <!-- 2차 파티클 -->
        <div class="c-piece" style="left:8%; background:#F59E0B; animation-delay:0.6s; width:8px; height:12px;"></div>
        <div class="c-piece" style="left:22%; background:#8B5CF6; animation-delay:0.7s; width:12px; height:8px;"></div>
        <div class="c-piece" style="left:38%; background:#EF4444; animation-delay:0.55s; width:10px; height:14px;"></div>
        <div class="c-piece" style="left:55%; background:#10B981; animation-delay:0.8s; width:8px; height:12px;"></div>
        <div class="c-piece" style="left:68%; background:#3B82F6; animation-delay:0.65s; width:12px; height:10px;"></div>
        <div class="c-piece" style="left:85%; background:#EC4899; animation-delay:0.75s; width:10px; height:14px;"></div>
    </div>
    """, unsafe_allow_html=True)
      
    sc = st.session_state.scores
    dim1 = "S" if sc["S"] >= 3 else "O"
    dim2 = "A" if sc["A"] >= 3 else "C"
    dim3 = "L" if sc["L"] >= 3 else "P"
    dim4 = "N" if sc["N"] >= 3 else "D"
    result_code = f"{dim1}{dim2}{dim3}{dim4}"
    
    persona = PERSONAS.get(result_code, PERSONAS["SALN"])
    
    st.markdown('<div style="text-align: center; margin-bottom: 16px;">', unsafe_allow_html=True)
    st.markdown('<span class="result-badge">YOUR TRADE PERSONA</span>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-size: clamp(34px, 7vw, 44px); font-weight: 900; color: #1E3A8A; margin: 2px 0;">{result_code}</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="font-size: clamp(17px, 4vw, 20px); font-weight: 700; color: #2563EB;">{persona["title"]}</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info(f"💡 {persona['summary']}")
    
    with st.expander("📊 나의 4대 지표 세부 성향 분석", expanded=True):
        st.write(f"**역할 성향:** 해외영업(S) {sc['S']*20}%  vs  무역관리(O) {sc['O']*20}%")
        st.progress(sc['S'] / 5.0)
        
        st.write(f"**의사결정:** 시장공격(A) {sc['A']*20}%  vs  리스크방어(C) {sc['C']*20}%")
        st.progress(sc['A'] / 5.0)
        
        st.write(f"**운영방식:** 현장실행(L) {sc['L']*20}%  vs  전략기획(P) {sc['P']*20}%")
        st.progress(sc['L'] / 5.0)
        
        st.write(f"**소통방식:** 협상조율(N) {sc['N']*20}%  vs  정확기록(D) {sc['D']*20}%")
        st.progress(sc['N'] / 5.0)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### ⚡ 핵심 강점")
            for item in persona["strengths"]:
                st.markdown(f"- {item}")
    with col2:
        with st.container(border=True):
            st.markdown("#### ⚠️ 보완할 점")
            for item in persona["cautions"]:
                st.markdown(f"- {item}")
                
    with st.container(border=True):
        st.markdown(f"💼 **추천 직무:** {persona['jobs']}")
        st.markdown(f"📜 **추천 자격증:** {persona['certs']}")
        st.divider()
        st.markdown(f"💚 **환상의 파트너:** {persona['best']}")
        st.markdown(f"💔 **주의할 파트너:** {persona['worst']}")

    st.write("")
    if st.button("🔄 테스트 다시하기", use_container_width=True, type="secondary"):
        restart_test()