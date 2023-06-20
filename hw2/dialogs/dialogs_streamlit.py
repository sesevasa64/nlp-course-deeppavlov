import pandas as pd
import altair as alt
import streamlit as st


emotions = ['joy', 'optimism', 'anger', 'sadness']
df = pd.read_csv("dialogs/data/dialogs_marked_33992.csv")
df["emotion"] = pd.Categorical(df["emotion"], categories=emotions)
speakers_count = len(df["speakers"].unique())
movie_titles = list(df["movie_title"].unique())

st.title("Интерфейс для просмотра распределения эмоций реплик из диалогов фильмов")
st.markdown("""
    С помощью интерфейса можно посмотреть на распределение эмоций реплик в конкретном
    фильме или для конкретного персонажа из фильма. В начале необходимо выбрать фильм,
    после чего выбрать персонажа из этого фильма. Если персонаж не выбран, то отображается
    распределение эмоций для всех персонажей из выбранного фильма
""")
st.write(f'Количество фильмов в базе данных: :blue[{len(movie_titles)}], количество персонажей: :blue[{speakers_count}]')

selected_movie = st.selectbox(
    'Какой фильм вас интересует?', [''] + movie_titles,
)

if selected_movie:
    df_subset = df[df["movie_title"] == selected_movie]
    speakers = list(df_subset["speakers"].unique())
    selected_speaker = st.selectbox(
        'Какой персонаж в фильме вас интересует?', [''] + speakers,
    )
    title = f"Распределение эмоций реплик персонажей в фильме: **:blue[{selected_movie}]**"
    if selected_speaker:
        title = f"Распределение эмоций реплик персонажа **:blue[{selected_speaker}]** в фильме: **:blue[{selected_movie}]**"
        df_subset = df_subset[df_subset["speakers"] == selected_speaker]
    st.markdown(title, unsafe_allow_html=False)
    data = df_subset["emotion"].value_counts(normalize=True).to_frame().reset_index()
    c = alt.Chart(data).mark_bar().encode(x="emotion", y="proportion")
    c = c.configure_axis(labelFontSize=16, titleFontSize=16, labelAngle=0)
    st.altair_chart(c, use_container_width=True)
