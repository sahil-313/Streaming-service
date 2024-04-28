document.addEventListener('DOMContentLoaded', function() {
    get_videos();
})

function get_videos()
{
    fetch('/get_videos')
    .then(response => response.json())
    .then(data => {
        const videoContainer = document.getElementById('video-container');

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