# Streaming Service

A simple video streaming website inspired by YouTube. It offers a range of features to enhance your video-watching experience:

1. **Upload and Share Videos**:
    
    + Users can easily upload their videos, whether it’s a vlog, tutorial, or creative content.
    + Share your moments with the world and build your own channel.

2. **Discover and Watch Content**:

    + Explore a vast library of videos uploaded by other users.

3. **Interact with Videos**:

    + Like or dislike videos to express your opinion.
    + Leave comments to let others know your thoughts about the video.

4. **Personalize Your Experience**:

    + Create custom playlists to organize your favorite videos.

5. **Connect with Creators**:

    + Subscribe to your favorite users and stay connected.

Whether you’re a viewer, a content creator, or both, **Streaming Service** provides a seamless platform for sharing, discovering, and enjoying videos. 📽️🍿

## Table of Contents

+ Installation
+ AWS S3 Setup
+ PostgreSQL Setup
+ Tailwind CSS Setup
+ Usage
+ Contributing

## Installation

1. Clone the repository:

    `git clone https://github.com/sahil-313/Streaming-service.git`

2. Navigate to the project directory:

    `cd Streaming-service`

3. Set Up a Virtual Environment:

    + Create a virtual environment for your project (if you haven't already):
    
        `python -m venv myenv`

    + Activate the virtual environment:

        `source myenv/bin/activate`
    
    + If you are on Windows, use this command:
        
        `myenv\Scripts\activate`

4. Install dependencies:

    `pip install -r requirements.txt`

## AWS S3 Setup

1. Create an AWS S3 bucket to store media files (images, videos, etc.).

2. Obtain your AWS access key ID and secret access key.

3. Store these credentials in a `.env` file at the root directory of your project:

    ```
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    ```

4. In `settings.py`, configure the S3 bucket credentials:

    ```python
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'your-region-name'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    ```

## PostgreSQL Setup

1. Create a new PostgreSQL database.

2. Note down the database name, username, password, host and port.

3. In `settings.py`, update the `DATABASES` configuration:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your-db-name',
            'USER': 'your-db-user',
            'PASSWORD': 'your-db-password',
            'HOST': 'your-db-host',
            'PORT': 'your-db-port',
        }
    }
    ```

4. Run database migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

## Tailwind CSS Setup

1. The project relies on Tailwind CSS for styling.

2. The Tailwind configuration file: `tailwind.config.js` with the necessary configurations as well as `package.json` and `package-lock.json` are already available in the project directory.

3. To compile and use Tailwind CSS, follow these steps:

    + Install Node.js (if not already installed).

    + Run the following command: `npx tailwindcss -i ./streamer/static/streamer/style.css -o ./streamer/static/streamer/output.css --watch`

4. Refer the [Tailwind docs](https://tailwindcss.com/docs/installation) for more information on how to use Tailwind.

## Usage

1. Run the development server:

    `python manage.py runserver`

2. Access the app in your browser at `http://localhost:8000`

3. Explore the features and functionalities.

## Contributing

1. Fork the repository.

2. Create a new branch: git checkout -b feature-name

3. Make your changes and commit: git commit -m "Add feature"

4. Push to the branch: git push origin feature-name

5. Create a pull request.