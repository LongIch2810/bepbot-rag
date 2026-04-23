import html

import streamlit as st

from app.config import (
    HYBRID,
    MAX_UPLOAD_FILE_MB,
    MAX_UPLOAD_FILES,
    MAX_UPLOAD_IMAGE_MB,
    SYSTEM_ONLY,
    USER_ONLY,
)
from app.workflow import Workflow


MODE_LABELS = {
    SYSTEM_ONLY: "Chỉ dùng tài liệu hệ thống",
    USER_ONLY: "Chỉ dùng tài liệu người dùng",
    HYBRID: "Dùng cả hai nguồn",
}


st.set_page_config(
    page_title="Chatbot Công Thức Nấu Ăn Việt Nam",
    page_icon="🍲",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] button span,
    [data-testid="collapsedControl"] button span {
        font-family: 'Material Symbols Rounded' !important;
    }

    .stApp {
        background: linear-gradient(160deg, #fff7ed 0%, #fff1e6 40%, #ffe8d6 100%);
    }

    .hero {
        text-align: center;
        padding: 2.25rem 1rem 1.25rem;
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
        color: #6b5a4e;
        font-size: .92rem;
        margin-top: .45rem;
    }

    .status-card {
        display: flex;
        align-items: center;
        gap: .6rem;
        padding: .75rem 1rem;
        border-radius: 12px;
        margin: .8rem auto;
        max-width: 700px;
        font-size: .9rem;
        font-weight: 500;
    }

    .status-ready {
        background: rgba(56, 176, 0, .1);
        border: 1px solid rgba(56, 176, 0, .3);
        color: #2d8a00;
    }

    .status-info {
        background: rgba(247, 127, 0, .12);
        border: 1px solid rgba(247, 127, 0, .35);
        color: #c56200;
    }

    .status-error {
        background: rgba(230, 57, 70, .1);
        border: 1px solid rgba(230, 57, 70, .3);
        color: #c5303a;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3d2c2c 0%, #5c3d2e 50%, #6b4226 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f5e6d3 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #f77f00 0%, #e85d04 100%) !important;
        color: #fffaf3 !important;
        border: 1px solid rgba(255, 219, 181, .28) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 18px rgba(61, 44, 44, .22);
        transition: background .2s ease, color .2s ease, box-shadow .2s ease, transform .2s ease;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #ffd166 0%, #ff9f1c 100%) !important;
        color: #5b2500 !important;
        border-color: rgba(255, 244, 230, .5) !important;
        box-shadow: 0 12px 24px rgba(61, 44, 44, .26);
        transform: translateY(-1px);
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover p,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover span,
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover div {
        color: #5b2500 !important;
        -webkit-text-fill-color: #5b2500 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:disabled {
        background: rgba(255, 255, 255, .14) !important;
        color: rgba(255, 243, 223, .72) !important;
        border-color: rgba(255, 255, 255, .12) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: .55rem;
        font-size: 1.35rem;
        font-weight: 700;
        color: #fff8ef !important;
        line-height: 1.2;
        margin-bottom: .35rem;
    }

    .sidebar-badge {
        display: inline-block;
        padding: .28rem .65rem;
        border-radius: 999px;
        font-size: .75rem;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(255, 183, 77, .4), rgba(247, 127, 0, .35));
        color: #fff3df !important;
        border: 1px solid rgba(255, 214, 165, .25);
        margin-bottom: .35rem;
    }

    [data-testid="stFileUploader"] > label,
    [data-testid="stRadio"] label,
    [data-testid="stFileUploader"] section {
        color: #fff3df !important;
        font-weight: 600;
    }

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #f8ddc1 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(180deg, #fffaf5 0%, #fff2e8 100%) !important;
        border: 1.5px dashed #d48a4a !important;
        border-radius: 16px !important;
        padding: .75rem !important;
        transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, .12);
        background: linear-gradient(180deg, #fff8ef 0%, #ffeddc 100%) !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
        text-shadow: none !important;
    }

    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #4b5563 !important;
        -webkit-text-fill-color: #4b5563 !important;
        opacity: 1 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #fff7ed !important;
        color: #a54f13 !important;
        border: 1px solid rgba(165, 79, 19, .25) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        border-color: #f59e0b !important;
        color: #8a3b12 !important;
        background: #fff1db !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div {
        font-size: .92rem !important;
        line-height: 1.45 !important;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, .72) !important;
        border: 1px solid rgba(214, 120, 63, .15);
        border-radius: 14px !important;
        backdrop-filter: blur(8px);
        margin-bottom: .5rem;
        box-shadow: 0 2px 8px rgba(180, 120, 60, .06);
    }

    .vision-status {
        display: flex;
        align-items: flex-start;
        gap: .75rem;
        margin-top: .8rem;
        padding: .85rem 1rem;
        border-radius: 14px;
        border: 1px solid rgba(214, 120, 63, .16);
        background: linear-gradient(180deg, rgba(255, 250, 245, .96) 0%, rgba(255, 244, 234, .96) 100%);
    }

    .vision-status.loading {
        border-color: rgba(245, 158, 11, .35);
        background: linear-gradient(180deg, rgba(255, 249, 235, .98) 0%, rgba(255, 241, 220, .98) 100%);
    }

    .vision-status.error {
        border-color: rgba(230, 57, 70, .28);
        background: linear-gradient(180deg, rgba(255, 243, 244, .98) 0%, rgba(255, 233, 236, .98) 100%);
    }

    .vision-icon {
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        background: rgba(247, 127, 0, .14);
    }

    .vision-status.error .vision-icon {
        background: rgba(230, 57, 70, .12);
    }

    .vision-copy strong {
        display: block;
        color: #8a3b12;
        font-size: .92rem;
        margin-bottom: .18rem;
    }

    .vision-copy span {
        color: #6b5a4e;
        font-size: .84rem;
        line-height: 1.45;
    }

    .vision-chip-list {
        display: flex;
        flex-wrap: wrap;
        gap: .4rem;
        margin-top: .7rem;
    }

    .vision-chip {
        display: inline-flex;
        align-items: center;
        padding: .28rem .62rem;
        border-radius: 999px;
        background: rgba(214, 120, 63, .1);
        border: 1px solid rgba(214, 120, 63, .18);
        color: #8a3b12;
        font-size: .76rem;
        font-weight: 600;
    }

    .vision-preview {
        margin-top: .7rem;
        padding: .7rem .85rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, .66);
        border: 1px solid rgba(214, 120, 63, .12);
        color: #59483c;
        font-size: .84rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state():
    defaults = {
        "messages": [],
        "system_ready": False,
        "init_error": None,
        "user_docs_ready": False,
        "upload_error": None,
        "upload_results": [],
        "processed_user_files": [],
        "selected_mode": SYSTEM_ONLY,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def available_modes():
    modes = [SYSTEM_ONLY]
    if st.session_state.user_docs_ready:
        modes.extend([USER_ONLY, HYBRID])
    return modes


def process_uploaded_files(workflow, uploaded_files):
    is_valid, message = workflow.validator.validate_upload_files(uploaded_files)
    if not is_valid:
        st.session_state.upload_error = message
        st.session_state.upload_results = []
        return

    validation_results = workflow.validator.validate_food_content(uploaded_files)
    st.session_state.upload_results = validation_results
    st.session_state.upload_error = None

    valid_names = {
        result["file_name"]
        for result in validation_results
        if result["is_food_related"]
    }
    valid_files = [
        uploaded_file
        for uploaded_file in uploaded_files
        if uploaded_file.name in valid_names
    ]

    if not valid_files:
        st.session_state.upload_error = (
            "Không có file hợp lệ để nạp vào user knowledge base."
        )
        return

    workflow.prepare_user_uploads(valid_files)
    st.session_state.user_docs_ready = True
    st.session_state.processed_user_files = [file.name for file in valid_files]
    st.session_state.messages = []


def analyze_turn_image(workflow, uploaded_file):
    is_valid, message = workflow.validator.validate_upload_images([uploaded_file])
    if not is_valid:
        raise ValueError(message)

    results = workflow.validator.analyze_uploaded_images([uploaded_file])
    if not results:
        return None

    result = results[0]
    if result.get("error"):
        raise ValueError(result["error"])

    return result


def render_image_analysis(analysis=None, loading=False, error=None):
    if loading:
        st.markdown(
            """
            <div class="vision-status loading">
                <div class="vision-icon">...</div>
                <div class="vision-copy">
                    <strong>Đang phân tích ảnh</strong>
                    <span>Hệ thống đang chạy vision image để nhận diện nội dung, chữ trong ảnh và ngữ cảnh món ăn.</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if error:
        st.markdown(
            f"""
            <div class="vision-status error">
                <div class="vision-icon">!</div>
                <div class="vision-copy">
                    <strong>Không thể phân tích ảnh</strong>
                    <span>{html.escape(error)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if not analysis:
        return

    chips = []
    if analysis.get("is_food_image"):
        chips.append("Ảnh món ăn")
    if analysis.get("image_label"):
        chips.append(f"Nhãn ảnh: {analysis['image_label']}")
    if analysis.get("is_text"):
        chips.append("Có text trong ảnh")

    chip_markup = "".join(
        f'<span class="vision-chip">{html.escape(chip)}</span>' for chip in chips
    )
    text_content = (analysis.get("text_content") or "").strip()
    preview = ""
    if text_content:
        preview = (
            '<div class="vision-preview"><strong>Text trích từ ảnh:</strong><br>'
            f"{html.escape(text_content)}</div>"
        )

    st.markdown(
        f"""
        <div class="vision-status">
            <div class="vision-icon">OK</div>
            <div class="vision-copy">
                <strong>Đã phân tích ảnh xong</strong>
                <span>Kết quả vision sẽ được đưa vào đúng lượt trả lời hiện tại.</span>
                <div class="vision-chip-list">{chip_markup}</div>
                {preview}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(workflow):
    uploaded_files = []
    process_uploads = False

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title"><span>👨‍🍳</span><span>Công Thức Nấu Ăn</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="sidebar-badge">Multi-source RAG</span>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(
            """
            **Mô tả**  
            Chatbot hỏi đáp về **200 món ăn truyền thống Việt Nam**,
            có thể kết hợp thêm tài liệu do người dùng upload.

            **Cách dùng**  
            1. Upload file PDF, DOCX hoặc TXT.  
            2. Bấm **Xử lý tài liệu** để kiểm duyệt và nạp user docs.  
            3. Trong khung chat, mỗi lần nhắn có thể đính kèm 1 ảnh cùng câu hỏi.  
            4. Ảnh sẽ hiện ngay trong hội thoại và được dùng cho đúng lượt trả lời đó.
            """
        )
        st.markdown("---")

        uploaded_files = st.file_uploader(
            f"Tải tài liệu bổ sung (tối đa {MAX_UPLOAD_FILES} file)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help=(
                f"Mỗi lần xử lý, batch file bạn chọn sẽ thay thế user docs trước đó. "
                f"Tổng dung lượng tối đa cho cả batch là {MAX_UPLOAD_FILE_MB}MB."
            ),
        )
        st.caption(
            f"Giới hạn upload: tối đa {MAX_UPLOAD_FILES} file, tổng dung lượng không vượt quá {MAX_UPLOAD_FILE_MB}MB."
        )
        process_uploads = st.button(
            "Xử lý tài liệu",
            width="stretch",
            disabled=not uploaded_files or not st.session_state.system_ready,
        )

        if st.session_state.user_docs_ready:
            st.success("Đã sẵn sàng truy vấn tài liệu người dùng.")
        else:
            st.info("Hiện chỉ dùng tài liệu hệ thống.")

        if st.session_state.processed_user_files:
            st.caption(
                "Batch user docs hiện tại: "
                + ", ".join(st.session_state.processed_user_files)
            )

        if st.session_state.upload_error:
            st.error(st.session_state.upload_error)

        if st.session_state.upload_results:
            st.markdown("#### Kết quả kiểm duyệt")
            for result in st.session_state.upload_results:
                prefix = "OK" if result["is_food_related"] else "NO"
                st.markdown(f"{prefix} **{result['file_name']}**: {result['content']}")

        current_modes = available_modes()
        if st.session_state.selected_mode not in current_modes:
            st.session_state.selected_mode = SYSTEM_ONLY

        st.radio(
            "Chế độ trả lời",
            options=current_modes,
            format_func=lambda mode: MODE_LABELS[mode],
            key="selected_mode",
        )

    if process_uploads:
        with st.spinner("Đang kiểm duyệt và xử lý tài liệu upload..."):
            try:
                process_uploaded_files(workflow, uploaded_files)
            except Exception as exc:
                st.session_state.upload_error = f"Lỗi khi xử lý tài liệu: {exc}"
            st.rerun()


def render_message(message):
    avatar = "👤" if message["role"] == "user" else "👨‍🍳"
    with st.chat_message(message["role"], avatar=avatar):
        if message.get("image_bytes"):
            st.image(
                message["image_bytes"],
                caption=message.get("image_name") or "Ảnh đính kèm",
                width="stretch",
            )
            if message.get("image_analysis"):
                analysis = message["image_analysis"]
                chips = []
                if analysis.get("image_label"):
                    chips.append(f"Nhãn ảnh: {analysis['image_label']}")
                if analysis.get("text_content"):
                    chips.append("Có text trong ảnh")
                if chips:
                    st.caption(" | ".join(chips))
            if message.get("image_analysis_error"):
                render_image_analysis(error=message["image_analysis_error"])
            elif message.get("image_analysis"):
                render_image_analysis(analysis=message["image_analysis"])

        st.markdown(message["content"])


init_state()


if not st.session_state.system_ready and st.session_state.init_error is None:
    with st.spinner("Đang khởi tạo Workflow và nạp tài liệu hệ thống..."):
        try:
            workflow = Workflow()
            workflow.load_and_process_documents()
            st.session_state.workflow = workflow
            st.session_state.system_ready = True
            st.rerun()
        except Exception as exc:
            st.session_state.init_error = str(exc)
            st.rerun()


if st.session_state.init_error is not None:
    st.markdown(
        f'<div class="status-card status-error">Lỗi khởi tạo: {st.session_state.init_error}</div>',
        unsafe_allow_html=True,
    )
    st.stop()

if not st.session_state.system_ready:
    st.stop()


workflow = st.session_state.workflow
render_sidebar(workflow)

st.markdown(
    """
    <div class="hero">
        <div style="font-size:3.5rem;">🤖👨‍🍳</div>
        <h1>Công Thức Nấu Ăn Việt Nam</h1>
        <p>Hỏi đáp từ tài liệu hệ thống, tài liệu người dùng và ảnh đính kèm theo từng message</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="status-card status-ready">Hệ thống đã sẵn sàng. Chế độ hiện tại: {MODE_LABELS[st.session_state.selected_mode]}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="status-card status-info">Mỗi lần hỏi có thể đính kèm tối đa 1 ảnh JPG/PNG/JPEG, kích thước tối đa {MAX_UPLOAD_IMAGE_MB}MB.</div>',
    unsafe_allow_html=True,
)

if st.session_state.selected_mode != SYSTEM_ONLY and not st.session_state.user_docs_ready:
    st.markdown(
        '<div class="status-card status-info">Cần xử lý ít nhất một tài liệu người dùng hợp lệ để dùng chế độ này.</div>',
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    render_message(message)

placeholder = {
    SYSTEM_ONLY: "Hỏi về công thức từ tài liệu hệ thống...",
    USER_ONLY: "Hỏi dựa trên tài liệu người dùng đã upload...",
    HYBRID: "Hỏi với cả tài liệu hệ thống và tài liệu người dùng...",
}[st.session_state.selected_mode]

chat_payload = st.chat_input(
    placeholder,
    accept_file=True,
    file_type=["png", "jpg", "jpeg"],
    max_upload_size=MAX_UPLOAD_IMAGE_MB,
)

if chat_payload:
    if isinstance(chat_payload, str):
        prompt = chat_payload.strip()
        uploaded_files = []
    else:
        prompt = chat_payload.text.strip()
        uploaded_files = list(chat_payload.files)

    if not prompt:
        st.warning("Cần nhập câu hỏi.")
        st.stop()

    if len(uploaded_files) > 1:
        st.warning("Mỗi lần nhắn chỉ được đính kèm 1 ảnh.")
        st.stop()

    uploaded_image = uploaded_files[0] if uploaded_files else None
    image_analysis = None
    image_bytes = None
    image_name = None

    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        image_name = uploaded_image.name

    user_message = {
        "role": "user",
        "content": prompt,
        "image_bytes": image_bytes,
        "image_name": image_name,
        "image_analysis": None,
        "image_analysis_error": None,
    }

    analysis_placeholder = None
    if uploaded_image is not None:
        with st.chat_message("user"):
            st.image(
                image_bytes,
                caption=image_name or "áº¢nh Ä‘Ã­nh kÃ¨m",
                width="stretch",
            )
            analysis_placeholder = st.empty()
            with analysis_placeholder.container():
                render_image_analysis(loading=True)
            st.markdown(prompt)

    if uploaded_image is not None:
        try:
            image_analysis = analyze_turn_image(workflow, uploaded_image)
            user_message["image_analysis"] = image_analysis
        except Exception as exc:
            user_message["image_analysis_error"] = str(exc)

    if analysis_placeholder is not None:
        with analysis_placeholder.container():
            if user_message["image_analysis_error"]:
                render_image_analysis(error=user_message["image_analysis_error"])
            elif user_message["image_analysis"]:
                render_image_analysis(analysis=user_message["image_analysis"])

    st.session_state.messages.append(user_message)
    if uploaded_image is None:
        render_message(user_message)

    with st.chat_message("assistant", avatar="👨‍🍳"):
        with st.spinner("Đang tìm kiếm và tổng hợp câu trả lời..."):
            try:
                image_context = [image_analysis] if image_analysis else None
                answer = workflow.retriever_and_generattion(
                    prompt,
                    st.session_state.selected_mode,
                    image_context,
                )
            except Exception as exc:
                answer = f"Đã xảy ra lỗi: {exc}"
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
