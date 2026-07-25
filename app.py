import streamlit as st

import template


st.set_page_config(
    page_title="AI Thuc Chien-P1 | Nguyen Duc Dung",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    """Add a compact visual system without changing Streamlit's functionality."""
    st.markdown(
        """
        <style>
            :root {
                --navy: #183a3b;
                --ink: #263b3d;
                --muted: #688082;
                --accent: #3d8b82;
                --accent-dark: #2d7069;
                --surface: #ffffff;
                --line: #dce8e5;
            }
            .stApp {
                background: radial-gradient(circle at 92% 0%, #e1f0eb 0, transparent 26rem),
                            linear-gradient(180deg, #f6faf8 0%, #ffffff 48%);
            }
            #MainMenu, footer { visibility: hidden; }
            .block-container { max-width: 1220px; padding-top: 2.2rem; padding-bottom: 2rem; }
            [data-testid="stSidebar"] {
                background: #183a3b;
            }
            [data-testid="stSidebar"] * { color: #f8fafc; }
            [data-testid="stSidebar"] [data-baseweb="select"] * { color: #1f2937; }
            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] textarea { color: #1f2937 !important; }
            [data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] { color: #f8fafc; }
            [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.18); }
            .hero {
                color: white;
                background: linear-gradient(118deg, #183a3b 0%, #28605e 55%, #4b9387 120%);
                border-radius: 22px;
                padding: 2rem 2.1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 18px 40px rgba(24, 58, 59, .16);
            }
            .hero h1 { font-size: 2rem; line-height: 1.2; margin: .35rem 0 .55rem; }
            .hero p { color: #dcefeb; margin: 0; font-size: 1rem; }
            .eyebrow { font-size: .76rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #b8ded7; }
            .metric-card {
                background: rgba(255,255,255,.94);
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                min-height: 100px;
                box-shadow: 0 8px 24px rgba(30, 41, 59, .06);
            }
            .metric-label { color: var(--muted); font-size: .82rem; font-weight: 600; }
            .metric-value { color: var(--navy); font-size: 1.55rem; font-weight: 750; margin-top: .3rem; }
            .empty-state {
                background: #f1f8f6;
                border: 1px dashed #aad2ca;
                border-radius: 16px;
                color: var(--muted);
                padding: 2.2rem 1.25rem;
                text-align: center;
                margin: 1rem 0;
            }
            .comparison-card {
                background: #fff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1.25rem;
                height: 100%;
                box-shadow: 0 8px 24px rgba(30, 41, 59, .06);
            }
            .comparison-card h3 { color: var(--navy); margin: 0 0 .75rem; }
            [data-testid="stChatMessage"] {
                border: 1px solid var(--line);
                border-radius: 14px;
                margin-bottom: .7rem;
                box-shadow: 0 4px 12px rgba(30,41,59,.04);
            }
            .stTabs [data-baseweb="tab-list"] { gap: .5rem; }
            .stTabs [data-baseweb="tab"] { border-radius: 10px 10px 0 0; font-weight: 600; }
            .stButton > button { border-radius: 10px; font-weight: 650; }
            .stButton > button[kind="primary"] {
                background: var(--accent);
                border-color: var(--accent);
            }
            .stButton > button[kind="primary"]:hover {
                background: var(--accent-dark);
                border-color: var(--accent-dark);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


inject_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats = {"tokens": 0, "cost": 0.0, "turns": 0}
if "comparison" not in st.session_state:
    st.session_state.comparison = None

with st.sidebar:
    st.markdown("## 🤖 AI Thuc Chien")
    st.caption("Nguyễn Đức Dũng - K4 Day01 - LLM API Exploration")
    st.divider()

    st.markdown("#### Cấu hình mô hình")
    selected_model = st.selectbox(
        "Mô hình", [template.OPENAI_MODEL, template.OPENAI_MINI_MODEL], help="Chọn mô hình cho cuộc trò chuyện."
    )
    system_prompt = st.text_area(
        "System prompt",
        value="Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn, chính xác bằng tiếng Việt.",
        height=115,
        help="Thiết lập vai trò và giọng điệu của trợ lý.",
    )

    with st.expander("🎛️ Tinh chỉnh phản hồi", expanded=True):
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
        top_k = st.slider("Top K", 1, 100, 40)
        max_tokens = st.number_input("Max tokens", 10, 4096, 256, 50)

    st.divider()
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.stats = {"tokens": 0, "cost": 0.0, "turns": 0}
        st.rerun()

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">AI COURSE BUILDER · PHẦN 1</div>
        <h1>Khám phá mô hình ngôn ngữ, trực quan hơn.</h1>
        <p>Trò chuyện, thử nghiệm tham số và đối chiếu nhanh hiệu năng giữa các mô hình.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

tab_chat, tab_compare = st.tabs(["💬 Trợ lý AI", "⚖️ So sánh mô hình"])

with tab_chat:
    stats = st.session_state.stats
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Lượt hội thoại", str(stats["turns"]))
    with col2:
        metric_card("Token đã dùng", f"{stats['tokens']:,}")
    with col3:
        metric_card("Chi phí ước tính", f"${stats['cost']:.6f}")

    st.markdown("#### Cuộc trò chuyện")
    if not st.session_state.messages:
        st.markdown(
            '<div class="empty-state">👋 Hãy bắt đầu bằng một câu hỏi ở ô nhập bên dưới.<br>'
            '<small>Bạn có thể điều chỉnh mô hình và tham số ở thanh bên trái.</small></div>',
            unsafe_allow_html=True,
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "metrics" in msg:
                st.caption(msg["metrics"])

    if user_input := st.chat_input("Nhập câu hỏi của bạn..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                try:
                    try:
                        reply, latency = template.chat_with_system_prompt(
                            system_prompt=system_prompt, user_prompt=user_input, model=selected_model,
                            temperature=temperature, max_tokens=max_tokens, top_p=top_p, top_k=top_k,
                        )
                    except TypeError:
                        reply, latency = template.chat_with_system_prompt(
                            system_prompt=system_prompt, user_prompt=user_input, model=selected_model,
                            temperature=temperature, max_tokens=max_tokens,
                        )
                    cost_info = template.estimate_cost(user_input, reply, model=selected_model)
                except Exception as exc:
                    st.error(f"Không thể gọi mô hình: {exc}")
                    reply = None
                else:
                    metrics = (
                        f"⏱️ Độ trễ: {latency:.2f}s  ·  🔢 Tokens: "
                        f"{cost_info['prompt_tokens'] + cost_info['completion_tokens']}  ·  "
                        f"💰 Chi phí: ${cost_info['total_cost']:.6f}"
                    )
                    st.write(reply)
                    st.caption(metrics)

        if reply is not None:
            st.session_state.messages.append({"role": "assistant", "content": reply, "metrics": metrics})
            st.session_state.stats["turns"] += 1
            st.session_state.stats["tokens"] += cost_info["prompt_tokens"] + cost_info["completion_tokens"]
            st.session_state.stats["cost"] += cost_info["total_cost"]

with tab_compare:
    st.markdown("#### Đặt cùng một câu hỏi cho hai mô hình")
    st.caption("Kết quả giúp bạn cân bằng giữa chất lượng phản hồi, tốc độ và chi phí.")
    compare_prompt = st.text_area(
        "Câu hỏi thử nghiệm", "Giải thích ngắn gọn khái niệm Machine Learning là gì?", height=100
    )

    if st.button("🚀 So sánh ngay", type="primary"):
        with st.spinner("Đang gọi cả hai mô hình..."):
            try:
                st.session_state.comparison = template.compare_models(compare_prompt)
            except Exception as exc:
                st.error(f"Không thể so sánh mô hình: {exc}")

    comp_res = st.session_state.comparison
    if comp_res:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown('<div class="comparison-card">', unsafe_allow_html=True)
            st.markdown("### 🟢 GPT-4o")
            st.write(comp_res["gpt4o_answer"])
            st.caption(f"⏱️ {comp_res['gpt4o_time']:.2f}s  ·  💰 ${comp_res['gpt4o_cost']:.6f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="comparison-card">', unsafe_allow_html=True)
            st.markdown("### 🔵 GPT-4o-mini")
            st.write(comp_res["mini_answer"])
            st.caption(f"⏱️ {comp_res['mini_time']:.2f}s  ·  💰 $0.000000 (rất rẻ)")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="empty-state">⚖️ Nhập câu hỏi rồi chọn <b>So sánh ngay</b> để xem kết quả song song.</div>',
            unsafe_allow_html=True,
        )
