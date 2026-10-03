;(function () {
	const root = document.getElementById('project-simple-timeline')
	if (!root) return

	const rawStages = document.getElementById('project-stages-raw')
	const horizontalView = document.getElementById('stages-horizontal-view')
	const verticalView = document.getElementById('stages-vertical-view')
	const track = document.getElementById('timeline-track')
	const title = document.getElementById('timeline-title')
	const text = document.getElementById('timeline-text')
	const prevBtn = root.querySelector('[data-action="prev"]')
	const nextBtn = root.querySelector('[data-action="next"]')

	if (!rawStages || !horizontalView || !verticalView || !track || !title || !text || !prevBtn || !nextBtn) return

	function normalize(value) {
		return (value || '').replace(/\s+/g, ' ').trim()
	}

	function getStageItems(container) {
		const items = []
		const liNodes = container.querySelectorAll('li')

		if (liNodes.length) {
			liNodes.forEach((node) => {
				const parsed = normalize(node.textContent)
				if (parsed) items.push(parsed)
			})
			return items
		}

		const pNodes = container.querySelectorAll('p')
		if (pNodes.length) {
			pNodes.forEach((node) => {
				const parsed = normalize(node.textContent)
				if (parsed) items.push(parsed)
			})
			return items
		}

		return normalize(container.textContent)
			.split(/\s*\n+\s*/)
			.map((line) => normalize(line))
			.filter(Boolean)
	}

	function splitHeadlineAndBody(value) {
		const clean = normalize(value)
		if (!clean) return { headline: '', body: '' }

		const match = clean.match(/^(.+?[.!?])(?:\s+|$)(.*)$/)
		if (!match) return { headline: clean, body: '' }

		return {
			headline: normalize(match[1]).replace(/\.$/, ''),
			body: normalize(match[2]),
		}
	}

	function splitVerticalStage(value) {
		const clean = normalize(value)
		const colonSplit = clean.match(/^([^:]{1,80}):\s*(.+)$/)
		if (colonSplit) {
			return { headline: normalize(colonSplit[1]), body: normalize(colonSplit[2]) }
		}
		return splitHeadlineAndBody(clean)
	}

	const rawStageItems = getStageItems(rawStages)
	const stages = rawStageItems.map(splitHeadlineAndBody)
	if (!stages.length) {
		root.style.display = 'none'
		return
	}

	rawStageItems.map(splitVerticalStage).forEach((stage, index) => {
		const item = document.createElement('li')
		item.className = 'stages-vertical-timeline__item'

		const marker = document.createElement('span')
		marker.className = 'stages-vertical-timeline__marker'
		marker.textContent = String(index + 1)
		marker.setAttribute('aria-hidden', 'true')
		item.appendChild(marker)

		const content = document.createElement('div')
		content.className = 'stages-vertical-timeline__content'
		const heading = document.createElement('h3')
		heading.className = 'stages-vertical-timeline__title'
		heading.textContent = stage.headline || `Stage ${index + 1}`
		content.appendChild(heading)

		if (stage.body) {
			const description = document.createElement('p')
			description.className = 'stages-vertical-timeline__description'
			description.textContent = stage.body
			content.appendChild(description)
		}

		item.appendChild(content)
		verticalView.appendChild(item)
	})

	document.querySelectorAll('input[name="stages-view"]').forEach((toggle) => {
		toggle.addEventListener('change', function () {
			const showVertical = toggle.value === 'timeline' && toggle.checked
			horizontalView.hidden = showVertical
			verticalView.hidden = !showVertical
		})
	})

	let activeIndex = 0

	function setActive(index) {
		activeIndex = index
		const points = track.querySelectorAll('.simple-timeline__point')

		points.forEach((point, pointIndex) => {
			point.classList.toggle('is-active', pointIndex === activeIndex)
			// point.setAttribute('aria-selected', pointIndex === activeIndex ? 'true' : 'false')
			// point.tabIndex = pointIndex === activeIndex ? 0 : -1
		})

		const current = stages[activeIndex]
		title.textContent = current.headline || `Stage ${activeIndex + 1}`
		text.textContent = current.body || current.headline

		prevBtn.disabled = activeIndex === 0
		nextBtn.disabled = activeIndex === stages.length - 1

		const currentPoint = points[activeIndex]
		if (currentPoint) {
			const targetLeft =
				currentPoint.offsetLeft - (track.clientWidth - currentPoint.offsetWidth) / 2
			const maxLeft = Math.max(0, track.scrollWidth - track.clientWidth)
			const safeLeft = Math.max(0, Math.min(targetLeft, maxLeft))

			track.scrollTo({ left: safeLeft, behavior: 'smooth' })
		}
	}

	stages.forEach((_, index) => {
		const point = document.createElement('button')
		point.type = 'button'
		point.className = 'simple-timeline__point'
		point.textContent = String(index + 1)
		point.setAttribute('role', 'tab')
		point.setAttribute('aria-label', `Stage ${index + 1}`)

		point.addEventListener('click', function () {
			setActive(index)
		})

		track.appendChild(point)
	})

	prevBtn.addEventListener('click', function () {
		if (activeIndex > 0) setActive(activeIndex - 1)
	})

	nextBtn.addEventListener('click', function () {
		if (activeIndex < stages.length - 1) setActive(activeIndex + 1)
	})

	setActive(0)
})()
