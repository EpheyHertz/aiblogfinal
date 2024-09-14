import filetype
import logging
import os
import json
from yt_dlp import YoutubeDL
# from youtube_dl import YoutubeDL
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytube import YouTube
from django.conf import settings
import assemblyai as aai
from moviepy.editor import VideoFileClip
from django.core.mail import EmailMessage
import time
import httpx
from django.shortcuts import render

import google.generativeai as genai
from .models import BlogPost
from django.shortcuts import get_object_or_404

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def home(request):
    return render(request, 'index.html')
@csrf_exempt
@login_required
def contact(request):
    # Retrieve the authenticated user's email
    user_email = request.user.email if request.user.is_authenticated else ''

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Debugging output
        #print(f"Received email: {email}, name: {name}, message: {message}")

        # Validate form data (basic example)
        if not name or not email or not message:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        # Send email logic
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.CONTACT_EMAIL]
        subject = f'Contact Form Submission from {name}'
        body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'

        try:
            email_message = EmailMessage(subject, body, from_email, to_email)
            email_message.send()
            return JsonResponse({'message': f'Thank you, {name}! Your message has been sent.'})
        except Exception as e:
            print(f"Error sending email: {e}")
            return JsonResponse({'error': 'Something went wrong. If this persists, try sending your email to "epheynyaga@gmail.com". Sorry for the inconvenience.'}, status=500)

    # Render the contact page and pass the user's email
    return render(request, 'contact.html', {'user_email': user_email})
@login_required
def dashboard(request):
    return render(request, 'home.html')



@csrf_exempt
def is_video_file(file):
    try:
        kind = filetype.guess(file.read())
        file.seek(0)  # Reset file pointer to the start
        return kind and kind.mime.startswith('video/')
    except Exception as e:
        logging.error(f"Error determining file type: {e}", exc_info=True)
        return False
@login_required
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            youtube_link = request.POST.get('youtube_link')
            file = request.FILES.get('file')

            if youtube_link:
                title = yt_title(youtube_link)
                # Download audio from the YouTube link
                audio_file = download_audio(youtube_link)
                if not audio_file:
                    return JsonResponse({'error': 'Failed to download audio from YouTube'}, status=500)

                # Get the transcription from the audio file
                transcription = get_transcription_from_file(audio_file)  # Custom transcription function
                if not transcription:
                    return JsonResponse({'error': 'Failed to transcribe the audio'}, status=500)

                # Generate the blog content from the transcription
                blog_content = generate_blog_from_transcription(transcription)
                if not blog_content:
                    return JsonResponse({'error': 'Failed to generate blog article'}, status=500)

                # Save the blog article
                new_blog_article = BlogPost.objects.create(
                    user=request.user,
                    youtube_title=title,
                    youtube_link=youtube_link,
                    transcript=transcription,
                    generated_content=blog_content
                )
                new_blog_article.save()

            elif file:
                # Handle file upload (audio/video)
                title = file.name
                file_path = save_file(file)  # Custom function to save the file and return the path

                if not file_path:
                    return JsonResponse({'error': 'Failed to save the uploaded file'}, status=500)

                # Check if the file is a video
                if is_video_file(file):
                    audio_file_path = extract_audio_from_video(file_path)  # Custom function to extract audio
                    if not audio_file_path:
                        return JsonResponse({'error': 'Failed to extract audio from video'}, status=500)
                else:
                    audio_file_path = file_path

                # Get the transcription from the file
                transcription = get_transcription_from_file(audio_file_path)
                if not transcription:
                    return JsonResponse({'error': 'Failed to transcribe the audio'}, status=500)

                # Generate the blog content
                blog_content = generate_blog_from_transcription(transcription)
                if not blog_content:
                    return JsonResponse({'error': 'Failed to generate blog article'}, status=500)

                # Save the blog article
                new_blog_article = BlogPost.objects.create(
                    user=request.user,
                    youtube_title=title,
                    youtube_link=file_path,  # Store the file path in youtube_link
                    transcript=transcription,
                    generated_content=blog_content
                )
                new_blog_article.save()

            else:
                return JsonResponse({'error': 'You must provide either a YouTube link or upload a file'}, status=400)

            return JsonResponse({"content": blog_content})

        except (KeyError, json.JSONDecodeError) as e:
            logging.error(f"Error processing POST data: {e}")
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def extract_audio_from_video(video_path):
    try:
        # Load the video file
        video = VideoFileClip(video_path)

        # Extract the audio
        audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
        video.audio.write_audiofile(audio_path)

        return audio_path

    except Exception as e:
        logging.error(f"Error extracting audio from video: {e}", exc_info=True)
        return None

def yt_title(link):
    try:
        yt = YouTube(link)
        title = yt.title
        return title
    except Exception as e:
        logging.error(f"Error fetching YouTube title for link {link}: {e}")
        return None

def download_audio(link):
    try:
        # YouTube-DL options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
            'retries': 5,  # Retry up to 5 times in case of failure
            'timeout': 60,  # Set timeout to 60 seconds for the download
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)  # Download audio
            file_path = ydl.prepare_filename(info_dict)
            base, ext = os.path.splitext(file_path)
            new_file = base + '.mp3'  # Change extension to .webm

            # Rename file if it already exists
            if os.path.exists(new_file):
                base = f"{base}_{info_dict['id']}"
                new_file = base + '.mp3'

            os.rename(file_path, new_file)  # Rename the downloaded file
            logging.info(f"File renamed successfully to: {new_file}")

        return new_file

    except Exception as e:
        logging.error(f"Error downloading audio from {link}: {e}", exc_info=True)
        return None


def save_file(file):
    file_name = file.name
    file_path = os.path.join('media/', file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def get_transcription(link):
    try:
        audio_file = download_audio(link)
        if not audio_file:
            return None

        aai.settings.api_key =  settings.AAI_API_KEY # Use Django settings for API key
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        return transcript.text

    except Exception as e:
        logging.error(f"Error in get_transcription function: {e}", exc_info=True)
        return None
    
MAX_RETRIES = 5
RETRY_DELAY = 5 
    
def get_transcription_from_file(file_path):
    def transcribe_with_retries():
        """Attempt to transcribe the file with retries."""
        for attempt in range(MAX_RETRIES):
            try:
                with open(file_path, 'rb') as audio_file:
                    transcript = transcriber.transcribe(audio_file)
                return transcript.text
            except httpx.WriteTimeout:
                logging.warning(f"Write timeout, retrying ({attempt + 1}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY)
            except Exception as e:
                logging.error(f"Error during transcription attempt {attempt + 1}: {e}", exc_info=True)
                if attempt == MAX_RETRIES - 1:
                    raise  # Re-raise the exception if all retries are exhausted
                time.sleep(RETRY_DELAY)

        logging.error("Failed to get transcription after several retries.")
        return None

    try:
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None

        # Set the API key for the transcriber
        aai.settings.api_key = settings.AAI_API_KEY
        transcriber = aai.Transcriber()

        # Retry the transcription process
        transcript_text = transcribe_with_retries()
        return transcript_text

    except Exception as e:
        logging.error(f"Error in get_transcription_from_file function: {e}", exc_info=True)
        return None
def generate_blog_from_transcription(transcription):
    def generate_with_retries():
        """Attempt to generate blog content with retries."""
        for attempt in range(MAX_RETRIES):
            try:
                response = model.generate_content(
                    transcription_text,
                    generation_config=generation_config
                )
                logging.info(f"Generation attempt {attempt + 1}/{MAX_RETRIES}: Response received.")
                
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if candidate.finish_reason == "SAFETY":
                        logging.error("Content generation blocked due to safety concerns.")
                        return "The content could not be generated as it was flagged for safety concerns."
                    elif hasattr(candidate, 'content') and candidate.content.parts:
                        generated_content = ''.join([part.text for part in candidate.content.parts])
                        return generated_content
                    else:
                        logging.error("The response does not contain valid 'text' in the candidate.")
                else:
                    logging.error("The response does not contain valid 'candidates'.")
                
            except Exception as e:
                logging.error(f"Error during generation attempt {attempt + 1}: {e}", exc_info=True)
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY)

        logging.error("Failed to generate content after several retries.")
        return "Content could not be generated due to repeated failures. Please try again later."

    try:
        gemini_api_key = settings.GEMINI_API_KEY 
        genai.configure(api_key=gemini_api_key)
        print(transcription)

        transcription_text = f"""
        Create a blog article from the provided transcript:

        {transcription}
        Structure the article as follows:
        1. Introduction: Briefly introduce the main topic or theme of the discussion.
        2. Body: Summarize the content based on timestamps.
        3. Conclusion: Summarize the key takeaways from the discussion.
        Format: Use clear headings and subheadings for different timestamps. 
        Write in an engaging and professional tone.
        """

        model = genai.GenerativeModel('gemini-1.5-flash')

        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            stop_sequences=["in Conclusion", "\n\n\n\n\n"],
            max_output_tokens=1000,
            temperature=0.5
        )

        # Retry the blog generation process
        generated_content = generate_with_retries()
        return generated_content

    except Exception as e:
        logging.error(f"Error in generate_blog_from_transcription function: {e}", exc_info=True)
        return None

@login_required
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request,'allblogpost.html',{'blog_articles':blog_articles})
@login_required
def blog_details(request,pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request,'blogdetails.html',{'blog_article_detail':blog_article_detail})
    else:
        return redirect('/')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend explicitly
            login(request, user)
            logging.info(f"The user logged in is: {user}")
            return redirect('/dashboard')
        else:
            logging.warning("Login failed")
            error_message = "Invalid user. Please sign up if you don't have an account."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                error_message = 'A user with this email already exists.'
                logging.warning(f"Attempted registration with existing email: {email}")
                return render(request, 'register.html', {'error_message': error_message})

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend explicitly
                login(request, user)

                logging.info(f"User registered and logged in: {user}")
                return redirect('/dashboard')

            except Exception as e:
                logging.error(f"Error registering user: {e}")
                error_message = 'Error occurred while registering the user. Please try again.'
                return render(request, 'register.html', {'error_message': error_message})

        else:
            error_message = 'Passwords do not match.'
            logging.warning(f"Password mismatch for email: {email}")
            return render(request, 'register.html', {'error_message': error_message})

    else:
        # Handle GET request by rendering the signup form
        return render(request, 'register.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')
@login_required
@csrf_exempt
def delete_blog(request, blog_id):
    if request.method == 'POST':
        try:
            blog = get_object_or_404(BlogPost, id=blog_id)
            blog.delete()
            return redirect('/blog-posts/')
            # return JsonResponse({"success": True, "message": "Blog deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    # return JsonResponse({"success": False, "message": "Invalid request method"})
    return redirect('/blog-posts/')
