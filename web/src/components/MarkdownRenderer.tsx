import React, { useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import mermaid from 'mermaid'

mermaid.initialize({ startOnLoad: true, theme: 'default' })

interface CodeProps {
  inline?: boolean
  className?: string
  children?: React.ReactNode
}

const CodeBlock: React.FC<CodeProps> = ({ inline, className, children }) => {
  const match = /language-(\w+)/.exec(className || '')
  const lang = match ? match[1] : ''
  const code = String(children).replace(/\n$/, '')

  useEffect(() => {
    if (lang === 'mermaid') {
      mermaid.contentLoaded()
    }
  }, [lang])

  if (lang === 'mermaid') {
    return (
      <div className="mermaid my-4 flex justify-center overflow-x-auto rounded-lg bg-slate-50 p-4">
        {code}
      </div>
    )
  }

  if (inline) {
    return (
      <code className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-sm text-slate-800">
        {children}
      </code>
    )
  }

  return (
    <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4">
      <code className="font-mono text-sm text-slate-100">{code}</code>
    </pre>
  )
}

interface MarkdownRendererProps {
  content: string
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="prose prose-sm max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: CodeBlock as any,
          h1: ({ children }) => <h1 className="mt-6 mb-4 text-2xl font-bold text-slate-900">{children}</h1>,
          h2: ({ children }) => <h2 className="mt-5 mb-3 text-xl font-bold text-slate-900">{children}</h2>,
          h3: ({ children }) => <h3 className="mt-4 mb-2 text-lg font-semibold text-slate-900">{children}</h3>,
          p: ({ children }) => <p className="my-3 text-slate-700 leading-relaxed">{children}</p>,
          ul: ({ children }) => <ul className="my-3 ml-6 list-disc text-slate-700">{children}</ul>,
          ol: ({ children }) => <ol className="my-3 ml-6 list-decimal text-slate-700">{children}</ol>,
          li: ({ children }) => <li className="my-1">{children}</li>,
          table: ({ children }) => (
            <div className="my-4 overflow-x-auto rounded-lg border border-slate-200">
              <table className="w-full text-sm">{children}</table>
            </div>
          ),
          thead: ({ children }) => <thead className="bg-slate-100 border-b border-slate-200">{children}</thead>,
          tbody: ({ children }) => <tbody>{children}</tbody>,
          tr: ({ children }) => <tr className="border-b border-slate-200 hover:bg-slate-50">{children}</tr>,
          th: ({ children }) => <th className="px-4 py-2 text-left font-semibold text-slate-900">{children}</th>,
          td: ({ children }) => <td className="px-4 py-2 text-slate-700">{children}</td>,
          a: ({ children, href }) => (
            <a href={href} target="_blank" rel="noreferrer" className="text-teal-700 underline hover:text-teal-900">
              {children}
            </a>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-4 border-l-4 border-slate-300 pl-4 italic text-slate-600">{children}</blockquote>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

export default MarkdownRenderer
