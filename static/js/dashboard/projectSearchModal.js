import { ProjectSearch } from '../helpers/projectSearch.js'

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function safeUrl(url) {
  if (typeof url !== 'string') return ''
  if (url.startsWith('/') && !url.startsWith('//')) return url
  try {
    const parsed = new URL(url)
    if (parsed.protocol === 'https:' || parsed.protocol === 'http:') return parsed.href
  } catch {
    return ''
  }
  return ''
}

function isExternalHref(href) {
  return href.startsWith('http://') || href.startsWith('https://')
}

function highlight(title, query) {
  const source = String(title || '')
  const needle = query.trim()
  if (needle.length < 2) return escapeHtml(source)

  const index = source.toLowerCase().indexOf(needle.toLowerCase())
  if (index === -1) return escapeHtml(source)

  const end = index + needle.length
  return (
    escapeHtml(source.slice(0, index)) +
    '<mark>' +
    escapeHtml(source.slice(index, end)) +
    '</mark>' +
    escapeHtml(source.slice(end))
  )
}

function setupProjectSearch(root) {
  const field = root.querySelector('#project-search-field')
  const results = root.querySelector('#project-search-results')
  const status = root.querySelector('[data-project-search-status]')
  if (!field || !results || !status || !window.bootstrap) return

  const messages = {
    hint: root.dataset.msgHint || '',
    empty: root.dataset.msgEmpty || '',
    loading: root.dataset.msgLoading || '',
    error: root.dataset.msgError || '',
  }
  let modal = new window.bootstrap.Modal(root)
  let catalogPromise = null
  let requestId = 0
  let activeIndex = -1

  function loadCatalog() {
    if (!catalogPromise) {
      catalogPromise = fetch(root.dataset.searchUrl, {
        headers: { Accept: 'application/json' },
      })
        .then((response) => {
          const contentType = response.headers.get('content-type') || ''
          if (!response.ok || !contentType.includes('application/json')) {
            throw new Error('search index failed')
          }
          return response.json()
        })
        .then((data) => new ProjectSearch(data.projects))
        .catch((error) => {
          catalogPromise = null
          throw error
        })
    }
    return catalogPromise
  }

  function showStatus(message) {
    results.hidden = true
    results.innerHTML = ''
    status.hidden = false
    status.textContent = message
    field.removeAttribute('aria-activedescendant')
    field.setAttribute('aria-expanded', 'false')
    activeIndex = -1
  }

  function setActive(index) {
    const options = results.querySelectorAll('[role="option"]')
    if (!options.length) return

    const next = (index + options.length) % options.length
    if (next === activeIndex && options[next].classList.contains('is-active')) return
    activeIndex = next
    options.forEach((option, optionIndex) => {
      const selected = optionIndex === next
      option.classList.toggle('is-active', selected)
      option.setAttribute('aria-selected', selected ? 'true' : 'false')
      if (selected) {
        field.setAttribute('aria-activedescendant', option.id)
        option.scrollIntoView({ block: 'nearest' })
      }
    })
  }

  function render(query, matches) {
    const visible = (matches || []).filter((project) => safeUrl(project.url))
    if (!query.trim()) {
      showStatus(messages.hint)
      return
    }
    if (!visible.length) {
      showStatus(messages.empty)
      return
    }

    status.hidden = true
    results.hidden = false
    results.innerHTML = visible
      .map((project, index) => {
        const course = project.course
          ? '<span class="project-search-results__course">' + escapeHtml(project.course) + '</span>'
          : ''
        const href = safeUrl(project.url)
        const external = isExternalHref(href)
        const blank = external ? ' target="_blank" rel="noopener noreferrer" data-external="1"' : ''
        return (
          '<li><a id="project-search-option-' +
          index +
          '" class="project-search-results__link" role="option" href="' +
          escapeHtml(href) +
          '"' +
          blank +
          '><span class="project-search-results__title">' +
          highlight(project.title, query) +
          '</span>' +
          course +
          '</a></li>'
        )
      })
      .join('')
    field.setAttribute('aria-expanded', 'true')
    setActive(0)
  }

  function searchNow() {
    const query = field.value
    const id = ++requestId
    if (!query.trim()) {
      showStatus(messages.hint)
      return
    }
    if (!catalogPromise) showStatus(messages.loading)

    loadCatalog()
      .then((search) => {
        if (id !== requestId || !root.classList.contains('show')) return
        render(query, search.search(query))
      })
      .catch(() => {
        if (id !== requestId || !root.classList.contains('show')) return
        showStatus(messages.error)
      })
  }

  function forceClose() {
    requestId += 1
    field.value = ''
    showStatus(messages.hint)
    modal.dispose()
    root.classList.remove('show')
    root.style.display = ''
    root.setAttribute('aria-hidden', 'true')
    root.removeAttribute('aria-modal')
    document.body.classList.remove('modal-open')
    document.body.style.removeProperty('padding-right')
    document.querySelectorAll('.modal-backdrop').forEach((node) => node.remove())
    modal = new window.bootstrap.Modal(root)
  }

  function openProject(option) {
    const href = option.href
    const external = option.dataset.external === '1'
    forceClose()
    if (external) {
      window.open(href, '_blank', 'noopener,noreferrer')
      return
    }
    window.location.assign(href)
  }

  function openSearch() {
    if (root.classList.contains('show')) {
      field.focus()
      field.select()
    } else {
      modal.show()
    }
    loadCatalog().catch(() => {
      if (!root.classList.contains('show') || field.value.trim()) return
      showStatus(messages.error)
    })
  }

  field.addEventListener('input', searchNow)

  field.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      setActive(activeIndex + 1)
    } else if (event.key === 'ArrowUp') {
      event.preventDefault()
      setActive(activeIndex - 1)
    } else if (event.key === 'Enter') {
      const active = results.querySelector('.is-active')
      if (!active) return
      event.preventDefault()
      openProject(active)
    } else if (event.key === 'Escape') {
      event.preventDefault()
      event.stopPropagation()
      modal.hide()
    }
  })

  results.addEventListener('click', (event) => {
    const option = event.target.closest('a[href]')
    if (!option || !results.contains(option)) return
    event.preventDefault()
    openProject(option)
  })

  results.addEventListener('mousemove', (event) => {
    const option = event.target.closest('[role="option"]')
    if (!option || !results.contains(option)) return
    const options = Array.from(results.querySelectorAll('[role="option"]'))
    setActive(options.indexOf(option))
  })

  root.addEventListener('shown.bs.modal', () => {
    field.focus()
    field.select()
  })

  root.addEventListener('hidden.bs.modal', () => {
    requestId += 1
    field.value = ''
    showStatus(messages.hint)
  })

  document.addEventListener('keydown', (event) => {
    if (event.repeat || event.shiftKey || event.altKey) return
    if (!(event.ctrlKey || event.metaKey) || event.key.toLowerCase() !== 'i') return
    event.preventDefault()
    openSearch()
  })

  document.querySelectorAll('[data-project-search-open]').forEach((button) => {
    button.addEventListener('click', openSearch)
  })

  window.addEventListener('pagehide', forceClose)
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) forceClose()
  })
}

document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('project-search-modal')
  if (root) setupProjectSearch(root)
})
