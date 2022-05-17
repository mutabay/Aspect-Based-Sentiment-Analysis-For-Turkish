// DOM elements
const fileUpload = document.querySelector('#fileUpload')
const textArea = document.querySelector('#textArea')
const accordion = document.querySelector('#accordion')
const btnLoadText = document.querySelector('#loadText')
const docTitle = document.querySelector('#docTitle')
const docDate = document.querySelector('#docDate')
const docMeta = document.querySelector('#docMeta')
const btnSaveMeta = document.querySelector('#saveMetadata')


// Constants
const DEFAULT_HEAD = 0
const DEFAULT_DEP = '-'
const SUPPORTED_EXTS = new Set(['txt', 'csv'])

// Objects
class TagElement {

  constructor(word, innerText, index) {
    this.word = word
    this.innerText = innerText
    this.index = index
    this.head = DEFAULT_HEAD
    this.dep = DEFAULT_DEP
  }

  setEntity() {
    this.head = this.index
    this.dep = 'ENTITY'
  }

  setAttribute(entityTag) {
    this.head = entityTag.index
    this.dep = 'ATTRIBUTE'
  }

  setChild(parentTag) {
    this.head = parentTag.index
    this.dep = 'CHILD'
  }

}

// State
let inputFile = null
let text = ''
let tags = []
let meta = {}
let entityEntries = {}
let modelEntries = []
let sentimentEntries = []

// Utils
function switchAccordion(oneIndex) {
  // TODO index bound check
  $('#accordion').children(`:nth-child(${oneIndex})`)
      .children(':nth-child(2)')
      .collapse('show')
}

function reset() {
  inputFile = null
  text = ''
  tags = []
  meta = {}
  entityEntries = {}
  modelEntries = []
  sentimentEntries = []
}

function createAnnotations() {
  const heads = tags.map(tag => tag.head)
  const deps = tags.map(tag => tag.dep)

  return {
    text: text,
    heads: heads,
    deps: deps
  }
}

function initWindow(window, words) {
  window.innerHTML = ''

  let spaceOffset = 0
  let space = ' '
  let consoleText = ''

  for (let idx = 0; idx < words.length; ++idx) {
    const word = words[idx]

    // Keep track of whitespace offset
    // to maintain proper word index for tags
    if (word.trim().length == 0) {
      ++spaceOffset
      space += word
      continue
    }

    const correctIdx = idx - spaceOffset
    const innerText = space + word
    const tag = new TagElement(word, innerText, correctIdx)
    const spanElem = buildSpan(tag)
    consoleText += innerText

    // Reset space
    space = ' '

    tags.push(tag)
    window.appendChild(spanElem)
  }

  text = consoleText
}