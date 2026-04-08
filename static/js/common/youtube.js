const YoutubeHeight = 500;
const YoutubeWidth = '100%';

document.addEventListener('DOMContentLoaded', function () {
	const existingIframe = document.querySelector('.lesson-details .lesson-video iframe');
	const iframeYoutubeUrl = existingIframe ? (existingIframe.dataset.youtubeUrl || '').trim() : '';
	const youtubeUrl = (window.lessonYoutubeUrl || iframeYoutubeUrl || '').trim();
	if (!youtubeUrl) return;

	const embedUrl = normalizeYoutubeEmbedUrl(youtubeUrl);
	if (!embedUrl) return;

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

	if (youtubeParagraph) {
		const wrapper = insertYoutubeIframe(embedUrl);
		youtubeParagraph.replaceWith(wrapper);
		return;
	}

	// No shortcode: render from admin field in predefined container if it exists.
	if (existingIframe) {
		existingIframe.src = embedUrl;
		existingIframe.allow =
			'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
		existingIframe.referrerPolicy = 'strict-origin-when-cross-origin';
		existingIframe.setAttribute('allowfullscreen', '');
	}
});

function normalizeYoutubeEmbedUrl(rawUrl) {
	if (!rawUrl) return null;

	let normalizedUrl = String(rawUrl).trim().replace(/&amp;/g, '&');

	const iframeSrcMatch = normalizedUrl.match(/src=["']([^"']+)["']/i);
	if (iframeSrcMatch && iframeSrcMatch[1]) {
		normalizedUrl = iframeSrcMatch[1].trim();
	}

	if (normalizedUrl.startsWith('//')) {
		normalizedUrl = `https:${normalizedUrl}`;
	} else if (normalizedUrl.startsWith('www.')) {
		normalizedUrl = `https://${normalizedUrl}`;
	} else if (!/^https?:\/\//i.test(normalizedUrl)) {
		normalizedUrl = `https://${normalizedUrl}`;
	}

	normalizedUrl = normalizedUrl.replace(/^http:\/\//i, 'https://');

	if (/youtube-nocookie\.com\/embed\//i.test(normalizedUrl)) {
		return normalizedUrl;
	}

	const videoId = extractYoutubeVideoId(normalizedUrl);
	if (!videoId) {
		const looseIdMatch = normalizedUrl.match(/([A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)/);
		if (looseIdMatch && looseIdMatch[1]) {
			return buildYoutubeEmbedUrl(looseIdMatch[1]);
		}
	}
	return videoId ? buildYoutubeEmbedUrl(videoId) : null;
}

function extractYoutubeVideoId(url) {
	if (!url) return null;

	const normalizedUrl = String(url).trim().replace(/&amp;/g, '&');

	try {
		const parsed = new URL(normalizedUrl);
		const host = parsed.hostname.replace(/^www\./, '');

		if (host === 'youtu.be') {
			const id = parsed.pathname.split('/').filter(Boolean)[0];
			if (id && id.length === 11) return id;
		}

		if (host === 'youtube.com' || host === 'm.youtube.com' || host === 'music.youtube.com') {
			if (parsed.pathname.includes('/embed/')) {
				const parts = parsed.pathname.split('/').filter(Boolean);
				const embedIdx = parts.indexOf('embed');
				if (embedIdx !== -1 && parts[embedIdx + 1] && parts[embedIdx + 1].length === 11) {
					return parts[embedIdx + 1];
				}
			}

			const fromQuery = parsed.searchParams.get('v');
			if (fromQuery && fromQuery.length === 11) return fromQuery;

			const parts = parsed.pathname.split('/').filter(Boolean);
			const markerIndex = parts.findIndex((part) => ['embed', 'shorts', 'live', 'v', 'e'].includes(part));
			if (markerIndex !== -1 && parts[markerIndex + 1] && parts[markerIndex + 1].length === 11) {
				return parts[markerIndex + 1];
			}
		}
	} catch (error) {
		// Fall back to regex parsing for non-standard or malformed URLs.
	}

	const regex = /(?:youtube\.com\/(?:.*[?&]v=|(?:embed|shorts|live|v|e)\/)|youtu\.be\/)([\w-]{11})/;
	const match = normalizedUrl.match(regex);
	return match ? match[1] : null;
}

function insertYoutubeIframe(videoId) {
	const wrapper = document.createElement('div');
	wrapper.innerHTML =
		`<iframe width="${YoutubeWidth}" height="${YoutubeHeight}" src="${videoId}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>`;
	return wrapper;
}

function buildYoutubeEmbedUrl(videoId) {
	return `https://www.youtube.com/embed/${videoId}`;
}
