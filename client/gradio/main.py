import io
import gradio as gr
import os
from dotenv import load_dotenv
import diarization as d
from PIL import Image

# load_dotenv()
# diarization_api = os.getenv('')


def handle_process_btn(recorded, uploaded):
    if recorded:
        audio_path = recorded
    elif uploaded:
        audio_path = uploaded
    else:
        return "record or upload an audio file"
    audio_file = open(audio_path, "rb")
    result = d.async_diarize(audio_file)
    if result == None:
        return 'reached timeout'
    return d.parse_diarize_result(result)


def handle_process_btn_image(recorded, uploaded):
    if recorded:
        audio_path = recorded
    elif uploaded:
        audio_path = uploaded
    else:
        return "record or upload an audio file"
    audio_file = open(audio_path, "rb")
    result = d.diarize(audio_file)
    im = Image.open(io.BytesIO(result))
    return im


with gr.Blocks().queue(max_size=5) as demo:
    gr.Markdown(
        """
    # Speaker Diarization
    Start recording to see the output.
    """)
    with gr.Row():
        recorded_audio = gr.Audio(
            source="microphone", type="filepath", label="record")
        uploaded_audio = gr.Audio(type="filepath", label="from drive")
    process_btn = gr.Button("Process")
    output = gr.Textbox(label="result")
    process_btn.click(fn=handle_process_btn, inputs=[
                      recorded_audio, uploaded_audio], outputs=output, api_name="process")


    demo.launch(share=False)
