"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, ArrowRight, Save, CheckCircle } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

const IMMIGRATION_TYPES = [
  { value: "family", label: "Family-Based Immigration", description: "Spouse, parent, child, or sibling petitions" },
  { value: "employment", label: "Employment-Based Immigration", description: "Work visas and employment petitions" },
  { value: "asylum", label: "Asylum/Refugee Status", description: "Protection from persecution" },
  { value: "adjustment", label: "Adjustment of Status", description: "Green card application while in the US" },
  { value: "naturalization", label: "Naturalization/Citizenship", description: "Becoming a US citizen" },
  { value: "removal", label: "Removal Defense", description: "Defense against deportation proceedings" },
  { value: "other", label: "Other Immigration Matter", description: "Other immigration-related issues" },
]

const STEPS = [
  { id: 1, title: "Immigration Type", description: "What type of immigration help do you need?" },
  { id: 2, title: "Personal Information", description: "Tell us about yourself" },
  { id: 3, title: "Case Details", description: "Provide details about your situation" },
  { id: 4, title: "Documents", description: "What documents do you have?" },
  { id: 5, title: "Review", description: "Review and submit your information" },
]

export default function ImmigrationIntake() {
  const router = useRouter()
  const { toast } = useToast()
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState({
    immigrationType: "",
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    dateOfBirth: "",
    countryOfBirth: "",
    currentStatus: "",
    caseDescription: "",
    urgency: "",
    hasDocuments: false,
    documentTypes: [] as string[],
    previousApplications: false,
    previousApplicationDetails: "",
    familyInUS: false,
    familyDetails: "",
    employmentHistory: "",
    criminalHistory: false,
    criminalDetails: "",
  })

  const updateFormData = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < STEPS.length) {
      setCurrentStep(currentStep + 1)
      // Auto-save progress
      toast({
        title: "Progress saved",
        description: "Your information has been automatically saved.",
      })
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSubmit = () => {
    toast({
      title: "Application submitted!",
      description: "We'll review your information and match you with an attorney.",
    })
    router.push("/app/immigration")
  }

  const progress = (currentStep / STEPS.length) * 100

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
              <h1 className="text-2xl font-bold text-slate-900">Immigration Intake</h1>
              <p className="text-slate-600 mt-1">
                Step {currentStep} of {STEPS.length}: {STEPS[currentStep - 1].title}
              </p>
            </div>
          </div>
          <div className="mt-4">
            <Progress value={progress} className="h-2" />
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>{STEPS[currentStep - 1].title}</CardTitle>
              <p className="text-slate-600">{STEPS[currentStep - 1].description}</p>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Step 1: Immigration Type */}
              {currentStep === 1 && (
                <div className="space-y-4">
                  {IMMIGRATION_TYPES.map((type) => (
                    <div
                      key={type.value}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        formData.immigrationType === type.value
                          ? "border-blue-500 bg-blue-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                      onClick={() => updateFormData("immigrationType", type.value)}
                    >
                      <div className="flex items-start gap-3">
                        <div
                          className={`w-4 h-4 rounded-full border-2 mt-1 ${
                            formData.immigrationType === type.value ? "border-blue-500 bg-blue-500" : "border-slate-300"
                          }`}
                        />
                        <div>
                          <div className="font-medium">{type.label}</div>
                          <div className="text-sm text-slate-600 mt-1">{type.description}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Step 2: Personal Information */}
              {currentStep === 2 && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="firstName">First Name *</Label>
                      <Input
                        id="firstName"
                        value={formData.firstName}
                        onChange={(e) => updateFormData("firstName", e.target.value)}
                        placeholder="Enter your first name"
                      />
                    </div>
                    <div>
                      <Label htmlFor="lastName">Last Name *</Label>
                      <Input
                        id="lastName"
                        value={formData.lastName}
                        onChange={(e) => updateFormData("lastName", e.target.value)}
                        placeholder="Enter your last name"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="email">Email Address *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={(e) => updateFormData("email", e.target.value)}
                      placeholder="Enter your email address"
                    />
                  </div>
                  <div>
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input
                      id="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => updateFormData("phone", e.target.value)}
                      placeholder="Enter your phone number"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="dateOfBirth">Date of Birth *</Label>
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={formData.dateOfBirth}
                        onChange={(e) => updateFormData("dateOfBirth", e.target.value)}
                      />
                    </div>
                    <div>
                      <Label htmlFor="countryOfBirth">Country of Birth *</Label>
                      <Input
                        id="countryOfBirth"
                        value={formData.countryOfBirth}
                        onChange={(e) => updateFormData("countryOfBirth", e.target.value)}
                        placeholder="Enter your country of birth"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="currentStatus">Current Immigration Status</Label>
                    <Select
                      value={formData.currentStatus}
                      onValueChange={(value) => updateFormData("currentStatus", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select your current status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="citizen">US Citizen</SelectItem>
                        <SelectItem value="permanent-resident">Permanent Resident</SelectItem>
                        <SelectItem value="h1b">H-1B</SelectItem>
                        <SelectItem value="f1">F-1 Student</SelectItem>
                        <SelectItem value="tourist">Tourist/B-2</SelectItem>
                        <SelectItem value="asylum-pending">Asylum Pending</SelectItem>
                        <SelectItem value="undocumented">Undocumented</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}

              {/* Step 3: Case Details */}
              {currentStep === 3 && (
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="caseDescription">Describe Your Situation *</Label>
                    <Textarea
                      id="caseDescription"
                      value={formData.caseDescription}
                      onChange={(e) => updateFormData("caseDescription", e.target.value)}
                      placeholder="Please provide details about your immigration situation, what help you need, and any relevant background information..."
                      rows={6}
                    />
                  </div>
                  <div>
                    <Label htmlFor="urgency">How urgent is your case?</Label>
                    <Select value={formData.urgency} onValueChange={(value) => updateFormData("urgency", value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select urgency level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="immediate">Immediate (within days)</SelectItem>
                        <SelectItem value="urgent">Urgent (within weeks)</SelectItem>
                        <SelectItem value="moderate">Moderate (within months)</SelectItem>
                        <SelectItem value="low">Low (no specific timeline)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="previousApplications"
                        checked={formData.previousApplications}
                        onCheckedChange={(checked) => updateFormData("previousApplications", checked)}
                      />
                      <Label htmlFor="previousApplications">I have filed immigration applications before</Label>
                    </div>
                    {formData.previousApplications && (
                      <Textarea
                        value={formData.previousApplicationDetails}
                        onChange={(e) => updateFormData("previousApplicationDetails", e.target.value)}
                        placeholder="Please describe your previous applications, their outcomes, and any relevant details..."
                        rows={3}
                      />
                    )}
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="familyInUS"
                        checked={formData.familyInUS}
                        onCheckedChange={(checked) => updateFormData("familyInUS", checked)}
                      />
                      <Label htmlFor="familyInUS">I have family members in the US</Label>
                    </div>
                    {formData.familyInUS && (
                      <Textarea
                        value={formData.familyDetails}
                        onChange={(e) => updateFormData("familyDetails", e.target.value)}
                        placeholder="Please describe your family members in the US, their status, and relationship to you..."
                        rows={3}
                      />
                    )}
                  </div>
                </div>
              )}

              {/* Step 4: Documents */}
              {currentStep === 4 && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="hasDocuments"
                      checked={formData.hasDocuments}
                      onCheckedChange={(checked) => updateFormData("hasDocuments", checked)}
                    />
                    <Label htmlFor="hasDocuments">I have relevant documents for my case</Label>
                  </div>

                  {formData.hasDocuments && (
                    <div className="space-y-3">
                      <Label>What types of documents do you have? (Check all that apply)</Label>
                      {[
                        "Passport",
                        "Birth Certificate",
                        "Marriage Certificate",
                        "Divorce Decree",
                        "Educational Transcripts",
                        "Employment Authorization Document",
                        "I-94 Arrival/Departure Record",
                        "Previous Immigration Forms",
                        "Court Documents",
                        "Medical Records",
                        "Police Certificates",
                        "Tax Returns",
                        "Other",
                      ].map((docType) => (
                        <div key={docType} className="flex items-center space-x-2">
                          <Checkbox
                            id={docType}
                            checked={formData.documentTypes.includes(docType)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                updateFormData("documentTypes", [...formData.documentTypes, docType])
                              } else {
                                updateFormData(
                                  "documentTypes",
                                  formData.documentTypes.filter((t) => t !== docType),
                                )
                              }
                            }}
                          />
                          <Label htmlFor={docType}>{docType}</Label>
                        </div>
                      ))}
                    </div>
                  )}

                  <div>
                    <Label htmlFor="employmentHistory">Employment History (if relevant)</Label>
                    <Textarea
                      id="employmentHistory"
                      value={formData.employmentHistory}
                      onChange={(e) => updateFormData("employmentHistory", e.target.value)}
                      placeholder="Please describe your employment history, especially if relevant to your immigration case..."
                      rows={4}
                    />
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="criminalHistory"
                        checked={formData.criminalHistory}
                        onCheckedChange={(checked) => updateFormData("criminalHistory", checked)}
                      />
                      <Label htmlFor="criminalHistory">I have been arrested or convicted of a crime</Label>
                    </div>
                    {formData.criminalHistory && (
                      <Textarea
                        value={formData.criminalDetails}
                        onChange={(e) => updateFormData("criminalDetails", e.target.value)}
                        placeholder="Please provide details about any arrests or convictions. This information is confidential and helps us provide better assistance..."
                        rows={3}
                      />
                    )}
                  </div>
                </div>
              )}

              {/* Step 5: Review */}
              {currentStep === 5 && (
                <div className="space-y-6">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span className="font-medium text-green-900">Ready to Submit</span>
                    </div>
                    <p className="text-green-800 text-sm">
                      Please review your information below. Once submitted, we'll match you with a qualified immigration
                      attorney.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <h3 className="font-medium text-slate-900 mb-2">Immigration Type</h3>
                      <p className="text-slate-600">
                        {IMMIGRATION_TYPES.find((t) => t.value === formData.immigrationType)?.label}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-medium text-slate-900 mb-2">Personal Information</h3>
                      <div className="text-slate-600 space-y-1">
                        <p>
                          {formData.firstName} {formData.lastName}
                        </p>
                        <p>{formData.email}</p>
                        {formData.phone && <p>{formData.phone}</p>}
                        <p>
                          Born: {formData.dateOfBirth} in {formData.countryOfBirth}
                        </p>
                        {formData.currentStatus && <p>Current Status: {formData.currentStatus}</p>}
                      </div>
                    </div>

                    <div>
                      <h3 className="font-medium text-slate-900 mb-2">Case Description</h3>
                      <p className="text-slate-600">{formData.caseDescription}</p>
                    </div>

                    {formData.urgency && (
                      <div>
                        <h3 className="font-medium text-slate-900 mb-2">Urgency</h3>
                        <p className="text-slate-600">{formData.urgency}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Navigation */}
              <div className="flex justify-between pt-6 border-t">
                <Button variant="outline" onClick={prevStep} disabled={currentStep === 1}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Previous
                </Button>

                <div className="flex gap-2">
                  <Button variant="outline">
                    <Save className="h-4 w-4 mr-2" />
                    Save Draft
                  </Button>

                  {currentStep === STEPS.length ? (
                    <Button onClick={handleSubmit}>Submit Application</Button>
                  ) : (
                    <Button
                      onClick={nextStep}
                      disabled={
                        (currentStep === 1 && !formData.immigrationType) ||
                        (currentStep === 2 && (!formData.firstName || !formData.lastName || !formData.email))
                      }
                    >
                      Next
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
