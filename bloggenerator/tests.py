from django.http import HttpResponse
from pytube import YouTube

def download_audio( video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        response = HttpResponse(stream.download(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{stream.title}.mp3"'
        return response
    else:
        # Handle cases where the video doesn't have an audio stream
        return HttpResponse('No audio stream found', status=404)
    
download_audio()