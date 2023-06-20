import pandas as pd
import streamlit as st


emotions = ['joy', 'optimism', 'anger', 'sadness']
df = pd.read_csv("dialogs/data/dialogs_marked_33992.csv")
df["emotion"] = pd.Categorical(df["emotion"], categories=emotions)
dialogs_count = len(df["dialog_id"].unique())
movie_titles = list(df["movie_title"].unique())


st.title("Интерфейс для аннотации реплик из диалогов")
st.markdown("""
    Для того, чтобы начать размечать реплики, необходимо выбрать фильм, 
    с диалогами из которого вам хотелось бы поработать.
    После этого появятся две реплики из диалога: предыдущая и текущая.
    На основе информации из этих двух реплик необходимо выбрать эмоциональный окрас текущей рекплики на основе одного или нескольких предварительно определнных классов.
""")
st.markdown("""
    Текущие классы для разметки: **joy**, **optimism**, **anger**, **sadness**
""")
st.write(f"Количество фильмов в базе данных: :red[{len(movie_titles)}], количество реплик: :green[{len(df)}], количество диалогов: :blue[{dialogs_count}]")

selected_movie = st.selectbox(
    'Какой фильм вас интересует?', [''] + movie_titles,
)

if selected_movie:
    if selected_movie not in st.session_state:
        st.session_state[selected_movie] = 1
    df_subset = df[df["movie_title"] == selected_movie]
    df_subset = df_subset.reset_index(drop=True)
    current_index = st.session_state[selected_movie]
    prev_row = df_subset.iloc[current_index-1]
    prev_speaker, prev_replica = prev_row["speakers"], prev_row["dialog"]
    curr_row = df_subset.iloc[current_index]
    curr_speaker, curr_replica = curr_row["speakers"], curr_row["dialog"]
    with st.form("My form", clear_on_submit=True):
        st.markdown(f"""
            Предыдущая реплика:
            ```
            {prev_speaker}: {prev_replica}
            ```
        """, unsafe_allow_html=True)
        st.markdown(f"""
            Текущая реплика:
            ```
            {curr_speaker}: {curr_replica}
            ```
        """)
        choices = st.multiselect(
            "Выберите подходящие эмоции к текущей реплике:",
            ['joy', 'optimism', 'anger', 'sadness'],
            key="multiselect"
        )
        if st.form_submit_button("Подтвердите ваш выбор") and choices:
            next_index = current_index + 1
            curr_dialog_id = df_subset.iloc[current_index]["dialog_id"]
            next_dialog_id = df_subset.iloc[next_index]["dialog_id"]
            if curr_dialog_id != next_dialog_id:
                next_index += 1
            st.session_state[selected_movie] = next_index
            st.experimental_rerun()
