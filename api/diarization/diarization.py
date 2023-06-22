def diarize(audio_file):

    file_path = audio_file.temporary_file_path()
    print("=====", file_path)
    
    return audio_file