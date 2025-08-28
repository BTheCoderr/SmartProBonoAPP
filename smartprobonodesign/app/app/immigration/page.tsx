"use client"

import { Calendar } from "@/components/ui/calendar"
import { useAuth } from "@/hooks/useAuth"
import { mockData } from "@/lib/mock-data"
import {
  Plus,
  CheckCircle,
  Clock,
  AlertCircle,
  FileText,
  ExternalLink,
  BookOpen,
  MessageSquare,
  Phone,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import Link from "next/link"
import { useState } from "react"

export default function ImmigrationDashboard() {
  const { user } = useAuth()
  const [selectedCase, setSelectedCase] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState("overview")

  const immigrationCases = mockData.cases.filter((c) => c.category === "Immigration")
  const currentCase = selectedCase ? immigrationCases.find((c) => c.id === selectedCase) : immigrationCases[0]

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Immigration Services</h1>
              <p className="text-slate-600 mt-1">Manage your immigration cases and applications</p>
            </div>
            <Button asChild>
              <Link href="/immigration/intake">
                <Plus className="h-4 w-4 mr-2" />
                New Immigration Case
              </Link>
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Cases Sidebar */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Your Cases</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <div className="space-y-1">
                  {immigrationCases.map((case_) => (
                    <button
                      key={case_.id}
                      onClick={() => setSelectedCase(case_.id)}
                      className={`w-full text-left p-4 hover:bg-slate-50 border-l-4 transition-colors ${
                        currentCase?.id === case_.id ? "border-l-blue-500 bg-blue-50" : "border-l-transparent"
                      }`}
                    >
                      <div className="font-medium text-sm">{case_.title}</div>
                      <div className="text-xs text-slate-500 mt-1">{case_.status}</div>
                      <div className="text-xs text-slate-400 mt-1">
                        Updated {new Date(case_.updatedAt).toLocaleDateString()}
                      </div>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {currentCase ? (
              <div className="space-y-6">
                {/* Case Header */}
                <Card>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-xl">{currentCase.title}</CardTitle>
                        <p className="text-slate-600 mt-1">{currentCase.description}</p>
                      </div>
                      <Badge variant={currentCase.status === "Active" ? "default" : "secondary"}>
                        {currentCase.status}
                      </Badge>
                    </div>
                  </CardHeader>
                </Card>

                {/* Tabs */}
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                  <TabsList className="grid w-full grid-cols-4">
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="documents">Documents</TabsTrigger>
                    <TabsTrigger value="timeline">Timeline</TabsTrigger>
                    <TabsTrigger value="resources">Resources</TabsTrigger>
                  </TabsList>

                  <TabsContent value="overview" className="space-y-6">
                    {/* Progress Overview */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Case Progress</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">Overall Progress</span>
                            <span className="text-sm text-slate-600">65%</span>
                          </div>
                          <Progress value={65} className="h-2" />

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                            <div className="text-center p-4 bg-green-50 rounded-lg">
                              <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                              <div className="font-medium text-green-900">Forms Submitted</div>
                              <div className="text-sm text-green-700">I-485, I-765</div>
                            </div>
                            <div className="text-center p-4 bg-yellow-50 rounded-lg">
                              <Clock className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                              <div className="font-medium text-yellow-900">Pending Review</div>
                              <div className="text-sm text-yellow-700">Supporting Documents</div>
                            </div>
                            <div className="text-center p-4 bg-blue-50 rounded-lg">
                              <FileText className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                              <div className="font-medium text-blue-900">Next Step</div>
                              <div className="text-sm text-blue-700">Biometrics Appointment</div>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Important Dates */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Important Dates</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <div className="flex items-center gap-3">
                              <Calendar className="h-4 w-4 text-slate-600" />
                              <span className="font-medium">Biometrics Appointment</span>
                            </div>
                            <span className="text-sm text-slate-600">March 15, 2024</span>
                          </div>
                          <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <div className="flex items-center gap-3">
                              <Clock className="h-4 w-4 text-slate-600" />
                              <span className="font-medium">Work Authorization Expires</span>
                            </div>
                            <span className="text-sm text-slate-600">June 30, 2024</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="documents" className="space-y-6">
                    <Card>
                      <CardHeader>
                        <CardTitle>Document Checklist</CardTitle>
                        <p className="text-sm text-slate-600">Track your required documents and their status</p>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {[
                            {
                              name: "Form I-485 (Application for Adjustment of Status)",
                              status: "completed",
                              required: true,
                            },
                            { name: "Form I-765 (Work Authorization)", status: "completed", required: true },
                            { name: "Birth Certificate", status: "completed", required: true },
                            { name: "Marriage Certificate", status: "pending", required: true },
                            { name: "Medical Examination (Form I-693)", status: "missing", required: true },
                            { name: "Tax Returns (Last 3 years)", status: "completed", required: false },
                          ].map((doc, index) => (
                            <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                              <div className="flex items-center gap-3">
                                {doc.status === "completed" && <CheckCircle className="h-5 w-5 text-green-600" />}
                                {doc.status === "pending" && <Clock className="h-5 w-5 text-yellow-600" />}
                                {doc.status === "missing" && <AlertCircle className="h-5 w-5 text-red-600" />}
                                <div>
                                  <div className="font-medium">{doc.name}</div>
                                  {doc.required && <div className="text-xs text-red-600">Required</div>}
                                </div>
                              </div>
                              <Button variant="outline" size="sm">
                                {doc.status === "completed" ? "View" : "Upload"}
                              </Button>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="timeline" className="space-y-6">
                    <Card>
                      <CardHeader>
                        <CardTitle>Case Timeline</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-6">
                          {[
                            { date: "Feb 15, 2024", title: "Forms I-485 and I-765 Submitted", status: "completed" },
                            { date: "Feb 20, 2024", title: "Receipt Notices Received", status: "completed" },
                            { date: "Mar 1, 2024", title: "Biometrics Appointment Scheduled", status: "completed" },
                            { date: "Mar 15, 2024", title: "Biometrics Appointment", status: "upcoming" },
                            { date: "TBD", title: "Interview Scheduled", status: "pending" },
                          ].map((event, index) => (
                            <div key={index} className="flex gap-4">
                              <div className="flex flex-col items-center">
                                <div
                                  className={`w-3 h-3 rounded-full ${
                                    event.status === "completed"
                                      ? "bg-green-600"
                                      : event.status === "upcoming"
                                        ? "bg-blue-600"
                                        : "bg-slate-300"
                                  }`}
                                />
                                {index < 4 && <div className="w-px h-8 bg-slate-200 mt-2" />}
                              </div>
                              <div className="flex-1 pb-8">
                                <div className="font-medium">{event.title}</div>
                                <div className="text-sm text-slate-600">{event.date}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="resources" className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Helpful Resources</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <Button variant="ghost" className="w-full justify-start" asChild>
                            <Link href="#">
                              <FileText className="h-4 w-4 mr-2" />
                              USCIS Processing Times
                            </Link>
                          </Button>
                          <Button variant="ghost" className="w-full justify-start" asChild>
                            <Link href="#">
                              <ExternalLink className="h-4 w-4 mr-2" />
                              Check Case Status Online
                            </Link>
                          </Button>
                          <Button variant="ghost" className="w-full justify-start" asChild>
                            <Link href="#">
                              <BookOpen className="h-4 w-4 mr-2" />
                              Immigration FAQ
                            </Link>
                          </Button>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Need Help?</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <Button className="w-full" asChild>
                            <Link href="/app/qa">
                              <MessageSquare className="h-4 w-4 mr-2" />
                              Ask Legal Question
                            </Link>
                          </Button>
                          <Button variant="outline" className="w-full bg-transparent" asChild>
                            <Link href="/contact">
                              <Phone className="h-4 w-4 mr-2" />
                              Contact Support
                            </Link>
                          </Button>
                        </CardContent>
                      </Card>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            ) : (
              <Card>
                <CardContent className="text-center py-12">
                  <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-slate-900 mb-2">No Immigration Cases</h3>
                  <p className="text-slate-600 mb-4">Start your immigration journey by creating a new case.</p>
                  <Button asChild>
                    <Link href="/immigration/intake">Start Immigration Case</Link>
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
