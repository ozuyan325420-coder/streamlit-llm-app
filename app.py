import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

st.set_page_config(page_title="AI専門家チャット", page_icon="🤖")

st.title("🤖 AI専門家チャットアプリ")
st.markdown("""
### アプリの概要
このアプリでは、様々な分野の専門家AIに質問することができます。

### 操作方法
1. **専門家の種類を選択**してください（ラジオボタン）
2. **質問を入力**してください
3. **「送信」ボタン**を押すと、選択した専門家として回答が返ってきます
""")

st.divider()

experts = {
    "💊 医療・健康の専門家": "あなたは医療・健康分野の専門家です。医学的な知識をもとに、わかりやすく丁寧に回答してください。ただし、診断や治療の最終判断は必ず医師に相談するよう案内してください。",
    "💰 ファイナンシャルアドバイザー": "あなたは金融・資産運用の専門家です。投資、節約、資産形成に関する質問に対して、わかりやすく実践的なアドバイスを提供してください。ただし、投資判断は自己責任である旨を伝えてください。",
    "🍳 料理・栄養の専門家": "あなたは料理と栄養学の専門家です。レシピの提案、食材の知識、栄養バランスについて詳しく回答してください。初心者にもわかりやすく説明してください。",
    "💻 ITエンジニア": "あなたはソフトウェア開発・IT技術の専門家です。プログラミング、システム設計、技術的な問題解決について、具体的なコード例を交えながら回答してください。",
}


def get_llm_response(user_input: str, expert_type: str) -> str:
    system_message = experts[expert_type]
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input),
    ]
    response = llm.invoke(messages)
    return response.content


selected_expert = st.radio(
    "専門家の種類を選択してください",
    list(experts.keys()),
    horizontal=False,
)

st.markdown(f"**選択中の専門家:** {selected_expert}")

user_input = st.text_area("質問を入力してください", placeholder="ここに質問を入力してください...", height=150)

if st.button("送信", type="primary"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            try:
                answer = get_llm_response(user_input, selected_expert)
                st.success("回答が生成されました！")
                st.markdown("### 回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
