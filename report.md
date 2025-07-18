Project Report: Geo-Notes Application
Author: Bombaclats  Date: 2025-07-18 Version: 1.2.1

1. Project Overview
This report details the development of the Geo-Notes application, a web-based tool designed to capture and store user notes with optional geolocation and audio recordings. The primary objective was to create an open-source application that leverages a modern cloud backend for data persistence and can be easily deployed to a public platform.

The application evolved from an initial concept of an offline-first, browser-storage-based app to a more robust, cloud-connected Streamlit application using Supabase for its backend, ensuring data is accessible from any device.

2. Technology Stack
The application was built using a combination of modern, open-source technologies:

Frontend Framework: Streamlit - A Python library for creating interactive web applications with simple Python scripts.

Backend-as-a-Service (BaaS): Supabase - An open-source alternative to Firebase, providing a PostgreSQL database, storage, and authentication.

Programming Language: Python 3.10

Key Python Libraries:

supabase-py: The official Python client for interacting with the Supabase API.

streamlit-webrtc: For capturing real-time audio from the user's microphone in the browser.

streamlit-js-eval: To execute JavaScript in the browser to fetch the client's geolocation data.

pydub: For processing and handling audio data.

Deployment Platform: Hugging Face Spaces - Using the Docker runtime for containerized deployment.

Containerization: Docker - For creating a consistent and reproducible runtime environment.

3. Core Features
The final application includes the following key features:

3.1. Note Creation
Users can input multi-line text notes through a simple text area.

3.2. Geolocation Capture (Optional)
A "Get Geolocation" button uses the browser's Geolocation API to capture the user's current latitude and longitude.

This feature is optional; users can save notes without providing their location.

The application handles browser permission requests gracefully.

3.3. Audio Recording (Optional)
Users can record audio clips directly in the application using their microphone.

The streamlit-webrtc component provides a real-time interface for starting and stopping recordings.

Recorded audio can be previewed before saving and is stored as a .webm file.

3.4. Cloud Storage with Supabase
Database: All note metadata (text, latitude, longitude, and a URL to the audio file) is saved to a PostgreSQL table named notes in a Supabase project.

File Storage: Recorded audio clips are uploaded to a Supabase Storage bucket named audio-notes, and the public URL is stored in the database.

3.5. Note Display
The application fetches and displays all previously saved notes in reverse chronological order.

Each note displays its text, an embedded audio player (if audio was recorded), and its location and date.

4. Database Schema
The application relies on a single table in the Supabase PostgreSQL database.

Table Name: notes

Column Name

Data Type

Description

id

int8

Primary Key (auto-generated)

created_at

timestamptz

Timestamp of when the note was created (auto-generated)

text

text

The user-submitted text content of the note.

audio_url

text

The public URL of the audio file in Supabase Storage.

latitude

float8

The latitude of the user's location.

longitude

float8

The longitude of the user's location.

5. Deployment
The application is designed for easy deployment on Hugging Face Spaces using Docker.

Prerequisites: A configured Supabase project with the notes table and audio-notes storage bucket created.

Configuration: The app.py file must be updated with the project's Supabase URL and public anon key.

Hugging Face Space: A new Space is created using the Docker SDK.

File Upload: The app.py, requirements.txt, and Dockerfile are uploaded to the Space repository.

Build Process: Hugging Face automatically builds the Docker image based on the Dockerfile, installs all Python dependencies, and runs the Streamlit application.

6. Challenges and Resolutions
Challenge: Initial versions of the app failed to save audio recordings due to Streamlit's stateless nature, which caused the recorded data to be lost on script reruns.

Resolution: This was solved by implementing st.session_state to correctly persist the audio data and other state variables (like location) across user interactions.

Challenge: The application frequently failed to save data to Supabase without clear errors.

Resolution: The issue was traced to Supabase's default Row Level Security (RLS) policies, which block all public access. The resolution involved guiding the user to create appropriate policies in their Supabase dashboard to allow INSERT operations on the notes table and SELECT/INSERT on the audio-notes storage bucket.

Challenge: A persistent "Invalid API key" error was traced back to a typo in the hardcoded key.

Resolution: The key was corrected, and the error handling was improved to provide more specific feedback for different types of database errors.