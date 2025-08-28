"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"
import { ArrowLeft, User, Star, Award, Settings, Save } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"

export default function AttorneyProfile() {
  const { user } = useAuth()
  const router = useRouter()
  const { toast } = useToast()

  const [profile, setProfile] = useState({
    name: user?.name || "",
    email: user?.email || "",
    phone: "+1 (555) 123-4567",
    location: "San Francisco, CA",
    barNumber: "CA123456",
    yearsExperience: "8",
    specialties: ["Immigration Law", "Family Law"],
    bio: "Experienced attorney passionate about providing pro bono legal services to underserved communities.",
    availability: "part-time",
    maxCases: "3",
    languages: ["English", "Spanish"],
    organization: "Bay Area Legal Aid",
  })

  const handleSave = () => {
    toast({
      title: "Profile updated",
      description: "Your attorney profile has been successfully updated.",
    })
  }

  const updateProfile = (field: string, value: any) => {
    setProfile((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => router.back()}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Attorney Profile</h1>
              <p className="text-slate-600 mt-1">Manage your professional information and availability</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Tabs defaultValue="profile" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="profile">Profile</TabsTrigger>
              <TabsTrigger value="availability">Availability</TabsTrigger>
              <TabsTrigger value="achievements">Achievements</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="profile" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Basic Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input id="name" value={profile.name} onChange={(e) => updateProfile("name", e.target.value)} />
                    </div>
                    <div>
                      <Label htmlFor="email">Email Address</Label>
                      <Input
                        id="email"
                        type="email"
                        value={profile.email}
                        onChange={(e) => updateProfile("email", e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="phone">Phone Number</Label>
                      <Input
                        id="phone"
                        value={profile.phone}
                        onChange={(e) => updateProfile("phone", e.target.value)}
                      />
                    </div>
                    <div>
                      <Label htmlFor="location">Location</Label>
                      <Input
                        id="location"
                        value={profile.location}
                        onChange={(e) => updateProfile("location", e.target.value)}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Professional Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="barNumber">Bar Number</Label>
                      <Input
                        id="barNumber"
                        value={profile.barNumber}
                        onChange={(e) => updateProfile("barNumber", e.target.value)}
                      />
                    </div>
                    <div>
                      <Label htmlFor="yearsExperience">Years of Experience</Label>
                      <Input
                        id="yearsExperience"
                        type="number"
                        value={profile.yearsExperience}
                        onChange={(e) => updateProfile("yearsExperience", e.target.value)}
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="organization">Organization/Firm</Label>
                    <Input
                      id="organization"
                      value={profile.organization}
                      onChange={(e) => updateProfile("organization", e.target.value)}
                    />
                  </div>
                  <div>
                    <Label htmlFor="bio">Professional Bio</Label>
                    <Textarea
                      id="bio"
                      value={profile.bio}
                      onChange={(e) => updateProfile("bio", e.target.value)}
                      rows={4}
                      placeholder="Tell clients about your experience and passion for pro bono work..."
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Specialties & Languages</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>Legal Specialties</Label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {profile.specialties.map((specialty) => (
                        <Badge key={specialty} variant="secondary">
                          {specialty}
                        </Badge>
                      ))}
                      <Button variant="outline" size="sm">
                        Add Specialty
                      </Button>
                    </div>
                  </div>
                  <div>
                    <Label>Languages</Label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {profile.languages.map((language) => (
                        <Badge key={language} variant="outline">
                          {language}
                        </Badge>
                      ))}
                      <Button variant="outline" size="sm">
                        Add Language
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button onClick={handleSave}>
                  <Save className="h-4 w-4 mr-2" />
                  Save Profile
                </Button>
              </div>
            </TabsContent>

            <TabsContent value="availability" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Availability Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="availability">Availability Status</Label>
                    <Select
                      value={profile.availability}
                      onValueChange={(value) => updateProfile("availability", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="full-time">Full-time (40+ hours/week)</SelectItem>
                        <SelectItem value="part-time">Part-time (10-20 hours/week)</SelectItem>
                        <SelectItem value="limited">Limited (5-10 hours/week)</SelectItem>
                        <SelectItem value="unavailable">Currently Unavailable</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="maxCases">Maximum Active Cases</Label>
                    <Input
                      id="maxCases"
                      type="number"
                      value={profile.maxCases}
                      onChange={(e) => updateProfile("maxCases", e.target.value)}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Case Preferences</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>Preferred Case Types</Label>
                    <div className="space-y-2 mt-2">
                      {["Immigration", "Family Law", "Housing", "Employment", "Benefits", "Criminal Defense"].map(
                        (type) => (
                          <div key={type} className="flex items-center space-x-2">
                            <Checkbox id={type} />
                            <Label htmlFor={type}>{type}</Label>
                          </div>
                        ),
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button onClick={handleSave}>
                  <Save className="h-4 w-4 mr-2" />
                  Save Availability
                </Button>
              </div>
            </TabsContent>

            <TabsContent value="achievements" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Pro Bono Statistics</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Total Hours</span>
                      <span className="font-bold text-2xl">156</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Cases Completed</span>
                      <span className="font-bold text-2xl">23</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Client Rating</span>
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span className="font-bold">4.9</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Achievements</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                      <Award className="h-6 w-6 text-yellow-600" />
                      <div>
                        <div className="font-medium text-yellow-900">Pro Bono Champion</div>
                        <div className="text-sm text-yellow-700">150+ hours completed</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                      <Star className="h-6 w-6 text-blue-600" />
                      <div>
                        <div className="font-medium text-blue-900">Client Favorite</div>
                        <div className="text-sm text-blue-700">4.8+ average rating</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                      <User className="h-6 w-6 text-green-600" />
                      <div>
                        <div className="font-medium text-green-900">Community Helper</div>
                        <div className="text-sm text-green-700">20+ clients served</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="settings" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Notification Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="emailNotifications" defaultChecked />
                      <Label htmlFor="emailNotifications">Email notifications for new cases</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox id="smsNotifications" />
                      <Label htmlFor="smsNotifications">SMS notifications for urgent cases</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox id="weeklyDigest" defaultChecked />
                      <Label htmlFor="weeklyDigest">Weekly digest of available cases</Label>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Privacy Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="publicProfile" defaultChecked />
                      <Label htmlFor="publicProfile">Make profile visible to clients</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox id="showStats" defaultChecked />
                      <Label htmlFor="showStats">Show pro bono statistics publicly</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox id="allowDirectContact" />
                      <Label htmlFor="allowDirectContact">Allow direct contact from clients</Label>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button onClick={handleSave}>
                  <Settings className="h-4 w-4 mr-2" />
                  Save Settings
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
