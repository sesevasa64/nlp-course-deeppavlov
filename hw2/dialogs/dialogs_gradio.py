import pandas as pd
import gradio as gr
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from typing import List


df = pd.read_csv("dialogs/data/dialogs_marked_33992.csv")
prop = FontProperties(fname='/mnt/c/Windows/Fonts/seguiemj.ttf')
emotions = ['joy', 'optimism', 'anger', 'sadness']
movie_genres = df["movie_genres"].unique()


def button_click(genres: List[str]) -> str:
    genres = [g.lower() for g in genres]
    df_subset = df[df["movie_genres"].isin(genres)].copy()
    df_subset["emotion"] = pd.Categorical(df_subset["emotion"], categories=emotions)
    fig, ax = plt.subplots()
    df_subset["emotion"].value_counts(normalize=True).plot(kind="bar", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontproperties=prop)
    return fig

def create_demo():
    with gr.Blocks() as demo:
        gr.Markdown("""
            # Визуализация распределения эмоций в диалогах в зависимости от жанра фильма
            Необходимо выбрать один или несколько жанров для визуализации<br>
            Если выбрано несколько жанров, то строится совместное распределение эмоций по всем фильмам из этих жанров
        """)
        checkbox = gr.CheckboxGroup(
            [g.capitalize() for g in movie_genres], 
            label="Жанр", info="Какие жанры вас интересуют?"
        )
        plot = gr.Plot(label="Распределение эмоций")
        button = gr.Button(value="Визуализировать", variant="primary")
        button.click(button_click, checkbox, plot)
    return demo


demo = create_demo()
demo.launch()