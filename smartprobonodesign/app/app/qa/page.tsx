"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Send, Bot, User, ExternalLink, Download, Copy } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
  sources?: Array<{
    title: string
    url: string
    snippet: string
  }>
  suggestions?: string[]
}

const mockSources = [
  {
    title: "Immigration Law Basics - USCIS",
    url: "https://uscis.gov/immigration-basics",
    snippet: "Overview of immigration processes and requirements...",
  },
  {
    title: "Tenant Rights Guide - HUD",
    url: "https://hud.gov/tenant-rights",
    snippet: "Understanding your rights as a tenant...",
  },
  {
    title: "Family Law Resources - Legal Aid",
    url: "https://legalaid.org/family-law",
    snippet: "Resources for family law matters including divorce and custody...",
  },
]

const suggestedQuestions = [
  "What documents do I need for a green card application?",
  "How can I respond to an eviction notice?",
  "What are my rights during a divorce proceeding?",
  "How do I file for unemployment benefits?",
  "What should I do if I'm facing workplace discrimination?",
]

export default function QAPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I'm your legal Q&A assistant. I can help answer questions about various legal topics including immigration, housing, family law, employment, and more. What would you like to know?",
      timestamp: new Date(),
      suggestions: suggestedQuestions.slice(0, 3),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: message,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: `Based on your question about "${message}", here's what I can tell you:

This is a complex legal matter that requires careful consideration. Generally speaking, you should:

1. **Document everything** - Keep records of all relevant communications and documents
2. **Know your rights** - Understanding your legal rights is crucial in this situation
3. **Consider timing** - Many legal matters have specific deadlines that must be met
4. **Seek professional help** - While I can provide general information, consulting with a qualified attorney is recommended for your specific situation

Please note that this is general legal information and not specific legal advice. Every situation is unique and may require different approaches.`,
        timestamp: new Date(),
        sources: mockSources.slice(0, 2),
        suggestions: [
          "What documents should I gather?",
          "What are the typical timelines?",
          "How do I find a qualified attorney?",
        ],
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 2000)
  }

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copied to clipboard",
      description: "The message has been copied to your clipboard.",
    })
  }

  const exportConversation = () => {
    const conversationText = messages.map((msg) => `${msg.type.toUpperCase()}: ${msg.content}\n`).join("\n")

    const blob = new Blob([conversationText], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "legal-qa-conversation.txt"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    toast({
      title: "Conversation exported",
      description: "Your conversation has been downloaded as a text file.",
    })
  }

  return (
    <div className="container py-8 max-w-6xl">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold">Legal Q&A Assistant</h1>
            <p className="text-muted-foreground">Get answers to your legal questions from our AI-powered assistant</p>
          </div>
          <Button variant="outline" onClick={exportConversation}>
            <Download className="mr-2 h-4 w-4" />
            Export Chat
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Chat Area */}
          <div className="lg:col-span-3">
            <Card className="h-[600px] flex flex-col">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bot className="h-5 w-5" />
                  Legal Assistant
                </CardTitle>
                <CardDescription>Ask questions about legal matters and get helpful guidance</CardDescription>
              </CardHeader>

              <CardContent className="flex-1 flex flex-col">
                <ScrollArea className="flex-1 pr-4">
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div key={message.id} className="space-y-2">
                        <div className={`flex gap-3 ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                          <div
                            className={`flex gap-3 max-w-[80%] ${message.type === "user" ? "flex-row-reverse" : ""}`}
                          >
                            <div
                              className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                message.type === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                              }`}
                            >
                              {message.type === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                            </div>
                            <div
                              className={`rounded-lg p-4 ${
                                message.type === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                              }`}
                            >
                              <div className="whitespace-pre-wrap">{message.content}</div>
                              {message.type === "assistant" && (
                                <div className="mt-2 flex gap-2">
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => copyToClipboard(message.content)}
                                    className="h-6 px-2"
                                  >
                                    <Copy className="h-3 w-3" />
                                  </Button>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Sources */}
                        {message.sources && (
                          <div className="ml-11 space-y-2">
                            <p className="text-sm font-medium text-muted-foreground">Sources:</p>
                            <div className="space-y-2">
                              {message.sources.map((source, index) => (
                                <Card key={index} className="p-3">
                                  <div className="flex items-start justify-between">
                                    <div className="space-y-1">
                                      <h4 className="text-sm font-medium">{source.title}</h4>
                                      <p className="text-xs text-muted-foreground">{source.snippet}</p>
                                    </div>
                                    <Button variant="ghost" size="sm" asChild>
                                      <a href={source.url} target="_blank" rel="noopener noreferrer">
                                        <ExternalLink className="h-3 w-3" />
                                      </a>
                                    </Button>
                                  </div>
                                </Card>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Suggestions */}
                        {message.suggestions && (
                          <div className="ml-11 space-y-2">
                            <p className="text-sm font-medium text-muted-foreground">Follow-up questions:</p>
                            <div className="flex flex-wrap gap-2">
                              {message.suggestions.map((suggestion, index) => (
                                <Button
                                  key={index}
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleSuggestionClick(suggestion)}
                                  className="text-xs"
                                >
                                  {suggestion}
                                </Button>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}

                    {isLoading && (
                      <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                          <Bot className="h-4 w-4" />
                        </div>
                        <div className="bg-muted rounded-lg p-4">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-200"></div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  <div ref={messagesEndRef} />
                </ScrollArea>

                <Separator className="my-4" />

                <div className="flex gap-2">
                  <Input
                    placeholder="Ask a legal question..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault()
                        handleSendMessage(inputValue)
                      }
                    }}
                    disabled={isLoading}
                  />
                  <Button onClick={() => handleSendMessage(inputValue)} disabled={isLoading || !inputValue.trim()}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Questions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Popular Questions</CardTitle>
                <CardDescription>Click to ask these common questions</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {suggestedQuestions.map((question, index) => (
                  <Button
                    key={index}
                    variant="ghost"
                    className="w-full text-left justify-start h-auto p-3 whitespace-normal"
                    onClick={() => handleSuggestionClick(question)}
                  >
                    {question}
                  </Button>
                ))}
              </CardContent>
            </Card>

            {/* Legal Categories */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Legal Areas</CardTitle>
                <CardDescription>We can help with these topics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {[
                    "Immigration",
                    "Housing",
                    "Family Law",
                    "Employment",
                    "Benefits",
                    "Consumer Rights",
                    "Criminal Defense",
                    "Civil Rights",
                  ].map((category) => (
                    <Badge key={category} variant="secondary">
                      {category}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Disclaimer */}
            <Card className="border-amber-200 bg-amber-50 dark:bg-amber-950/20">
              <CardHeader>
                <CardTitle className="text-base text-amber-800 dark:text-amber-200">Important Notice</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-amber-700 dark:text-amber-300">
                <p>
                  This AI assistant provides general legal information, not legal advice. For specific legal matters,
                  please consult with a qualified attorney.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
