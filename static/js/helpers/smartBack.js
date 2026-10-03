const RETURN_URL_KEY = 'codelevels:smartBack:returnUrl'

const LIST_PATHS = [
  /^\/projects$/,
  /^\/topics$/,
  /^\/concepts$/,
  /^\/roadmap$/,
  /^\/projects\/course\/[^/]+$/,
  /^\/topics\/language\/[^/]+$/,
  /^\/courses\/course\/\d+$/,
  /^\/roadmap\/course\/[^/]+$/,
]

function isSameOrigin(referrer) {
  if (!referrer) return false
  try {
    return new URL(referrer).origin === window.location.origin
  } catch {
    return false
  }
}

function normalizePath(pathname) {
  if (pathname.length > 1 && pathname.endsWith('/')) {
    return pathname.slice(0, -1)
  }
  return pathname
}

function isListPath(pathname) {
  const path = normalizePath(pathname)
  return LIST_PATHS.some((pattern) => pattern.test(path))
}

function isCurrentOrNestedPage(referrer) {
  try {
    const currentPath = normalizePath(window.location.pathname)
    const referrerPath = normalizePath(new URL(referrer).pathname)
    if (referrerPath === currentPath) return true
    return referrerPath.startsWith(`${currentPath}/`)
  } catch {
    return true
  }
}

export function shouldUseHistoryBack(referrer = document.referrer) {
  if (!isSameOrigin(referrer)) return false
  if (isCurrentOrNestedPage(referrer)) return false
  return true
}

function toStoredUrl(url) {
  return url.pathname + url.search
}

function rememberReturnUrl() {
  try {
    if (isListPath(window.location.pathname)) {
      sessionStorage.setItem(RETURN_URL_KEY, toStoredUrl(window.location))
      return
    }
    if (!isSameOrigin(document.referrer)) return
    const referrer = new URL(document.referrer)
    if (!isListPath(referrer.pathname)) return
    sessionStorage.setItem(RETURN_URL_KEY, toStoredUrl(referrer))
  } catch {
    // sessionStorage can throw in private mode
  }
}

function getRememberedReturnUrl() {
  try {
    const stored = sessionStorage.getItem(RETURN_URL_KEY)
    if (!stored || stored[0] !== '/') return null
    const url = new URL(stored, window.location.origin)
    if (url.origin !== window.location.origin) return null
    if (!isListPath(url.pathname)) return null
    return url.pathname + url.search
  } catch {
    return null
  }
}

function backTitleForReturnUrl(returnUrl, link) {
  const path = normalizePath(new URL(returnUrl, window.location.origin).pathname)
  if (path === '/roadmap' || path.startsWith('/roadmap/course/')) {
    return link.dataset.backTitleRoadmap || link.getAttribute('title')
  }
  if (path === '/topics' || path.startsWith('/topics/language/')) {
    return link.dataset.backTitleTopics || link.getAttribute('title')
  }
  if (path === '/concepts') {
    return link.dataset.backTitleConcepts || link.getAttribute('title')
  }
  if (path.startsWith('/courses/course/')) {
    return link.dataset.backTitleCourses || link.getAttribute('title')
  }
  return link.dataset.backTitleProjects || link.getAttribute('title')
}

function applyRememberedHref() {
  const returnUrl = getRememberedReturnUrl()
  if (!returnUrl) return
  document.querySelectorAll('a[data-smart-back]').forEach((link) => {
    link.setAttribute('href', returnUrl)
    const title = backTitleForReturnUrl(returnUrl, link)
    if (title) {
      link.setAttribute('title', title)
    }
  })
}

function onSmartBackClick(event) {
  const link = event.target.closest('a[data-smart-back]')
  if (!link) return
  if (event.button !== 0) return
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
  if (!shouldUseHistoryBack()) return
  event.preventDefault()
  history.back()
}

let isBound = false

export function initSmartBack() {
  rememberReturnUrl()
  applyRememberedHref()
  if (isBound) return
  isBound = true
  document.addEventListener('click', onSmartBackClick)
}

initSmartBack()
