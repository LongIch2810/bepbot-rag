import sys
import os
import streamlit as st

# Đảm bảo import được các module từ thư mục app/
sys.path.insert(0, os.path.dirname(__file__))

from workflow import Workflow


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chatbot Công Thức Nấu Ăn Việt Nam",
    page_icon="👨‍🍳",
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────── */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Ensure Streamlit Material icons render correctly, overriding the global font */
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }
    .stApp {
        background: linear-gradient(160deg, #fff7ed 0%, #fff1e6 40%, #ffe8d6 100%);
    }
    /* Override Streamlit default text color */
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
    .stMarkdown, .stMarkdown p {
        color: #2d2d2d !important;
    }

    /* ── Header hero ────────────────────────────── */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .hero-icon {
        font-size: 3.5rem;
        margin-bottom: .4rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-8px); }
    }
    .hero h1 {
        background: linear-gradient(135deg, #e63946, #f77f00, #d62828);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -.5px;
    }
    .hero p {
        color: #6b5a4e !important;
        font-size: .92rem;
        margin-top: .35rem;
    }

    /* ── Status cards ───────────────────────────── */
    .status-card {
        display: flex;
        align-items: center;
        gap: .6rem;
        padding: .75rem 1.1rem;
        border-radius: 12px;
        margin: .8rem auto;
        max-width: 520px;
        font-size: .88rem;
        font-weight: 500;
    }
    .status-loading {
        background: rgba(247, 127, 0, .12);
        border: 1px solid rgba(247, 127, 0, .35);
        color: #c56200 !important;
    }
    .status-ready {
        background: rgba(56, 176, 0, .1);
        border: 1px solid rgba(56, 176, 0, .3);
        color: #2d8a00 !important;
    }
    .status-error {
        background: rgba(230, 57, 70, .1);
        border: 1px solid rgba(230, 57, 70, .3);
        color: #c5303a !important;
    }

    /* ── Sidebar ────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3d2c2c 0%, #5c3d2e 50%, #6b4226 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label {
        color: #f5e6d3 !important;
    }
    /* Fix the sidebar toggle button */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg {
        color: #f59e0b !important;
        fill: #f59e0b !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] strong {
        color: #ffd6a5 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.15) !important;
    }
    .sidebar-badge {
        display: inline-block;
        padding: .2rem .55rem;
        border-radius: 6px;
        font-size: .75rem;
        font-weight: 600;
        background: rgba(255, 183, 77, .25);
        color: #ffd6a5;
        margin-bottom: .15rem;
    }

    /* ── Chat bubbles ───────────────────────────── */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, .65) !important;
        border: 1px solid rgba(214, 120, 63, .15);
        border-radius: 14px !important;
        backdrop-filter: blur(8px);
        margin-bottom: .5rem;
        transition: background .2s, box-shadow .2s;
        box-shadow: 0 2px 8px rgba(180, 120, 60, .06);
    }
    [data-testid="stChatMessage"]:hover {
        background: rgba(255, 255, 255, .8) !important;
        box-shadow: 0 4px 16px rgba(180, 120, 60, .1);
    }
    [data-testid="stChatMessage"] p {
        color: #2d2d2d !important;
    }

    /* ── Chat input container ──────────────────── */
    [data-testid="stChatInput"] {
        border-top: 1px solid rgba(0, 0, 0, .06);
        padding-top: .5rem;
    }
    /* Remove Streamlit's default red/primary focus ring on the wrapper div */
    [data-testid="stChatInput"] > div:first-child,
    [data-testid="stChatInput"] > div:first-child:focus-within {
        border-color: transparent !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        border: 1.5px solid #d4d4d8 !important;
        border-radius: 12px !important;
        color: #2d2d2d !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .95rem !important;
        padding: .7rem 1rem !important;
        transition: border-color .25s, box-shadow .25s;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, .12) !important;
        outline: none !important;
    }
    /* Send button */
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 5px rgba(217, 119, 6, 0.2), 0 1px 2px rgba(217, 119, 6, 0.1) !important;
    }
    [data-testid="stChatInput"] button:hover {
        background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(217, 119, 6, 0.3), 0 3px 6px rgba(217, 119, 6, 0.15) !important;
    }
    [data-testid="stChatInput"] button:active {
        transform: translateY(0) scale(0.95) !important;
        box-shadow: 0 1px 2px rgba(217, 119, 6, 0.2) !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #fff !important;
        stroke: #fff !important;
        width: 18px !important;
        height: 18px !important;
        transition: transform 0.2s ease !important;
    }
    [data-testid="stChatInput"] button:hover svg {
        transform: scale(1.1) translate(1px, -1px) !important;
    }

    /* ── Spinner text ──────────────────────────── */
    .stSpinner > div > span {
        color: #6b4226 !important;
    }

    /* ── Scrollbar ──────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(180, 120, 60, .2);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(180, 120, 60, .35); }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖👨‍🍳 Công Thức Nấu Ăn")
    st.markdown(
        '<span class="sidebar-badge">RAG Chatbot</span>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        """
        **Mô tả**  
        Chatbot hỏi đáp về **200 món ăn truyền thống Việt Nam**, 
        sử dụng kỹ thuật RAG để trả lời chính xác từ tài liệu.

        **Tech Stack**  
        - 🤖 Google Gemini 2.5 Flash  
        - 📐 Ollama Embeddings  
        - 🗄️ Qdrant Vector DB  
        - 🔗 LangChain Agent  

        **Hướng dẫn**  
        Nhập câu hỏi về công thức nấu ăn, 
        nguyên liệu, cách chế biến, mẹo nấu ăn…  
        Bot sẽ tìm kiếm và trả lời dựa trên tài liệu.
        """
    )
    st.markdown("---")
    st.markdown(
        "<p style='color:#a08b76;font-size:.78rem;text-align:center'>"
        "Powered by LangChain &amp; Gemini</p>",
        unsafe_allow_html=True,
    )


# ── Hero header ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🤖👨‍🍳</div>
        <h1>Công Thức Nấu Ăn Việt Nam</h1>
        <p>Hỏi bất kỳ điều gì về 200 món ăn truyền thống Việt Nam</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── Initialise session state ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False

if "init_error" not in st.session_state:
    st.session_state.init_error = None


# ── Load workflow & documents (runs once) ─────────────────────────────────────
if not st.session_state.system_ready and st.session_state.init_error is None:
    # Hiển thị loading indicator
    st.markdown(
        '<div class="status-card status-loading">'
        "⏳ Đang khởi tạo hệ thống và tải tài liệu… Vui lòng chờ."
        "</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Đang khởi tạo Workflow và nạp tài liệu…"):
        try:
            workflow = Workflow()
            workflow.load_and_process_documents()
            st.session_state.workflow = workflow
            st.session_state.system_ready = True
            st.rerun()
        except Exception as exc:
            st.session_state.init_error = str(exc)
            st.rerun()


# ── Show status ──────────────────────────────────────────────────────────────
if st.session_state.init_error is not None:
    st.markdown(
        f'<div class="status-card status-error">'
        f"❌ Lỗi khởi tạo: {st.session_state.init_error}"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.stop()

if not st.session_state.system_ready:
    st.stop()

# Hệ thống sẵn sàng
st.markdown(
    '<div class="status-card status-ready">'
    "✅ Hệ thống đã sẵn sàng — hãy đặt câu hỏi bên dưới!"
    "</div>",
    unsafe_allow_html=True,
)


# ── Render chat history ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "👨‍🍳"):
        st.markdown(msg["content"])


# ── Chat input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Hỏi về công thức nấu ăn Việt Nam…"):
    # Hiển thị & lưu câu hỏi
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Gọi Agent và hiển thị kết quả
    with st.chat_message("assistant", avatar="👨‍🍳"):
        with st.spinner("Đang tìm kiếm và tổng hợp câu trả lời…"):
            try:
                answer = st.session_state.workflow.retriever_and_generattion(prompt)
            except Exception as exc:
                answer = f"⚠️ Đã xảy ra lỗi: {exc}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
