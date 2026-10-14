let openHandler = null

export function setOpenSearch(handler) {
  openHandler = handler
}

export function openSearch() {
  if (openHandler) openHandler()
}


export class ProjectSearch {
  static #SHORT_QUERY = 3
  static #catalogs = new Map()

  static load(url) {
    const cached = ProjectSearch.#catalogs.get(url)
    if (cached) return cached

    const request = fetch(url, {
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
        ProjectSearch.#catalogs.delete(url)
        throw error
      })

    ProjectSearch.#catalogs.set(url, request)
    return request
  }

  static hasCatalog(url) {
    return ProjectSearch.#catalogs.has(url)
  }

  constructor(projects, limit = 8) {
    this.projects = Array.isArray(projects) ? projects : []
    this.limit = limit
  }

  search(query) {
    const needle = ProjectSearch.#normalize(query)
    if (!needle) return []

    return this.projects
      .map((project) => ({
        project,
        score: ProjectSearch.#titleScore(project && project.title, needle),
      }))
      .filter((hit) => hit.score > 0)
      .sort((left, right) => {
        const kindOrder =
          ProjectSearch.#kindRank(right.project) - ProjectSearch.#kindRank(left.project)
        if (kindOrder !== 0) return kindOrder
        if (right.score !== left.score) return right.score - left.score
        return String(left.project.title).localeCompare(String(right.project.title))
      })
      .slice(0, this.limit)
      .map((hit) => hit.project)
  }

  static #normalize(value) {
    return String(value || '')
      .toLowerCase()
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ')
      .trim()
  }

  static #editDistance(left, right) {
    const rows = left.length + 1
    const cols = right.length + 1
    const grid = Array.from({ length: rows }, () => new Array(cols).fill(0))

    for (let row = 0; row < rows; row += 1) grid[row][0] = row
    for (let col = 0; col < cols; col += 1) grid[0][col] = col

    for (let row = 1; row < rows; row += 1) {
      for (let col = 1; col < cols; col += 1) {
        const cost = left[row - 1] === right[col - 1] ? 0 : 1
        let value = Math.min(
          grid[row - 1][col] + 1,
          grid[row][col - 1] + 1,
          grid[row - 1][col - 1] + cost
        )
        const swapped =
          row > 1 &&
          col > 1 &&
          left[row - 1] === right[col - 2] &&
          left[row - 2] === right[col - 1]
        if (swapped) value = Math.min(value, grid[row - 2][col - 2] + 1)
        grid[row][col] = value
      }
    }

    return grid[left.length][right.length]
  }

  static #fuzzyScore(haystack, words, needle) {
    const candidates =
      Math.abs(haystack.length - needle.length) <= 1 ? [haystack, ...words] : words
    let best = 0

    candidates.forEach((candidate) => {
      if (Math.abs(candidate.length - needle.length) > 1) return
      if (ProjectSearch.#editDistance(candidate, needle) !== 1) return
      best = 230
    })

    return best
  }

  static #kindRank(project) {
    return project && project.kind === 'roadmap' ? 1 : 0
  }

  static #titleScore(title, needle) {
    const haystack = ProjectSearch.#normalize(title)
    if (!haystack || !needle) return 0
    if (haystack === needle) return 1000

    const words = haystack.split(' ')
    if (needle.length < ProjectSearch.#SHORT_QUERY) {
      if (haystack.startsWith(needle)) return 800
      return words.some((word) => word.startsWith(needle)) ? 700 : 0
    }

    if (haystack.startsWith(needle)) return 800

    const index = haystack.indexOf(needle)
    if (index !== -1) return 600 - index

    const compactHaystack = haystack.replace(/ /g, '')
    const compactNeedle = needle.replace(/ /g, '')
    if (compactNeedle && compactHaystack.includes(compactNeedle)) return 500

    const tokens = needle.split(' ')
    if (tokens.length > 1 && tokens.every((token) => haystack.includes(token))) return 400

    return ProjectSearch.#fuzzyScore(haystack, words, needle)
  }
}
