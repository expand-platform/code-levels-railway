const SHORT_QUERY = 3

function normalize(value) {
  return String(value || '')
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
}

function editDistance(left, right) {
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

function fuzzyScore(haystack, words, needle) {
  const candidates =
    Math.abs(haystack.length - needle.length) <= 1 ? [haystack, ...words] : words
  let best = 0

  candidates.forEach((candidate) => {
    if (Math.abs(candidate.length - needle.length) > 1) return
    if (editDistance(candidate, needle) !== 1) return
    best = 230
  })

  return best
}

function titleScore(title, needle) {
  const haystack = normalize(title)
  if (!haystack || !needle) return 0
  if (haystack === needle) return 1000

  const words = haystack.split(' ')
  if (needle.length < SHORT_QUERY) {
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

  return fuzzyScore(haystack, words, needle)
}

export class ProjectSearch {
  constructor(projects, limit = 8) {
    this.projects = Array.isArray(projects) ? projects : []
    this.limit = limit
  }

  search(query) {
    const needle = normalize(query)
    if (!needle) return []

    return this.projects
      .map((project) => ({
        project,
        score: titleScore(project && project.title, needle),
      }))
      .filter((hit) => hit.score > 0)
      .sort((left, right) => {
        if (right.score !== left.score) return right.score - left.score
        return String(left.project.title).localeCompare(String(right.project.title))
      })
      .slice(0, this.limit)
      .map((hit) => hit.project)
  }
}
