import time
import streamlit as st
import template  # Import trực tiếp từ file template.py của bạn

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="AICB-P1 | LLM API Playground",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AICB-P1: LLM API Dashboard & Assistant")

# 2. Thanh cấu hình Sidebar (Kéo đầy đủ các tham số cấu hình)
with st.sidebar:
    st.header("⚙️ Cấu Hình Mô Hình")
    
    # Chọn Model
    selected_model = st.selectbox(
        "Mô hình (Model)",
        options=[template.OPENAI_MODEL, template.OPENAI_MINI_MODEL],
        index=0,
        help="Chọn gpt-4o hoặc gpt-4o-mini"
    )
    
    # System Prompt / Persona
    system_prompt = st.text_area(
        "System Prompt (Persona)",
        value="Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn, chính xác bằng tiếng Việt.",
        height=100,
        help="Định hình vai trò và phong cách trả lời của AI"
    )
    
    st.divider()
    st.subheader("🎛️ Tham Số Hyperparameters")
    
    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Độ ngẫu nhiên/sáng tạo (0.0 = chính xác, 2.0 = sáng tạo cao)"
    )
    
    # Top P
    top_p = st.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Nucleus sampling"
    )
    
    # Top K (Mới thêm vào)
    top_k = st.slider(
        "Top K",
        min_value=1,
        max_value=100,
        value=40,
        step=1,
        help="Giới hạn tập hợp K token có xác suất cao nhất"
    )
    
    # Max Tokens
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=10,
        max_value=4096,
        value=256,
        step=50,
        help="Số token tối đa sinh ra trong phản hồi"
    )
    
    st.divider()
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.stats = {"tokens": 0, "cost": 0.0, "turns": 0}
        st.rerun()

# 3. Tạo các Tab tính năng
tab1, tab2 = st.tabs(["💬 Chatbot Trợ Lý", "⚖️ So Sánh Models"])

# ---------------------------------------------------------------------------
# TAB 1: CHATBOT CÓ CẤU HÌNH & THỐNG KÊ
# ---------------------------------------------------------------------------
with tab1:
    # Khởi tạo session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "stats" not in st.session_state:
        st.session_state.stats = {"tokens": 0, "cost": 0.0, "turns": 0}

    # Hiển thị các ô chỉ số Thống kê phía trên
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng lượt chat", st.session_state.stats["turns"])
    col2.metric("Tổng Tokens đã dùng", st.session_state.stats["tokens"])
    col3.metric("Tổng Chi Phí Ước Tính", f"${st.session_state.stats['cost']:.6f}")

    st.divider()

    # Hiển thị lịch sử hội thoại
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "metrics" in msg:
                st.caption(msg["metrics"])

    # Ô nhập tin nhắn người dùng
    if user_input := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
        # Hiển thị tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Xử lý và gọi API
        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                start_time = time.time()
                
                # Gọi hàm chat_with_system_prompt từ template.py với cấu hình từ sidebar
                # Lưu ý: OpenAI API tiêu chuẩn dùng top_p, tham số top_k có thể truyền thêm vào nếu provider/wrapper hỗ trợ
                try:
                    reply, latency = template.chat_with_system_prompt(
                        system_prompt=system_prompt,
                        user_prompt=user_input,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        top_k=top_k
                    )
                except TypeError:
                    # Fallback nếu hàm chat_with_system_prompt trong template.py chưa khai báo nhận tham số top_k/top_p
                    reply, latency = template.chat_with_system_prompt(
                        system_prompt=system_prompt,
                        user_prompt=user_input,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                
                # Tính chi phí dựa trên hàm estimate_cost trong template.py
                cost_info = template.estimate_cost(user_input, reply, model=selected_model)
                
                # Hiển thị kết quả
                st.write(reply)
                
                # Chuỗi thông tin thống kê cho lượt chat này
                metrics_str = (
                    f"⏱️ **Độ trễ:** {latency:.2f}s | "
                    f"🔢 **Tokens:** {cost_info['prompt_tokens'] + cost_info['completion_tokens']} | "
                    f"💰 **Chi phí:** ${cost_info['total_cost']:.6f}"
                )
                st.caption(metrics_str)

        # Cập nhật lịch sử và thống kê tổng
        st.session_state.messages.append({
            "role": "assistant", 
            "content": reply, 
            "metrics": metrics_str
        })
        
        st.session_state.stats["turns"] += 1
        st.session_state.stats["tokens"] += (cost_info['prompt_tokens'] + cost_info['completion_tokens'])
        st.session_state.stats["cost"] += cost_info['total_cost']

# ---------------------------------------------------------------------------
# TAB 2: SO SÁNH TRỰC TIẾP GPT-4O VÀ GPT-4O-MINI
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("So sánh GPT-4o và GPT-4o-mini")
    compare_prompt = st.text_input("Nhập câu hỏi để thử nghiệm so sánh:", "Giải thích ngắn gọn khái niệm Machine Learning là gì?")
    
    if st.button("🚀 So sánh ngay", type="primary"):
        with st.spinner("Đang gọi cả 2 model..."):
            # Gọi hàm compare_models từ template.py
            comp_res = template.compare_models(compare_prompt)
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("### 🟢 GPT-4o")
                st.info(comp_res["gpt4o_answer"])
                st.write(f"⏱️ **Thời gian:** {comp_res['gpt4o_time']:.2f}s")
                st.write(f"💰 **Chi phí ước tính:** ${comp_res['gpt4o_cost']:.6f}")
                
            with c2:
                st.markdown("### 🔵 GPT-4o-mini")
                st.success(comp_res["mini_answer"])
                st.write(f"⏱️ **Thời gian:** {comp_res['mini_time']:.2f}s")
                st.write(f"💰 **Chi phí ước tính:** $0.000000 (Rất rẻ)")