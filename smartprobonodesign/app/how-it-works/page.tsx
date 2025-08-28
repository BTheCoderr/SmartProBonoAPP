import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { ArrowRight, UserCheck, FileSearch, MessageCircle, Gavel } from "lucide-react"

export default function HowItWorksPage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-b from-background to-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">How SmartProBono Works</h1>
            <p className="text-muted-foreground text-lg md:text-xl">
              Getting legal help shouldn't be complicated. Our simple 4-step process connects you with qualified
              attorneys who can help resolve your legal matters.
            </p>
          </div>
        </div>
      </section>

      {/* Steps Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="relative">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                  <UserCheck className="h-8 w-8 text-primary-foreground" />
                </div>
                <Badge className="absolute -top-2 -right-2 w-8 h-8 rounded-full p-0 flex items-center justify-center">
                  1
                </Badge>
              </div>
              <h3 className="text-xl font-semibold">Tell Us Your Story</h3>
              <p className="text-muted-foreground">
                Complete our secure intake form to help us understand your legal situation and needs.
              </p>
            </div>

            <div className="flex flex-col items-center text-center space-y-4">
              <div className="relative">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                  <FileSearch className="h-8 w-8 text-primary-foreground" />
                </div>
                <Badge className="absolute -top-2 -right-2 w-8 h-8 rounded-full p-0 flex items-center justify-center">
                  2
                </Badge>
              </div>
              <h3 className="text-xl font-semibold">Get Matched</h3>
              <p className="text-muted-foreground">
                Our system matches you with qualified attorneys who specialize in your type of legal issue.
              </p>
            </div>

            <div className="flex flex-col items-center text-center space-y-4">
              <div className="relative">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                  <MessageCircle className="h-8 w-8 text-primary-foreground" />
                </div>
                <Badge className="absolute -top-2 -right-2 w-8 h-8 rounded-full p-0 flex items-center justify-center">
                  3
                </Badge>
              </div>
              <h3 className="text-xl font-semibold">Connect & Collaborate</h3>
              <p className="text-muted-foreground">
                Work directly with your attorney through our secure platform to build your case.
              </p>
            </div>

            <div className="flex flex-col items-center text-center space-y-4">
              <div className="relative">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                  <Gavel className="h-8 w-8 text-primary-foreground" />
                </div>
                <Badge className="absolute -top-2 -right-2 w-8 h-8 rounded-full p-0 flex items-center justify-center">
                  4
                </Badge>
              </div>
              <h3 className="text-xl font-semibold">Resolve Your Case</h3>
              <p className="text-muted-foreground">
                Get the legal resolution you need with ongoing support throughout the process.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">What Makes Us Different</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              We've built technology that makes legal help more accessible and efficient for everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>Always Free</CardTitle>
                <CardDescription>
                  Our services are completely free for clients. No hidden fees, no surprise charges.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Vetted Attorneys</CardTitle>
                <CardDescription>
                  All attorneys are licensed, experienced, and committed to providing quality pro bono services.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Secure Platform</CardTitle>
                <CardDescription>
                  Your information is protected with encryption and attorney-client privilege.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Document Help</CardTitle>
                <CardDescription>
                  Get assistance with legal forms, document review, and paperwork preparation.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Case Tracking</CardTitle>
                <CardDescription>
                  Monitor your case progress, deadlines, and communications in one place.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>24/7 Access</CardTitle>
                <CardDescription>Access your case information and resources anytime from any device.</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-8">
            <div className="space-y-4 max-w-2xl mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Ready to Get Started?</h2>
              <p className="text-muted-foreground text-lg">
                Join thousands of people who have found legal help through SmartProBono.
              </p>
            </div>
            <Button size="lg" asChild className="text-lg px-8">
              <Link href="/get-help">
                Start Your Case <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
