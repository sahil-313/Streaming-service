document.addEventListener('DOMContentLoaded', function() {

    // By default, get all the videos when the page is loaded or refreshed
    get_videos();

    document.getElementById('home').addEventListener('click', get_videos);

    document.getElementById('subscriptions').addEventListener('click', subscriptions_videos);

    document.getElementById('playlists').addEventListener('click', playlists);

})

function get_videos()
{
    const videoContainer = document.getElementById('video-container');

    videoContainer.innerHTML = '';
    videoContainer.classList.remove('hidden');
    document.getElementById('subscriptions-container').classList.add('hidden');
    document.getElementById('playlists-container').classList.add('hidden');

    fetch('/get_videos')
    .then(response => response.json())
    .then(data => {

        data.videos.forEach(video => {
            const videoDiv = document.createElement('div');
            videoDiv.classList.add('bg-white-medium', 'rounded-lg', 'text-white', 'p-4', 'm-2', 'hover:bg-gray-950',
            'hover:ring-1', 'hover:ring-red-500', 'hover:cursor-pointer', 'hover:text-red-500');

            const thumbnailImg = document.createElement('img');
            thumbnailImg.src = video.thumbnail;
            thumbnailImg.classList.add('w-full', 'h-48', 'object-cover', 'rounded-lg');

            const titleText = document.createElement('h1');
            titleText.textContent = video.title;
            titleText.classList.add('text-2xl', 'my-4');

            const creatorText = document.createElement('a');
            creatorText.href = `profile/${video.creator_id}`;
            creatorText.textContent = `Posted by: ${video.creator}`;
            creatorText.classList.add('my-4');

            videoDiv.appendChild(thumbnailImg);
            videoDiv.appendChild(titleText);
            videoDiv.appendChild(creatorText);

            videoDiv.addEventListener('click', () => {
                window.open(`/watch/${video.video_id}`);
            });

            videoContainer.appendChild(videoDiv);
        });
    })
    .catch(error => console.log(error));
}

function subscriptions_videos()
{
    const subscriptionsContainer = document.getElementById('subscriptions-container');
    
    subscriptionsContainer.innerHTML = '';
    subscriptionsContainer.classList.remove('hidden');
    subscriptionsContainer.classList.add('grid');
    document.getElementById('video-container').classList.add('hidden');
    document.getElementById('playlists-container').classList.add('hidden');

    fetch('/subscriptions_videos')
    .then(response => response.json())
    .then(data => {

        data.videos.forEach(video => {
            const videoDiv = document.createElement('div');
            videoDiv.classList.add('bg-white-medium', 'rounded-lg', 'text-white', 'p-4', 'm-2', 'hover:bg-gray-950',
            'hover:ring-1', 'hover:ring-red-500', 'hover:cursor-pointer', 'hover:text-red-500');

            const thumbnailImg = document.createElement('img');
            thumbnailImg.src = video.thumbnail;
            thumbnailImg.classList.add('w-full', 'h-48', 'object-cover', 'rounded-lg');

            const titleText = document.createElement('h1');
            titleText.textContent = video.title;
            titleText.classList.add('text-2xl', 'my-4');

            const creatorText = document.createElement('a');
            creatorText.href = `profile/${video.creator_id}`;
            creatorText.textContent = `Posted by: ${video.creator}`;
            creatorText.classList.add('my-4');

            videoDiv.appendChild(thumbnailImg);
            videoDiv.appendChild(titleText);
            videoDiv.appendChild(creatorText);

            videoDiv.addEventListener('click', () => {
                window.open(`/watch/${video.video_id}`);
            });

            subscriptionsContainer.appendChild(videoDiv);
        });
    })
    .catch(error => console.log(error));
}

function playlists() {
    const playlistsContainer = document.getElementById('playlists-container');

    playlistsContainer.innerHTML = '';
    playlistsContainer.classList.remove('hidden');
    playlistsContainer.classList.add('grid');
    document.getElementById('video-container').classList.add('hidden');
    document.getElementById('subscriptions-container').classList.add('hidden');

    fetch('/get_user_playlists')
    .then(response => response.json())
    .then(data => {
        if (data.playlists.length === 0) {
            const message = document.createElement('h1');

            message.classList.add('font-nunito', 'text-gray-950', 'text-3xl');

            message.innerHTML = 'You have not created any playlists';

            playlistsContainer.append(message);
            return;
        }

        data.playlists.forEach(playlist => {
            const playlistDiv = document.createElement('div');

            playlistDiv.classList.add('bg-white-medium', 'rounded-lg', 'text-white', 
            'p-4', 'm-2', 'hover:bg-gray-950', 'hover:ring-1', 'hover:ring-red-500', 
            'hover:cursor-pointer', 'hover:text-red-500', 'playlist-div');

            playlistDiv.innerHTML = playlist;

            playlistsContainer.appendChild(playlistDiv);
        });

        playlistClickHandlers();
    })
    .catch(error => console.log(error));
}

function playlistClickHandlers() {
    const playlistDivs = document.querySelectorAll('.playlist-div'); // Adjust the selector based on your actual class name
    const playlistsContainer = document.getElementById('playlists-container'); // Assuming you have a container for playlists

    playlistDivs.forEach(playlistDiv => {
        playlistDiv.addEventListener('click', () => {
            // Hide other playlist divs (except the clicked one)
            playlistDivs.forEach(div => {
                //if (div !== playlistDiv) {
                    div.style.display = 'none';
                //}
            });

            // Fetch and display videos for the selected playlist
            const playlistName = playlistDiv.innerHTML; // Assuming the playlist name is directly set as innerHTML
            fetchVideosForPlaylist(playlistName); // Implement this function to fetch videos

            // Create a back button
            const backButton = document.createElement('button');
            backButton.innerText = 'Back to Playlists';
            backButton.id = 'back-button';
            backButton.classList.add('back-button', 'bg-red-500', 'text-gray-950', 'rounded-lg', 'w-1/2', 'p-2', 'h-10'); // Add your desired CSS class for styling
            backButton.addEventListener('click', () => {
                // Show all playlist divs again
                playlistDivs.forEach(div => {
                    div.style.display = 'block';
                });
                // Hide the videos (implement this)
                const playListVideos = document.querySelectorAll('.playlist-video');
                playListVideos.forEach(video => {
                    video.style.display = 'none';
                });
                backButton.style.display = 'none'; // Hide the back button
            });

            // Append the back button to the playlists container
            playlistsContainer.appendChild(backButton);
        });
    });
}

function fetchVideosForPlaylist(playlistName) {

    const playlistsContainer = document.getElementById('playlists-container');

    fetch(`/playlist_content/${playlistName}`)
    .then(response => response.json())
    .then(data => {

        if (data.videos.length === 0) {
            const message = document.createElement('h1');
            message.innerHTML = 'No videos in this playlist';
            message.classList.add('text-2xl', 'font-nunito', 'font-semibold', 'text-white', 'playlist-video');
            playlistsContainer.append(message);
            return;
        }

        data.videos.forEach(video => {
            const playlistVideoDiv = document.createElement('div');
            playlistVideoDiv.classList.add('bg-white-medium', 'rounded-lg', 'text-white', 'p-4', 'm-2', 'hover:bg-gray-950',
            'hover:ring-1', 'hover:ring-red-500', 'hover:cursor-pointer', 'hover:text-red-500', 'playlist-video');

            const thumbnailImg = document.createElement('img');
            thumbnailImg.src = video.thumbnail;
            thumbnailImg.classList.add('w-full', 'h-48', 'object-cover', 'rounded-lg');

            const titleText = document.createElement('h1');
            titleText.textContent = video.title;
            titleText.classList.add('text-2xl', 'my-4');

            const creatorText = document.createElement('a');
            creatorText.href = `profile/${video.creator_id}`;
            creatorText.textContent = `Posted by: ${video.creator}`;
            creatorText.classList.add('my-4');

            playlistVideoDiv.appendChild(thumbnailImg);
            playlistVideoDiv.appendChild(titleText);
            playlistVideoDiv.appendChild(creatorText);

            playlistVideoDiv.addEventListener('click', () => {
                window.open(`/watch/${video.video_id}`);
            });

            playlistsContainer.appendChild(playlistVideoDiv);
        });
    })
    .catch(error => console.log(error));

}