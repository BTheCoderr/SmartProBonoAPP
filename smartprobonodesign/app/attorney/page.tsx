"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { mockData } from "@/lib/mock-data"
import {
  Users,
  Clock,
  FileText,
  Calendar,
  TrendingUp,
  MessageSquare,
  Star,
  Search,
  Plus,
  AlertCircle,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Link from "next/link"

export default function AttorneyDashboard() {
  const { user } = useAuth()
  const [searchQuery, setSearchQuery] = useState("")
  const [filterCategory, setFilterCategory] = useState("all")
  const [filterUrgency, setFilterUrgency] = useState("all")

  // Mock attorney stats
  const stats = {
    activeCases: 8,
    totalHours: 156,
    clientsSaved: 23,
    avgRating: 4.9,
  }

  // Filter available cases
  const availableCases = mockData.cases.filter((case_) => {
    const matchesSearch =
      case_.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      case_.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = filterCategory === "all" || case_.category.toLowerCase() === filterCategory
    const matchesUrgency = filterUrgency === "all" || case_.priority?.toLowerCase() === filterUrgency
    return matchesSearch && matchesCategory && matchesUrgency && case_.status === "Open"
  })

  const myCases = mockData.cases.filter((case_) => case_.status === "Active")

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Attorney Portal</h1>
              <p className="text-slate-600 mt-1">Welcome back, {user?.name}</p>
            </div>
            <div className="flex gap-3">
              <Button variant="outline" asChild>
                <Link href="/attorney/profile">
                  <Users className="h-4 w-4 mr-2" />
                  Profile
                </Link>
              </Button>
              <Button asChild>
                <Link href="/attorney/cases/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Take Case
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="available">Available Cases</TabsTrigger>
            <TabsTrigger value="my-cases">My Cases</TabsTrigger>
            <TabsTrigger value="resources">Resources</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Active Cases</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.activeCases}</p>
                    </div>
                    <FileText className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Pro Bono Hours</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.totalHours}</p>
                    </div>
                    <Clock className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Clients Helped</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.clientsSaved}</p>
                    </div>
                    <Users className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Average Rating</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.avgRating}</p>
                    </div>
                    <Star className="h-8 w-8 text-yellow-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Cases</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {myCases.slice(0, 3).map((case_) => (
                      <div key={case_.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                        <div>
                          <div className="font-medium text-sm">{case_.title}</div>
                          <div className="text-xs text-slate-500">{case_.category}</div>
                        </div>
                        <Badge variant="secondary">{case_.status}</Badge>
                      </div>
                    ))}
                  </div>
                  <Button variant="ghost" className="w-full mt-4" asChild>
                    <Link href="/attorney?tab=my-cases">View All Cases</Link>
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Upcoming Deadlines</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
                      <AlertCircle className="h-4 w-4 text-red-600" />
                      <div>
                        <div className="font-medium text-sm">Immigration Form Due</div>
                        <div className="text-xs text-slate-500">Tomorrow, 5:00 PM</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                      <Calendar className="h-4 w-4 text-yellow-600" />
                      <div>
                        <div className="font-medium text-sm">Client Meeting</div>
                        <div className="text-xs text-slate-500">March 15, 2:00 PM</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                      <FileText className="h-4 w-4 text-blue-600" />
                      <div>
                        <div className="font-medium text-sm">Document Review</div>
                        <div className="text-xs text-slate-500">March 18, 10:00 AM</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="available" className="space-y-6">
            {/* Filters */}
            <Card>
              <CardContent className="p-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                      <Input
                        placeholder="Search cases..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <Select value={filterCategory} onValueChange={setFilterCategory}>
                    <SelectTrigger className="w-full md:w-48">
                      <SelectValue placeholder="Category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Categories</SelectItem>
                      <SelectItem value="immigration">Immigration</SelectItem>
                      <SelectItem value="family">Family Law</SelectItem>
                      <SelectItem value="housing">Housing</SelectItem>
                      <SelectItem value="employment">Employment</SelectItem>
                      <SelectItem value="benefits">Benefits</SelectItem>
                    </SelectContent>
                  </Select>
                  <Select value={filterUrgency} onValueChange={setFilterUrgency}>
                    <SelectTrigger className="w-full md:w-48">
                      <SelectValue placeholder="Urgency" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Urgency</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="low">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* Available Cases */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {availableCases.map((case_) => (
                <Card key={case_.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{case_.title}</CardTitle>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge variant="outline">{case_.category}</Badge>
                          {case_.priority && (
                            <Badge
                              variant={
                                case_.priority === "High"
                                  ? "destructive"
                                  : case_.priority === "Medium"
                                    ? "default"
                                    : "secondary"
                              }
                            >
                              {case_.priority} Priority
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 text-sm mb-4">{case_.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="text-xs text-slate-500">
                        Posted {new Date(case_.createdAt).toLocaleDateString()}
                      </div>
                      <Button size="sm" asChild>
                        <Link href={`/attorney/cases/${case_.id}`}>View Details</Link>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {availableCases.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-slate-900 mb-2">No Cases Found</h3>
                  <p className="text-slate-600">
                    Try adjusting your search criteria or check back later for new cases.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="my-cases" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {myCases.map((case_) => (
                <Card key={case_.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{case_.title}</CardTitle>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge variant="outline">{case_.category}</Badge>
                          <Badge variant="default">{case_.status}</Badge>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 text-sm mb-4">{case_.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="text-xs text-slate-500">
                        Last updated {new Date(case_.updatedAt).toLocaleDateString()}
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/attorney/cases/${case_.id}/messages`}>
                            <MessageSquare className="h-4 w-4 mr-1" />
                            Message
                          </Link>
                        </Button>
                        <Button size="sm" asChild>
                          <Link href={`/attorney/cases/${case_.id}`}>Manage</Link>
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {myCases.length === 0 && (
              <Card>
                <CardContent className="text-center py-12">
                  <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-slate-900 mb-2">No Active Cases</h3>
                  <p className="text-slate-600 mb-4">
                    You don't have any active cases yet. Browse available cases to get started.
                  </p>
                  <Button asChild>
                    <Link href="/attorney?tab=available">Browse Available Cases</Link>
                  </Button>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="resources" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Legal Resources</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/resources">
                      <FileText className="h-4 w-4 mr-2" />
                      Legal Forms Library
                    </Link>
                  </Button>
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/resources">
                      <FileText className="h-4 w-4 mr-2" />
                      Case Law Database
                    </Link>
                  </Button>
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/resources">
                      <FileText className="h-4 w-4 mr-2" />
                      Practice Guides
                    </Link>
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Training & Support</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/training">
                      <TrendingUp className="h-4 w-4 mr-2" />
                      Pro Bono Training
                    </Link>
                  </Button>
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/training">
                      <MessageSquare className="h-4 w-4 mr-2" />
                      Attorney Forums
                    </Link>
                  </Button>
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/contact">
                      <Users className="h-4 w-4 mr-2" />
                      Contact Support
                    </Link>
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Recognition</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-center p-4 bg-yellow-50 rounded-lg">
                    <Star className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                    <div className="font-medium text-yellow-900">Pro Bono Champion</div>
                    <div className="text-sm text-yellow-700">150+ hours completed</div>
                  </div>
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <Link href="/attorney/achievements">
                      <TrendingUp className="h-4 w-4 mr-2" />
                      View All Achievements
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
