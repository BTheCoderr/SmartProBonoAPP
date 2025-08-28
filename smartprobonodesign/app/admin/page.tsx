"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { mockData } from "@/lib/mock-data"
import {
  Users,
  FileText,
  TrendingUp,
  AlertCircle,
  Clock,
  CheckCircle,
  BarChart3,
  Settings,
  Shield,
  Database,
  Activity,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Link from "next/link"

export default function AdminDashboard() {
  const { user } = useAuth()
  const [timeRange, setTimeRange] = useState("30d")

  // Mock admin statistics
  const stats = {
    totalUsers: 1247,
    totalCases: 89,
    activeCases: 34,
    completedCases: 55,
    totalAttorneys: 156,
    activeAttorneys: 89,
    totalHours: 2340,
    avgResponseTime: "2.4h",
  }

  const recentActivity = [
    { type: "case", action: "New case created", user: "Maria Rodriguez", time: "5 minutes ago" },
    { type: "attorney", action: "Attorney joined", user: "Dr. James Wilson", time: "12 minutes ago" },
    { type: "case", action: "Case completed", user: "Sarah Chen", time: "1 hour ago" },
    { type: "user", action: "New user registered", user: "Michael Brown", time: "2 hours ago" },
    { type: "case", action: "Case accepted", user: "Attorney Lisa Park", time: "3 hours ago" },
  ]

  const systemHealth = {
    uptime: "99.9%",
    responseTime: "145ms",
    errorRate: "0.02%",
    activeConnections: 234,
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Admin Dashboard</h1>
              <p className="text-slate-600 mt-1">Platform overview and management</p>
            </div>
            <div className="flex items-center gap-3">
              <Select value={timeRange} onValueChange={setTimeRange}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                  <SelectItem value="1y">Last year</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline" asChild>
                <Link href="/admin/settings">
                  <Settings className="h-4 w-4 mr-2" />
                  Settings
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="cases">Cases</TabsTrigger>
            <TabsTrigger value="content">Content</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="system">System</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Total Users</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.totalUsers.toLocaleString()}</p>
                      <p className="text-xs text-green-600 mt-1">+12% from last month</p>
                    </div>
                    <Users className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Active Cases</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.activeCases}</p>
                      <p className="text-xs text-green-600 mt-1">+8% from last month</p>
                    </div>
                    <FileText className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Active Attorneys</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.activeAttorneys}</p>
                      <p className="text-xs text-green-600 mt-1">+15% from last month</p>
                    </div>
                    <Shield className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-600">Pro Bono Hours</p>
                      <p className="text-2xl font-bold text-slate-900">{stats.totalHours.toLocaleString()}</p>
                      <p className="text-xs text-green-600 mt-1">+23% from last month</p>
                    </div>
                    <Clock className="h-8 w-8 text-yellow-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Charts and Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Case Status Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-green-500 rounded-full" />
                        <span className="text-sm">Completed</span>
                      </div>
                      <span className="font-medium">{stats.completedCases}</span>
                    </div>
                    <Progress value={(stats.completedCases / stats.totalCases) * 100} className="h-2" />

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-blue-500 rounded-full" />
                        <span className="text-sm">Active</span>
                      </div>
                      <span className="font-medium">{stats.activeCases}</span>
                    </div>
                    <Progress value={(stats.activeCases / stats.totalCases) * 100} className="h-2" />

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                        <span className="text-sm">Pending</span>
                      </div>
                      <span className="font-medium">{stats.totalCases - stats.activeCases - stats.completedCases}</span>
                    </div>
                    <Progress
                      value={((stats.totalCases - stats.activeCases - stats.completedCases) / stats.totalCases) * 100}
                      className="h-2"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity, index) => (
                      <div key={index} className="flex items-center gap-3">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.type === "case"
                              ? "bg-blue-500"
                              : activity.type === "attorney"
                                ? "bg-purple-500"
                                : "bg-green-500"
                          }`}
                        />
                        <div className="flex-1">
                          <div className="text-sm font-medium">{activity.action}</div>
                          <div className="text-xs text-slate-500">{activity.user}</div>
                        </div>
                        <div className="text-xs text-slate-400">{activity.time}</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* System Health */}
            <Card>
              <CardHeader>
                <CardTitle>System Health</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{systemHealth.uptime}</div>
                    <div className="text-sm text-slate-600">Uptime</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{systemHealth.responseTime}</div>
                    <div className="text-sm text-slate-600">Avg Response Time</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{systemHealth.errorRate}</div>
                    <div className="text-sm text-slate-600">Error Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{systemHealth.activeConnections}</div>
                    <div className="text-sm text-slate-600">Active Connections</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="users" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">User Management</h2>
              <Button asChild>
                <Link href="/admin/users/new">Add User</Link>
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <Card>
                <CardContent className="p-6 text-center">
                  <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.totalUsers}</div>
                  <div className="text-sm text-slate-600">Total Users</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Shield className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.totalAttorneys}</div>
                  <div className="text-sm text-slate-600">Attorneys</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.totalUsers - stats.totalAttorneys}</div>
                  <div className="text-sm text-slate-600">Clients</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Users</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockData.users.slice(0, 5).map((user) => (
                    <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center">
                          <Users className="h-5 w-5 text-slate-600" />
                        </div>
                        <div>
                          <div className="font-medium">{user.name}</div>
                          <div className="text-sm text-slate-600">{user.email}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={user.role === "Attorney" ? "default" : "secondary"}>{user.role}</Badge>
                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/admin/users/${user.id}`}>View</Link>
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="cases" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Case Management</h2>
              <Button variant="outline" asChild>
                <Link href="/admin/cases/export">Export Cases</Link>
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              <Card>
                <CardContent className="p-6 text-center">
                  <FileText className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.totalCases}</div>
                  <div className="text-sm text-slate-600">Total Cases</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Activity className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.activeCases}</div>
                  <div className="text-sm text-slate-600">Active Cases</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.completedCases}</div>
                  <div className="text-sm text-slate-600">Completed</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Clock className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{stats.avgResponseTime}</div>
                  <div className="text-sm text-slate-600">Avg Response</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Cases</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockData.cases.slice(0, 5).map((case_) => (
                    <div key={case_.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">{case_.title}</div>
                        <div className="text-sm text-slate-600">{case_.category}</div>
                        <div className="text-xs text-slate-500 mt-1">
                          Created {new Date(case_.createdAt).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge
                          variant={
                            case_.status === "Active"
                              ? "default"
                              : case_.status === "Completed"
                                ? "secondary"
                                : "outline"
                          }
                        >
                          {case_.status}
                        </Badge>
                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/admin/cases/${case_.id}`}>View</Link>
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="content" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Content Management</h2>
              <Button asChild>
                <Link href="/admin/content/new">Add Content</Link>
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Resources Library</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span>Legal Forms</span>
                    <Badge variant="secondary">24 items</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>FAQ Articles</span>
                    <Badge variant="secondary">18 items</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Legal Guides</span>
                    <Badge variant="secondary">12 items</Badge>
                  </div>
                  <Button variant="outline" className="w-full mt-4 bg-transparent" asChild>
                    <Link href="/admin/content/resources">Manage Resources</Link>
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>System Pages</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span>Terms of Service</span>
                    <Badge variant="outline">Updated 2 days ago</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Privacy Policy</span>
                    <Badge variant="outline">Updated 1 week ago</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>About Page</span>
                    <Badge variant="outline">Updated 2 weeks ago</Badge>
                  </div>
                  <Button variant="outline" className="w-full mt-4 bg-transparent" asChild>
                    <Link href="/admin/content/pages">Manage Pages</Link>
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Analytics & Reports</h2>
              <Button variant="outline" asChild>
                <Link href="/admin/analytics/export">Export Report</Link>
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardContent className="p-6 text-center">
                  <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">+23%</div>
                  <div className="text-sm text-slate-600">User Growth</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <BarChart3 className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">87%</div>
                  <div className="text-sm text-slate-600">Case Success Rate</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Clock className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">4.2</div>
                  <div className="text-sm text-slate-600">Avg Days to Match</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Users className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold">92%</div>
                  <div className="text-sm text-slate-600">Attorney Satisfaction</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Platform Usage Trends</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-slate-500">
                  <BarChart3 className="h-16 w-16 mb-4" />
                  <div className="text-center">
                    <div className="font-medium">Analytics Chart</div>
                    <div className="text-sm">Interactive charts would be displayed here</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="system" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">System Management</h2>
              <Button variant="outline" asChild>
                <Link href="/admin/system/logs">View Logs</Link>
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>System Status</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Database</span>
                    </div>
                    <Badge variant="secondary">Healthy</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>API Services</span>
                    </div>
                    <Badge variant="secondary">Operational</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Email Service</span>
                    </div>
                    <Badge variant="secondary">Operational</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="h-4 w-4 text-yellow-600" />
                      <span>File Storage</span>
                    </div>
                    <Badge variant="outline">Degraded</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Alerts</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                    <AlertCircle className="h-4 w-4 text-yellow-600" />
                    <div>
                      <div className="font-medium text-sm">High Memory Usage</div>
                      <div className="text-xs text-slate-500">2 hours ago</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                    <Database className="h-4 w-4 text-blue-600" />
                    <div>
                      <div className="font-medium text-sm">Database Backup Completed</div>
                      <div className="text-xs text-slate-500">6 hours ago</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <div>
                      <div className="font-medium text-sm">System Update Applied</div>
                      <div className="text-xs text-slate-500">1 day ago</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
