"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Checkbox } from "@/components/ui/checkbox"
import { useToast } from "@/hooks/use-toast"
import { Heart, Users, Scale, Shield, DollarSign } from "lucide-react"

const donationAmounts = [
  { value: "25", label: "$25", description: "Helps one person access legal resources" },
  { value: "50", label: "$50", description: "Supports intake processing for 2-3 cases" },
  { value: "100", label: "$100", description: "Funds attorney matching for 5 clients" },
  { value: "250", label: "$250", description: "Covers platform costs for 10 cases" },
  { value: "500", label: "$500", description: "Supports a full case from start to finish" },
  { value: "custom", label: "Custom", description: "Enter your own amount" },
]

const impactStats = [
  {
    icon: Users,
    number: "10,000+",
    label: "People Helped",
    description: "Individuals who received free legal assistance",
  },
  {
    icon: Scale,
    number: "$2.5M",
    label: "Legal Value",
    description: "Estimated value of pro bono services provided",
  },
  {
    icon: Heart,
    number: "500+",
    label: "Volunteer Attorneys",
    description: "Legal professionals donating their time",
  },
  {
    icon: Shield,
    number: "95%",
    label: "Success Rate",
    description: "Cases resolved successfully",
  },
]

export default function DonatePage() {
  const [selectedAmount, setSelectedAmount] = useState("50")
  const [customAmount, setCustomAmount] = useState("")
  const [isMonthly, setIsMonthly] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { toast } = useToast()

  const handleDonate = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate donation processing
    await new Promise((resolve) => setTimeout(resolve, 2000))

    toast({
      title: "Thank you for your donation!",
      description: "Your contribution will help us provide legal assistance to those in need.",
    })

    setIsSubmitting(false)
  }

  const getAmount = () => {
    return selectedAmount === "custom" ? customAmount : selectedAmount
  }

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-b from-background to-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Support Our Mission</h1>
            <p className="text-muted-foreground text-lg md:text-xl">
              Your donation helps us provide free legal assistance to those who need it most. Every contribution makes a
              real difference in someone's life.
            </p>
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Your Impact</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              See how your donations have helped us make legal assistance accessible to everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {impactStats.map((stat, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <stat.icon className="h-12 w-12 text-primary mx-auto mb-4" />
                  <CardTitle className="text-3xl font-bold text-primary">{stat.number}</CardTitle>
                  <CardDescription className="font-medium">{stat.label}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{stat.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Donation Form Section */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="max-w-4xl mx-auto">
            <div className="text-center space-y-4 mb-12">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Make a Donation</h2>
              <p className="text-muted-foreground text-lg">
                Choose an amount that works for you. Every dollar helps us serve more people in need.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              {/* Donation Amounts */}
              <div className="space-y-8">
                <Card>
                  <CardHeader>
                    <CardTitle>Select Amount</CardTitle>
                    <CardDescription>Choose a donation amount or enter a custom amount.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <RadioGroup value={selectedAmount} onValueChange={setSelectedAmount}>
                      <div className="grid grid-cols-1 gap-4">
                        {donationAmounts.map((amount) => (
                          <div key={amount.value} className="flex items-center space-x-3">
                            <RadioGroupItem value={amount.value} id={amount.value} />
                            <Label htmlFor={amount.value} className="flex-1 cursor-pointer">
                              <div className="flex justify-between items-center">
                                <span className="font-medium">{amount.label}</span>
                                <span className="text-sm text-muted-foreground">{amount.description}</span>
                              </div>
                            </Label>
                          </div>
                        ))}
                      </div>
                    </RadioGroup>

                    {selectedAmount === "custom" && (
                      <div className="space-y-2">
                        <Label htmlFor="customAmount">Custom Amount</Label>
                        <div className="relative">
                          <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                          <Input
                            id="customAmount"
                            type="number"
                            placeholder="0.00"
                            value={customAmount}
                            onChange={(e) => setCustomAmount(e.target.value)}
                            className="pl-10"
                            min="1"
                          />
                        </div>
                      </div>
                    )}

                    <div className="flex items-center space-x-2">
                      <Checkbox id="monthly" checked={isMonthly} onCheckedChange={setIsMonthly} />
                      <Label htmlFor="monthly" className="text-sm">
                        Make this a monthly donation
                      </Label>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Donation Summary & Form */}
              <div className="space-y-8">
                <Card>
                  <CardHeader>
                    <CardTitle>Donation Summary</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>Amount:</span>
                      <span className="font-medium">${getAmount()}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Frequency:</span>
                      <span className="font-medium">{isMonthly ? "Monthly" : "One-time"}</span>
                    </div>
                    <div className="border-t pt-4">
                      <div className="flex justify-between items-center font-semibold">
                        <span>Total:</span>
                        <span>${getAmount()}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Donor Information</CardTitle>
                    <CardDescription>Your information is secure and will not be shared.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleDonate} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="firstName">First Name</Label>
                          <Input id="firstName" placeholder="Enter your first name" required />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="lastName">Last Name</Label>
                          <Input id="lastName" placeholder="Enter your last name" required />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" type="email" placeholder="Enter your email" required />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="address">Address (Optional)</Label>
                        <Input id="address" placeholder="Enter your address" />
                      </div>

                      <div className="flex items-center space-x-2">
                        <Checkbox id="anonymous" />
                        <Label htmlFor="anonymous" className="text-sm">
                          Make this donation anonymous
                        </Label>
                      </div>

                      <Button type="submit" className="w-full" disabled={isSubmitting || !getAmount()}>
                        {isSubmitting ? "Processing..." : `Donate $${getAmount()}`}
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Other Ways to Help */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Other Ways to Help</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              There are many ways to support our mission beyond financial donations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <Scale className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Volunteer as Attorney</CardTitle>
                <CardDescription>
                  Share your legal expertise by taking on pro bono cases through our platform.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" asChild>
                  <a href="/attorney">Learn More</a>
                </Button>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Users className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Spread the Word</CardTitle>
                <CardDescription>
                  Help us reach more people who need legal assistance by sharing our mission.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" asChild>
                  <a href="/about">Share Our Story</a>
                </Button>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Corporate Partnership</CardTitle>
                <CardDescription>
                  Partner with us to provide legal assistance as part of your corporate social responsibility.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" asChild>
                  <a href="/contact">Contact Us</a>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  )
}
