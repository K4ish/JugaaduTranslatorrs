Changelog
All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

[1.2.1] - 2025-07-18
Fixed
Corrected a SyntaxError related to the use of a global variable.

Refactored state management to reliably use st.session_state for audio data, resolving issues where recordings were lost on app reruns.

Improved UI feedback with more descriptive status messages and a clearer flow for saving notes.

[1.2.0] - 2025-07-17
Changed
Geolocation is now optional. Users can save text or audio notes without providing their location.

Improved UI feedback during the save process with more descriptive spinner messages.

Enhanced error messages to better diagnose issues related to Supabase policies for the database table and storage bucket.

Fixed
Critical: Corrected a typo in the Supabase API key that was causing all database and storage operations to fail with an "Invalid API key" error.

[1.1.0] - 2025-07-17
Added
Added a "Saved Notes" section to fetch and display all previously saved notes from the Supabase database.

Included an audio player to play back recorded audio associated with each note.

Added a "Refresh Notes" button to manually reload the list of notes.

Fixed
Resolved a major state management bug where recorded audio was lost after clicking the "Save" button. The application now correctly uses st.session_state to persist the audio data across Streamlit reruns.

[1.0.0] - 2025-07-17
Added
Initial release of the Geo-Notes application.

Core functionality to record audio notes and capture browser geolocation.

Integration with Supabase for backend storage:

Note metadata (text, location) is saved to a Supabase PostgreSQL table.

Recorded audio files are uploaded to Supabase Storage.

Created app.py for the Streamlit application logic.

Added requirements.txt with all necessary Python dependencies.

Configured Dockerfile for deployment on Hugging Face Spaces.