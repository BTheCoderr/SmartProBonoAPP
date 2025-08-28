"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { useAuth } from "@/lib/auth-context"
import { mockCases, mockDocuments, mockEvents } from "@/lib/mock-data"
import { FileText, MessageSquare, Calendar, Search, Plus, Clock, CheckCircle, Scale } from "lucide-react"

export default function AppDashboard() {
  const { user } = useAuth()

  if (!user) {
    return <div>Please log in to access the dashboard.</div>
  }

  const userCases = mockCases.filter((c) => c.clientId === user.id || c.attorneyId === user.id)
  const recentDocuments = mockDocuments.slice(0, 3)
  const upcomingEvents = mockEvents.filter((e) => new Date(e.date) > new Date()).slice(0, 3)

  const caseStats = {
    active: userCases.filter((c) => c.status === "active").length,
    pending: userCases.filter((c) => c.status === "pending").length,
    completed: userCases.filter((c) => c.status === "completed").length,
  }

  return (
    <div className="container py-8 space-y-8">
      {/* Welcome Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Welcome back, {user.name}</h1>
        <p className="text-muted-foreground">Here's what's happening with your legal matters today.</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Button asChild className="h-auto p-6 flex-col space-y-2">
          <Link href="/get-help">
            <Plus className="h-8 w-8" />
            <span>Get Help</span>
          </Link>
        </Button>
        <Button variant="outline" asChild className="h-auto p-6 flex-col space-y-2 bg-transparent">
          <Link href="/app/qa">
            <MessageSquare className="h-8 w-8" />
            <span>Ask Legal Question</span>
          </Link>
        </Button>
        <Button variant="outline" asChild className="h-auto p-6 flex-col space-y-2 bg-transparent">
          <Link href="/app/documents">
            <FileText className="h-8 w-8" />
            <span>Upload Document</span>
          </Link>
        </Button>
        <Button variant="outline" asChild className="h-auto p-6 flex-col space-y-2 bg-transparent">
          <Link href="/app/search">
            <Search className="h-8 w-8" />
            <span>Search Cases</span>
          </Link>
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Cases</CardTitle>
            <Scale className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{caseStats.active}</div>
            <p className="text-xs text-muted-foreground">Cases in progress</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Review</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{caseStats.pending}</div>
            <p className="text-xs text-muted-foreground">Awaiting attorney review</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{caseStats.completed}</div>
            <p className="text-xs text-muted-foreground">Successfully resolved</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Cases */}
        <Card>
          <CardHeader>
            <CardTitle>Your Cases</CardTitle>
            <CardDescription>Recent legal matters and their status</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {userCases.length > 0 ? (
              userCases.slice(0, 3).map((case_) => (
                <div key={case_.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="space-y-1">
                    <h4 className="font-medium">{case_.title}</h4>
                    <p className="text-sm text-muted-foreground">{case_.category}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge
                      variant={
                        case_.status === "active" ? "default" : case_.status === "pending" ? "secondary" : "outline"
                      }
                    >
                      {case_.status}
                    </Badge>
                    <Button variant="ghost" size="sm" asChild>
                      <Link href={`/app/cases/${case_.id}`}>View</Link>
                    </Button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <Scale className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-medium mb-2">No cases yet</h3>
                <p className="text-sm text-muted-foreground mb-4">Get started by requesting legal help</p>
                <Button asChild>
                  <Link href="/get-help">Get Help Now</Link>
                </Button>
              </div>
            )}
            {userCases.length > 3 && (
              <Button variant="outline" className="w-full bg-transparent" asChild>
                <Link href="/app/cases">View All Cases</Link>
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Recent Documents */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Documents</CardTitle>
            <CardDescription>Recently uploaded and shared files</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentDocuments.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-muted-foreground" />
                  <div className="space-y-1">
                    <h4 className="font-medium text-sm">{doc.name}</h4>
                    <p className="text-xs text-muted-foreground">{new Date(doc.createdAt).toLocaleDateString()}</p>
                  </div>
                </div>
                <Badge variant={doc.status === "approved" ? "default" : "secondary"}>{doc.status}</Badge>
              </div>
            ))}
            <Button variant="outline" className="w-full bg-transparent" asChild>
              <Link href="/app/documents">View All Documents</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Upcoming Events */}
      {upcomingEvents.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Upcoming Events</CardTitle>
            <CardDescription>Important dates and deadlines</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {upcomingEvents.map((event) => (
                <div key={event.id} className="flex items-center gap-4 p-4 border rounded-lg">
                  <Calendar className="h-5 w-5 text-primary" />
                  <div className="flex-1">
                    <h4 className="font-medium">{event.title}</h4>
                    <p className="text-sm text-muted-foreground">{event.description}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">{new Date(event.date).toLocaleDateString()}</p>
                    <p className="text-xs text-muted-foreground">{new Date(event.date).toLocaleTimeString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
