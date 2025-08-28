"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Progress } from "@/components/ui/progress"
import { useToast } from "@/hooks/use-toast"
import { ChevronLeft, ChevronRight, Save } from "lucide-react"

const steps = [
  { id: 1, title: "Basic Information", description: "Tell us about yourself" },
  { id: 2, title: "Legal Issue", description: "Describe your legal matter" },
  { id: 3, title: "Details", description: "Additional information" },
  { id: 4, title: "Review", description: "Review and submit" },
]

const step1Schema = z.object({
  firstName: z.string().min(2, "First name is required"),
  lastName: z.string().min(2, "Last name is required"),
  email: z.string().email("Valid email is required"),
  phone: z.string().min(10, "Phone number is required"),
  address: z.string().min(5, "Address is required"),
  city: z.string().min(2, "City is required"),
  state: z.string().min(2, "State is required"),
  zipCode: z.string().min(5, "ZIP code is required"),
})

const step2Schema = z.object({
  legalCategory: z.string().min(1, "Please select a legal category"),
  issueTitle: z.string().min(10, "Please provide a brief title (at least 10 characters)"),
  issueDescription: z.string().min(50, "Please provide more details (at least 50 characters)"),
  urgency: z.enum(["low", "medium", "high", "urgent"]),
  hasDeadline: z.boolean(),
  deadline: z.string().optional(),
})

const step3Schema = z.object({
  previousLegalHelp: z.boolean(),
  previousHelpDetails: z.string().optional(),
  documentsAvailable: z.boolean(),
  documentTypes: z.array(z.string()).optional(),
  additionalInfo: z.string().optional(),
  incomeQualification: z.enum(["under_25k", "25k_50k", "50k_75k", "over_75k"]),
  householdSize: z.string().min(1, "Household size is required"),
})

type Step1Form = z.infer<typeof step1Schema>
type Step2Form = z.infer<typeof step2Schema>
type Step3Form = z.infer<typeof step3Schema>

export default function GetHelpPage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<any>({})
  const [isSaving, setIsSaving] = useState(false)
  const { toast } = useToast()
  const router = useRouter()

  const step1Form = useForm<Step1Form>({
    resolver: zodResolver(step1Schema),
    defaultValues: formData.step1 || {},
  })

  const step2Form = useForm<Step2Form>({
    resolver: zodResolver(step2Schema),
    defaultValues: formData.step2 || {},
  })

  const step3Form = useForm<Step3Form>({
    resolver: zodResolver(step3Schema),
    defaultValues: formData.step3 || {},
  })

  const saveProgress = async (stepData: any, stepNumber: number) => {
    setIsSaving(true)
    // Simulate autosave
    await new Promise((resolve) => setTimeout(resolve, 500))
    setFormData((prev: any) => ({ ...prev, [`step${stepNumber}`]: stepData }))
    setIsSaving(false)
  }

  const handleNext = async () => {
    let isValid = false
    let stepData = {}

    switch (currentStep) {
      case 1:
        isValid = await step1Form.trigger()
        if (isValid) {
          stepData = step1Form.getValues()
          await saveProgress(stepData, 1)
        }
        break
      case 2:
        isValid = await step2Form.trigger()
        if (isValid) {
          stepData = step2Form.getValues()
          await saveProgress(stepData, 2)
        }
        break
      case 3:
        isValid = await step3Form.trigger()
        if (isValid) {
          stepData = step3Form.getValues()
          await saveProgress(stepData, 3)
        }
        break
    }

    if (isValid) {
      setCurrentStep((prev) => Math.min(prev + 1, steps.length))
    }
  }

  const handlePrevious = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 1))
  }

  const handleSubmit = async () => {
    setIsSaving(true)
    try {
      // Simulate form submission
      await new Promise((resolve) => setTimeout(resolve, 2000))

      toast({
        title: "Application submitted!",
        description: "We'll review your request and match you with an attorney within 3-5 business days.",
      })

      router.push("/app")
    } catch (error) {
      toast({
        title: "Error",
        description: "Something went wrong. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSaving(false)
    }
  }

  const progress = (currentStep / steps.length) * 100

  return (
    <div className="container py-8 max-w-4xl">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold">Get Legal Help</h1>
          <p className="text-muted-foreground">
            Complete this form to get matched with a qualified attorney who can help with your legal matter.
          </p>
        </div>

        {/* Progress */}
        <div className="space-y-4">
          <div className="flex justify-between text-sm">
            <span>
              Step {currentStep} of {steps.length}
            </span>
            <span>{Math.round(progress)}% complete</span>
          </div>
          <Progress value={progress} className="h-2" />
          <div className="flex justify-between">
            {steps.map((step) => (
              <div
                key={step.id}
                className={`text-center ${step.id <= currentStep ? "text-primary" : "text-muted-foreground"}`}
              >
                <div
                  className={`w-8 h-8 rounded-full mx-auto mb-2 flex items-center justify-center text-sm font-medium ${
                    step.id <= currentStep ? "bg-primary text-primary-foreground" : "bg-muted"
                  }`}
                >
                  {step.id}
                </div>
                <div className="text-xs font-medium">{step.title}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Form Content */}
        <Card>
          <CardHeader>
            <CardTitle>{steps[currentStep - 1].title}</CardTitle>
            <CardDescription>{steps[currentStep - 1].description}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {currentStep === 1 && (
              <form className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">First Name</Label>
                    <Input
                      id="firstName"
                      {...step1Form.register("firstName")}
                      className={step1Form.formState.errors.firstName ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.firstName && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.firstName.message}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input
                      id="lastName"
                      {...step1Form.register("lastName")}
                      className={step1Form.formState.errors.lastName ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.lastName && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.lastName.message}</p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      {...step1Form.register("email")}
                      className={step1Form.formState.errors.email ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.email && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.email.message}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone</Label>
                    <Input
                      id="phone"
                      type="tel"
                      {...step1Form.register("phone")}
                      className={step1Form.formState.errors.phone ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.phone && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.phone.message}</p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="address">Address</Label>
                  <Input
                    id="address"
                    {...step1Form.register("address")}
                    className={step1Form.formState.errors.address ? "border-destructive" : ""}
                  />
                  {step1Form.formState.errors.address && (
                    <p className="text-sm text-destructive">{step1Form.formState.errors.address.message}</p>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="city">City</Label>
                    <Input
                      id="city"
                      {...step1Form.register("city")}
                      className={step1Form.formState.errors.city ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.city && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.city.message}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="state">State</Label>
                    <Input
                      id="state"
                      {...step1Form.register("state")}
                      className={step1Form.formState.errors.state ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.state && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.state.message}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="zipCode">ZIP Code</Label>
                    <Input
                      id="zipCode"
                      {...step1Form.register("zipCode")}
                      className={step1Form.formState.errors.zipCode ? "border-destructive" : ""}
                    />
                    {step1Form.formState.errors.zipCode && (
                      <p className="text-sm text-destructive">{step1Form.formState.errors.zipCode.message}</p>
                    )}
                  </div>
                </div>
              </form>
            )}

            {currentStep === 2 && (
              <form className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="legalCategory">Legal Category</Label>
                  <Select onValueChange={(value) => step2Form.setValue("legalCategory", value)}>
                    <SelectTrigger className={step2Form.formState.errors.legalCategory ? "border-destructive" : ""}>
                      <SelectValue placeholder="Select the type of legal issue" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="immigration">Immigration</SelectItem>
                      <SelectItem value="housing">Housing</SelectItem>
                      <SelectItem value="family">Family Law</SelectItem>
                      <SelectItem value="employment">Employment</SelectItem>
                      <SelectItem value="benefits">Benefits</SelectItem>
                      <SelectItem value="consumer">Consumer Rights</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                  {step2Form.formState.errors.legalCategory && (
                    <p className="text-sm text-destructive">{step2Form.formState.errors.legalCategory.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="issueTitle">Brief Title</Label>
                  <Input
                    id="issueTitle"
                    placeholder="Briefly describe your legal issue"
                    {...step2Form.register("issueTitle")}
                    className={step2Form.formState.errors.issueTitle ? "border-destructive" : ""}
                  />
                  {step2Form.formState.errors.issueTitle && (
                    <p className="text-sm text-destructive">{step2Form.formState.errors.issueTitle.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="issueDescription">Detailed Description</Label>
                  <Textarea
                    id="issueDescription"
                    placeholder="Please provide as much detail as possible about your situation..."
                    className={`min-h-[120px] ${step2Form.formState.errors.issueDescription ? "border-destructive" : ""}`}
                    {...step2Form.register("issueDescription")}
                  />
                  {step2Form.formState.errors.issueDescription && (
                    <p className="text-sm text-destructive">{step2Form.formState.errors.issueDescription.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="urgency">Urgency Level</Label>
                  <Select onValueChange={(value) => step2Form.setValue("urgency", value as any)}>
                    <SelectTrigger className={step2Form.formState.errors.urgency ? "border-destructive" : ""}>
                      <SelectValue placeholder="How urgent is this matter?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low - No immediate deadline</SelectItem>
                      <SelectItem value="medium">Medium - Within a few weeks</SelectItem>
                      <SelectItem value="high">High - Within a week</SelectItem>
                      <SelectItem value="urgent">Urgent - Immediate attention needed</SelectItem>
                    </SelectContent>
                  </Select>
                  {step2Form.formState.errors.urgency && (
                    <p className="text-sm text-destructive">{step2Form.formState.errors.urgency.message}</p>
                  )}
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="hasDeadline"
                      onCheckedChange={(checked) => step2Form.setValue("hasDeadline", checked as boolean)}
                    />
                    <Label htmlFor="hasDeadline">I have a specific deadline</Label>
                  </div>

                  {step2Form.watch("hasDeadline") && (
                    <div className="space-y-2">
                      <Label htmlFor="deadline">Deadline Date</Label>
                      <Input id="deadline" type="date" {...step2Form.register("deadline")} />
                    </div>
                  )}
                </div>
              </form>
            )}

            {currentStep === 3 && (
              <form className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="previousLegalHelp"
                      onCheckedChange={(checked) => step3Form.setValue("previousLegalHelp", checked as boolean)}
                    />
                    <Label htmlFor="previousLegalHelp">I have received legal help for this issue before</Label>
                  </div>

                  {step3Form.watch("previousLegalHelp") && (
                    <div className="space-y-2">
                      <Label htmlFor="previousHelpDetails">Previous Legal Help Details</Label>
                      <Textarea
                        id="previousHelpDetails"
                        placeholder="Please describe the previous legal assistance you received..."
                        {...step3Form.register("previousHelpDetails")}
                      />
                    </div>
                  )}
                </div>

                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="documentsAvailable"
                      onCheckedChange={(checked) => step3Form.setValue("documentsAvailable", checked as boolean)}
                    />
                    <Label htmlFor="documentsAvailable">I have documents related to this issue</Label>
                  </div>

                  {step3Form.watch("documentsAvailable") && (
                    <div className="space-y-2">
                      <Label>Document Types (check all that apply)</Label>
                      <div className="grid grid-cols-2 gap-2">
                        {[
                          "Contracts",
                          "Court papers",
                          "Letters/emails",
                          "Government forms",
                          "Financial records",
                          "Photos",
                          "Other documents",
                        ].map((docType) => (
                          <div key={docType} className="flex items-center space-x-2">
                            <Checkbox id={docType} />
                            <Label htmlFor={docType} className="text-sm">
                              {docType}
                            </Label>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="incomeQualification">Household Income (Annual)</Label>
                  <Select onValueChange={(value) => step3Form.setValue("incomeQualification", value as any)}>
                    <SelectTrigger
                      className={step3Form.formState.errors.incomeQualification ? "border-destructive" : ""}
                    >
                      <SelectValue placeholder="Select your household income range" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="under_25k">Under $25,000</SelectItem>
                      <SelectItem value="25k_50k">$25,000 - $50,000</SelectItem>
                      <SelectItem value="50k_75k">$50,000 - $75,000</SelectItem>
                      <SelectItem value="over_75k">Over $75,000</SelectItem>
                    </SelectContent>
                  </Select>
                  {step3Form.formState.errors.incomeQualification && (
                    <p className="text-sm text-destructive">{step3Form.formState.errors.incomeQualification.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="householdSize">Household Size</Label>
                  <Input
                    id="householdSize"
                    type="number"
                    min="1"
                    placeholder="Number of people in your household"
                    {...step3Form.register("householdSize")}
                    className={step3Form.formState.errors.householdSize ? "border-destructive" : ""}
                  />
                  {step3Form.formState.errors.householdSize && (
                    <p className="text-sm text-destructive">{step3Form.formState.errors.householdSize.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="additionalInfo">Additional Information (Optional)</Label>
                  <Textarea
                    id="additionalInfo"
                    placeholder="Is there anything else you'd like us to know?"
                    {...step3Form.register("additionalInfo")}
                  />
                </div>
              </form>
            )}

            {currentStep === 4 && (
              <div className="space-y-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Review Your Information</h3>
                  <p className="text-muted-foreground">
                    Please review the information below before submitting your request.
                  </p>
                </div>

                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">Personal Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      <p>
                        <strong>Name:</strong> {formData.step1?.firstName} {formData.step1?.lastName}
                      </p>
                      <p>
                        <strong>Email:</strong> {formData.step1?.email}
                      </p>
                      <p>
                        <strong>Phone:</strong> {formData.step1?.phone}
                      </p>
                      <p>
                        <strong>Address:</strong> {formData.step1?.address}, {formData.step1?.city},{" "}
                        {formData.step1?.state} {formData.step1?.zipCode}
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">Legal Issue</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      <p>
                        <strong>Category:</strong> {formData.step2?.legalCategory}
                      </p>
                      <p>
                        <strong>Title:</strong> {formData.step2?.issueTitle}
                      </p>
                      <p>
                        <strong>Description:</strong> {formData.step2?.issueDescription}
                      </p>
                      <p>
                        <strong>Urgency:</strong> {formData.step2?.urgency}
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">Additional Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      <p>
                        <strong>Previous Legal Help:</strong> {formData.step3?.previousLegalHelp ? "Yes" : "No"}
                      </p>
                      <p>
                        <strong>Documents Available:</strong> {formData.step3?.documentsAvailable ? "Yes" : "No"}
                      </p>
                      <p>
                        <strong>Household Income:</strong> {formData.step3?.incomeQualification}
                      </p>
                      <p>
                        <strong>Household Size:</strong> {formData.step3?.householdSize}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                <div className="bg-muted/50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">What happens next?</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• We'll review your request within 1-2 business days</li>
                    <li>• You'll be matched with a qualified attorney within 3-5 business days</li>
                    <li>• Your attorney will contact you to schedule an initial consultation</li>
                    <li>• All services are provided free of charge</li>
                  </ul>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            {isSaving && (
              <>
                <Save className="h-4 w-4 animate-spin" />
                <span className="text-sm text-muted-foreground">Saving...</span>
              </>
            )}
          </div>

          <div className="flex gap-4">
            {currentStep > 1 && (
              <Button variant="outline" onClick={handlePrevious}>
                <ChevronLeft className="mr-2 h-4 w-4" />
                Previous
              </Button>
            )}

            {currentStep < steps.length ? (
              <Button onClick={handleNext}>
                Next
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            ) : (
              <Button onClick={handleSubmit} disabled={isSaving}>
                {isSaving ? "Submitting..." : "Submit Request"}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
