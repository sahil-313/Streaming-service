document.addEventListener('DOMContentLoaded', function() {
    
    document.getElementById('uploaded-videos-div').addEventListener('click', () => {
        document.getElementById('liked-videos').innerHTML = '';
        displayVideos('uploaded');
    });

    document.getElementById('liked-videos-div').addEventListener('click', () => {
        document.getElementById('uploaded-videos').innerHTML = '';
        displayVideos('liked');
    });

    const editProfileButton = document.getElementById('edit-profile');
        if (editProfileButton) {
            editProfileButton.addEventListener('click', () => {
            document.getElementById('edit-profile-form').classList.toggle('hidden');
            });

            document.getElementById('user-pfp').addEventListener('change', function (event) {
                const pfpPreview = document.getElementById('pfp-preview');
                const file = event.target.files[0];
                if (file) {
                    pfpPreview.src = URL.createObjectURL(file);
                    pfpPreview.classList.remove('hidden');
                } else {
                    // Reset the preview if no file is selected
                    pfpPreview.src = '#';
                }
            });
        }
    

    document.querySelector('.action').addEventListener('click', subOrUnsub);

})

function displayVideos(videoType) {
    const user_id = document.getElementById('user_id').value;
    const containerId = videoType === 'uploaded' ? 'uploaded-videos' : 'liked-videos';

    fetch(`/user_videos/${user_id}/${videoType}`)
        .then(response => response.json())
        .then(data => {
            const videosContainer = document.getElementById(containerId);
            videosContainer.innerHTML = '';

            if (data.videos.length === 0) {
                const message = document.createElement('h1');
                message.textContent = `User has not ${videoType === 'uploaded' ? 'uploaded' : 'liked'} any videos yet 😅`;
                message.classList.add('text-2xl', 'm-4');

                videosContainer.appendChild(message);
                return;
            }

            data.videos.forEach(video => {
                const videoDiv = document.createElement('div');
                videoDiv.classList.add(
                    'bg-white-medium', 'rounded-lg', 'text-white', 'p-4', 'm-2',
                    'hover:bg-gray-950', 'hover:ring-1', 'hover:ring-red-500',
                    'hover:cursor-pointer', 'hover:text-red-500', 'w-1/2'
                );

                const thumbnailImg = document.createElement('img');
                thumbnailImg.src = video.thumbnail;
                thumbnailImg.classList.add('w-full', 'h-48', 'object-cover', 'rounded-lg');

                const titleText = document.createElement('h1');
                titleText.textContent = video.title;
                titleText.classList.add('text-2xl', 'my-4');

                videoDiv.appendChild(thumbnailImg);
                videoDiv.appendChild(titleText);

                videoDiv.addEventListener('click', () => {
                    window.open(`/watch/${video.video_id}`);
                });

                videosContainer.appendChild(videoDiv);
            });
        })
        .catch(error => console.log(error));
}

async function subOrUnsub(event) {

    const user_id = document.getElementById('user_id').value;
    const action = event.target.getAttribute('data-action');

    try {
        const response = await fetch(`/sub_or_unsub/${user_id}/${action}`, { method: 'POST'});
        
        if (response.ok) {
            //const buttonId = action === 'subscribe' ? 'subscribe-button' : 'unsubscribe-button';
            const button = document.querySelector('.action');

            button.innerHTML = action === 'subscribe' ? '- Unsubscribe' : '+ Subscribe';

            button.setAttribute('data-action', action === 'subscribe' ? 'unsubscribe' : 'subscribe');

            console.log(`${action} action successful!`);
        }
        else {
            console.log(`${action} action failed`);
        }
    } catch (error) {
        console.log(error);
    }

}