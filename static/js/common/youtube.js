const YoutubeHeight = 500;
const YoutubeWidth = '100%';

document.addEventListener('DOMContentLoaded', function () {
	const content = document.querySelector('.lesson-details .content');
	let youtubeParagraph = null;

	if (content) {
		const paragraphs = content.querySelectorAll('p');
		paragraphs.forEach(p => {
			if (p.textContent.includes('[[youtube]]') || p.textContent.includes('[[ youtube ]]')) {
				youtubeParagraph = p;
			}
		});
	}

	if (youtubeParagraph && window.lessonYoutubeUrl) {
		console.log('youtube shortcode detected');
		const videoId = extractYoutubeVideoId(window.lessonYoutubeUrl);
		if (videoId) {
			const wrapper = insertYoutubeIframe(videoId);
			youtubeParagraph.replaceWith(wrapper);
		}
	}
});

function extractYoutubeVideoId(url) {
	// Handles various YouTube URL formats
	const regex = /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?|shorts)\/|.*[?&]v=)|youtu\.be\/)([\w-]{11})/;
	const match = url.match(regex);
	return match ? match[1] : null;
}

function insertYoutubeIframe(videoId) {
	const wrapper = document.createElement('div');
	wrapper.innerHTML =
		`<iframe width="${YoutubeWidth}" height="${YoutubeHeight}" src="https://www.youtube.com/embed/${videoId}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>`;
	return wrapper;
}
