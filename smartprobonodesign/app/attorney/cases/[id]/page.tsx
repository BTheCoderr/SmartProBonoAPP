"use client"

import { useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { mockData } from "@/lib/mock-data"
import {
  ArrowLeft,
  MessageSquare,
  FileText,
  Clock,
  User,
  Phone,
  Mail,
  MapPin,
  Download,
  Upload,
  Plus,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import Link from "next/link"

export default function CaseDetails() {
  const params = useParams()
  const router = useRouter()
  const { toast } = useToast()
  const [newNote, setNewNote] = useState("")
  const [timeEntry, setTimeEntry] = useState({ hours: "", description: "" })

  const case_ = mockData.cases.find((c) => c.id === params.id)
  const client = mockData.users.find((u) => u.id === case_?.clientId)

  if (!case_) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Case Not Found</h1>
          <p className="text-slate-600 mb-4">The case you're looking for doesn't exist.</p>
          <Button onClick={() => router.back()}>Go Back</Button>
        </div>
      </div>
    )
  }

  const handleAcceptCase = () => {
    toast({
      title: "Case accepted!",
      description: "You have successfully accepted this case. The client will be notified.",
    })
  }

  const handleAddNote = () => {
    if (newNote.trim()) {
      toast({
        title: "Note added",
        description: "Your case note has been saved.",
      })
      setNewNote("")
    }
  }

  const handleTimeEntry = () => {
    if (timeEntry.hours && timeEntry.description) {
      toast({
        title: "Time logged",
        description: `${timeEntry.hours} hours logged for this case.`,
      })
      setTimeEntry({ hours: "", description: "" })
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-4 mb-4">
            <Button variant="ghost" size="sm" onClick={() => router.back()}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-slate-900">{case_.title}</h1>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant="outline">{case_.category}</Badge>
                <Badge variant={case_.status === "Active" ? "default" : "secondary"}>{case_.status}</Badge>
                {case_.priority && (
                  <Badge
                    variant={
                      case_.priority === "High" ? "destructive" : case_.priority === "Medium" ? "default" : "secondary"
                    }
                  >
                    {case_.priority} Priority
                  </Badge>
                )}
              </div>
            </div>
            <div className="flex gap-2">
              {case_.status === "Open" && <Button onClick={handleAcceptCase}>Accept Case</Button>}
              {case_.status === "Active" && (
                <>
                  <Button variant="outline" asChild>
                    <Link href={`/attorney/cases/${case_.id}/messages`}>
                      <MessageSquare className="h-4 w-4 mr-2" />
                      Message Client
                    </Link>
                  </Button>
                  <Button>Update Status</Button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Client Information Sidebar */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Client Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {client && (
                  <>
                    <div className="flex items-center gap-3">
                      <User className="h-5 w-5 text-slate-600" />
                      <div>
                        <div className="font-medium">{client.name}</div>
                        <div className="text-sm text-slate-600">{client.role}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Mail className="h-5 w-5 text-slate-600" />
                      <div className="text-sm">{client.email}</div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Phone className="h-5 w-5 text-slate-600" />
                      <div className="text-sm">+1 (555) 123-4567</div>
                    </div>
                    <div className="flex items-center gap-3">
                      <MapPin className="h-5 w-5 text-slate-600" />
                      <div className="text-sm">San Francisco, CA</div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Case Timeline</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <div className="w-2 h-2 bg-green-600 rounded-full mt-2" />
                    <div>
                      <div className="font-medium text-sm">Case Created</div>
                      <div className="text-xs text-slate-600">{new Date(case_.createdAt).toLocaleDateString()}</div>
                    </div>
                  </div>
                  {case_.status === "Active" && (
                    <div className="flex gap-3">
                      <div className="w-2 h-2 bg-blue-600 rounded-full mt-2" />
                      <div>
                        <div className="font-medium text-sm">Case Accepted</div>
                        <div className="text-xs text-slate-600">{new Date(case_.updatedAt).toLocaleDateString()}</div>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="overview" className="space-y-6">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="documents">Documents</TabsTrigger>
                <TabsTrigger value="notes">Notes</TabsTrigger>
                <TabsTrigger value="time">Time Tracking</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Case Description</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-700 leading-relaxed">{case_.description}</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Case Details</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label className="text-sm font-medium text-slate-600">Category</Label>
                        <div className="mt-1">{case_.category}</div>
                      </div>
                      <div>
                        <Label className="text-sm font-medium text-slate-600">Priority</Label>
                        <div className="mt-1">{case_.priority || "Medium"}</div>
                      </div>
                      <div>
                        <Label className="text-sm font-medium text-slate-600">Created</Label>
                        <div className="mt-1">{new Date(case_.createdAt).toLocaleDateString()}</div>
                      </div>
                      <div>
                        <Label className="text-sm font-medium text-slate-600">Last Updated</Label>
                        <div className="mt-1">{new Date(case_.updatedAt).toLocaleDateString()}</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="documents" className="space-y-6">
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle>Case Documents</CardTitle>
                      <Button size="sm">
                        <Upload className="h-4 w-4 mr-2" />
                        Upload Document
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {[
                        { name: "Initial Intake Form.pdf", size: "2.4 MB", date: "2024-02-15" },
                        { name: "Supporting Documents.zip", size: "8.1 MB", date: "2024-02-16" },
                        { name: "Client Statement.docx", size: "156 KB", date: "2024-02-18" },
                      ].map((doc, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                          <div className="flex items-center gap-3">
                            <FileText className="h-5 w-5 text-slate-600" />
                            <div>
                              <div className="font-medium text-sm">{doc.name}</div>
                              <div className="text-xs text-slate-500">
                                {doc.size} • {doc.date}
                              </div>
                            </div>
                          </div>
                          <Button variant="ghost" size="sm">
                            <Download className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="notes" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Add Case Note</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <Textarea
                        placeholder="Add a note about this case..."
                        value={newNote}
                        onChange={(e) => setNewNote(e.target.value)}
                        rows={4}
                      />
                      <Button onClick={handleAddNote} disabled={!newNote.trim()}>
                        <Plus className="h-4 w-4 mr-2" />
                        Add Note
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Case Notes</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {[
                        {
                          date: "2024-02-20",
                          note: "Initial client consultation completed. Reviewed all documents and discussed case strategy.",
                        },
                        {
                          date: "2024-02-18",
                          note: "Received additional supporting documents from client. Need to review immigration history.",
                        },
                        {
                          date: "2024-02-15",
                          note: "Case accepted. Scheduled initial consultation for February 20th.",
                        },
                      ].map((note, index) => (
                        <div key={index} className="p-4 bg-slate-50 rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <Clock className="h-4 w-4 text-slate-600" />
                            <span className="text-sm font-medium text-slate-600">{note.date}</span>
                          </div>
                          <p className="text-slate-700">{note.note}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="time" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Log Time</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <Label htmlFor="hours">Hours</Label>
                          <Input
                            id="hours"
                            type="number"
                            step="0.25"
                            placeholder="2.5"
                            value={timeEntry.hours}
                            onChange={(e) => setTimeEntry({ ...timeEntry, hours: e.target.value })}
                          />
                        </div>
                        <div>
                          <Label htmlFor="description">Description</Label>
                          <Input
                            id="description"
                            placeholder="Client consultation, document review, etc."
                            value={timeEntry.description}
                            onChange={(e) => setTimeEntry({ ...timeEntry, description: e.target.value })}
                          />
                        </div>
                      </div>
                      <Button onClick={handleTimeEntry} disabled={!timeEntry.hours || !timeEntry.description}>
                        <Clock className="h-4 w-4 mr-2" />
                        Log Time
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Time Entries</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {[
                        { date: "2024-02-20", hours: 2.0, description: "Initial client consultation" },
                        { date: "2024-02-18", hours: 1.5, description: "Document review and analysis" },
                        { date: "2024-02-15", hours: 0.5, description: "Case acceptance and initial review" },
                      ].map((entry, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                          <div>
                            <div className="font-medium text-sm">{entry.description}</div>
                            <div className="text-xs text-slate-500">{entry.date}</div>
                          </div>
                          <div className="text-sm font-medium">{entry.hours}h</div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-4 pt-4 border-t">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">Total Hours:</span>
                        <span className="font-bold text-lg">4.0h</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}
