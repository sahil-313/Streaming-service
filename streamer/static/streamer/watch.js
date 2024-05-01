document.addEventListener('DOMContentLoaded', function() {
    
    const expandBtn = document.getElementById('expand-button');
    const additionalDtls = document.getElementById('additional-details');
    expandBtn.addEventListener('click', () => {
        additionalDtls.classList.toggle('hidden');

        expandBtn.textContent = additionalDtls.classList.contains('hidden') ? '▼' : '▲';
    });

    document.querySelectorAll('.action-div').forEach(div => {
        div.addEventListener('click', action);
    });

    document.getElementById('add-to-playlist').addEventListener('click', () => {
        document.getElementById('playlist-menu').classList.toggle('hidden');
        getUserPlaylists();
    });

    document.getElementById('create-playlist').addEventListener('click', () => {
        document.getElementById('new-playlist-form').classList.toggle('hidden');
    });
});

const video_id = document.getElementById('video-id').value;

async function action(event) {
    const div = event.currentTarget;
    const action = div.dataset.action;

    //const video_id = document.getElementById('video-id').value;

    try {
        const response = await fetch(`/action/${action}/${video_id}`, { method: 'POST'});

        if (response.ok) {
            const data = await response.json();

            const likeCountElement = document.querySelector('.action-div[data-action="like"] p');
            const dislikeCountElement = document.querySelector('.action-div[data-action="dislike"] p');

            if (action === 'like') {
                likeCountElement.textContent = data.like_count;
            } else if (action === 'dislike') {
                dislikeCountElement.textContent = data.dislike_count;
            }

            div.classList.remove('bg-gray-950', 'text-red-500', 'hover:bg-red-500', 'hover:text-gray-950', 'hover:ring-2', 'hover:ring-gray-950');
            div.classList.add('bg-red-500', 'text-gray-950', 'ring-2', 'ring-gray-950');
        }
        else {
            console.log(`Error ${action} failed for the video`);
        }
    } catch (error) {
        console.log(error);
    }
}

function getUserPlaylists() {
    const createdPlaylists = document.getElementById('created-playlists');
    createdPlaylists.innerHTML = '';

    fetch('/get_user_playlists')
    .then(response => response.json())
    .then(data => {
        if (data.playlists.length === 0) {
            const noPlaylistName = document.createElement('li');

            noPlaylistName.classList.add('font-nunito', 'text-gray-950');

            noPlaylistName.innerHTML = 'You have not created any playlists';

            createdPlaylists.append(noPlaylistName);
            return;
        }

        data.playlists.forEach(playlist => {
            const playListName = document.createElement('li');

            playListName.classList.add('p-2','font-nunito', 'text-gray-950',
            'hover:cursor-pointer', 'hover:bg-black-dark', 'rounded-lg');

            playListName.innerHTML = playlist;

            playListName.addEventListener('click', () => {
                addToPlaylist(playlist, video_id);
            });

            createdPlaylists.appendChild(playListName);
        });
    })
    .catch(error => console.log(error));
}

async function addToPlaylist(playlist, video_id) {

    try {
        const response = await fetch(`/add_to_playlist/${playlist}/${video_id}`, { method: 'POST'});

        if (response.ok) {
            console.log(response.message);
        }
        else {
            console.log(response.error);
        }
    } catch(error) {
        console.log(error);
    }
}