import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
from .fastapi_api import app, DialogRequestModel, Replica, get_sentiment
from typing import List


def button_click(text: str) -> str:
    replicas = []
    speakers = []
    try:
        lines = text.split("\n")
        for line in lines:
            speaker, sentence = line.split(":")
            replica = Replica(text=sentence, speaker=speaker)
            replicas.append(replica)
            speakers.append(speaker)
    except:
        return plt.figure()
    dialog = DialogRequestModel(dialog=replicas)
    response = get_sentiment(dialog)
    labels = response.labels
    df = pd.DataFrame({
        "speakers": speakers,
        "labels": pd.Categorical(labels, categories=["NEGATIVE", "POSITIVE", "NEUTRAL"])
    })
    ax: List[plt.Axes]
    fig, ax = plt.subplots(1, len(set(speakers)))
    res = df.groupby(["speakers", "labels"]).size()
    for i, (speaker, new_df) in enumerate(res.groupby(level=0)):
        ax_i = ax[i] if len(set(speakers)) > 1 else ax
        new_df /= new_df.values.sum()
        new_df.plot(kind="bar", ax=ax_i)
        ax_i.set_xticklabels(["NEG", "POS", "NEU"], rotation=0)
        ax_i.set_xlabel(speaker)
    return fig


def create_demo():
    with gr.Blocks() as demo:
        gr.Markdown("""
        # Интерфейс для анализа тональности реплик из диалогов
        На вход подается диалог в формате:
        ```
        {speaker_name}: {replica}
        ...
        {speaker_name}: {replica}
        ```
        где `{speaker_name}` - имя персонажа, от которого производится реплика 
        `{replica}` - текст реплики персонажа

        На выдохе получаем график распределение тональности реплик 
        для каждого персонажа из диалога<br>
        Всего используется три типа тональности: `позитивная` (POS), `негативная` (NEG) и `нейтральная` (NEU)
        """)
        input_text = gr.Textbox(label="Диалог")
        plot = gr.Plot(label="Распределение тональности реплик для персонажей из диалога")
        button = gr.Button(value="Визуализировать", variant="primary")
        button.click(button_click, input_text, plot)
    return demo


demo = create_demo()
app = gr.mount_gradio_app(app, demo, "/")
