import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Scale, Users, FileText, MessageSquare, Shield, Clock, ArrowRight, CheckCircle, Star } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-background via-secondary/30 to-background py-24 lg:py-32">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container relative px-4 md:px-6 max-w-screen-xl">
          <div className="flex flex-col items-center space-y-8 text-center animate-fade-in-up">
            <Badge variant="secondary" className="px-4 py-2 text-sm font-medium">
              Trusted by 10,000+ clients nationwide
            </Badge>
            <div className="space-y-6 max-w-4xl">
              <h1 className="text-5xl font-bold tracking-tight sm:text-6xl md:text-7xl lg:text-8xl">
                Empowering Your <span className="gradient-text">Legal Journey</span>
              </h1>
              <p className="mx-auto max-w-2xl text-muted-foreground text-xl md:text-2xl leading-relaxed">
                Connect with dedicated pro bono attorneys ready to help you navigate legal challenges with confidence
                and support.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button
                size="lg"
                className="text-lg px-8 py-4 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
                asChild
              >
                <Link href="/get-help">
                  Find Your Attorney
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="text-lg px-8 py-4 hover:bg-secondary transition-all duration-300 bg-transparent"
                asChild
              >
                <Link href="/how-it-works">How it Works</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-16 bg-muted/30">
        <div className="container px-4 md:px-6 max-w-screen-xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-3xl font-bold text-primary">10,000+</div>
              <div className="text-sm text-muted-foreground">Clients Helped</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-primary">500+</div>
              <div className="text-sm text-muted-foreground">Pro Bono Attorneys</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-primary">98%</div>
              <div className="text-sm text-muted-foreground">Success Rate</div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-center items-center space-x-1">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 fill-accent text-accent" />
                ))}
              </div>
              <div className="text-sm text-muted-foreground">Client Rating</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 lg:py-32">
        <div className="container px-4 md:px-6 max-w-screen-xl">
          <div className="text-center space-y-6 mb-20">
            <Badge variant="outline" className="px-4 py-2">
              Why Choose SmartProBono
            </Badge>
            <h2 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
              Legal Help That Actually <span className="gradient-text">Works</span>
            </h2>
            <p className="mx-auto max-w-3xl text-muted-foreground text-xl leading-relaxed">
              We've reimagined legal assistance to be accessible, efficient, and genuinely supportive for everyone who
              needs it.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Scale,
                title: "Expert Legal Matching",
                description:
                  "Our AI-powered system connects you with attorneys who specialize in your exact legal needs, ensuring the best possible outcome.",
              },
              {
                icon: Users,
                title: "Vetted Pro Bono Network",
                description:
                  "Every attorney in our network is thoroughly vetted and committed to providing high-quality pro bono services.",
              },
              {
                icon: FileText,
                title: "Smart Document Tools",
                description:
                  "Get help with legal documents through our intelligent tools that guide you step-by-step through complex paperwork.",
              },
              {
                icon: MessageSquare,
                title: "Secure Communication",
                description:
                  "Communicate safely with your attorney through our encrypted platform that maintains attorney-client privilege.",
              },
              {
                icon: Shield,
                title: "Privacy First",
                description:
                  "Your information is protected with enterprise-grade security and strict confidentiality protocols.",
              },
              {
                icon: Clock,
                title: "24/7 Platform Access",
                description:
                  "Access your case information, documents, and resources anytime, anywhere from any device.",
              },
            ].map((feature, index) => (
              <Card
                key={index}
                className="hover-lift border-2 hover:border-primary/20 transition-all duration-300 animate-scale-in group"
              >
                <CardHeader className="space-y-4">
                  <div className="flex items-center justify-center h-16 w-16 rounded-2xl bg-primary/10 group-hover:bg-primary/20 transition-colors">
                    <feature.icon className="h-8 w-8 text-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base leading-relaxed">{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Legal Areas Section */}
      <section className="py-24 lg:py-32 bg-secondary/20">
        <div className="container px-4 md:px-6 max-w-screen-xl">
          <div className="text-center space-y-6 mb-20">
            <Badge variant="outline" className="px-4 py-2">
              Legal Practice Areas
            </Badge>
            <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
              Comprehensive Legal <span className="gradient-text">Support</span>
            </h2>
            <p className="mx-auto max-w-3xl text-muted-foreground text-xl leading-relaxed">
              We provide expert assistance across the legal matters that affect everyday people most.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                title: "Immigration Law",
                description: "Visa applications, citizenship, asylum, family reunification, deportation defense",
                popular: true,
              },
              {
                title: "Housing Rights",
                description: "Tenant rights, evictions, discrimination, housing assistance, landlord disputes",
              },
              {
                title: "Family Law",
                description: "Divorce, custody, domestic violence, adoption, child support",
              },
              {
                title: "Employment Law",
                description: "Workplace discrimination, wage theft, unemployment benefits, wrongful termination",
              },
              {
                title: "Public Benefits",
                description: "Social Security, disability, food assistance, healthcare, veterans benefits",
              },
              {
                title: "Consumer Protection",
                description: "Debt collection, scams, contract disputes, bankruptcy, credit repair",
              },
              {
                title: "Criminal Defense",
                description: "Misdemeanors, expungement, victim rights, traffic violations",
              },
              {
                title: "Civil Rights",
                description: "Discrimination, police misconduct, voting rights, accessibility",
              },
            ].map((area, index) => (
              <Card key={index} className="hover-lift transition-all duration-300 relative group">
                {area.popular && (
                  <Badge className="absolute -top-2 -right-2 bg-accent text-accent-foreground">Most Popular</Badge>
                )}
                <CardHeader className="text-center space-y-3">
                  <CardTitle className="text-lg group-hover:text-primary transition-colors">{area.title}</CardTitle>
                  <CardDescription className="text-sm leading-relaxed">{area.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 lg:py-32 bg-gradient-to-r from-primary to-primary/90 text-primary-foreground">
        <div className="container px-4 md:px-6 max-w-screen-xl">
          <div className="flex flex-col items-center space-y-8 text-center">
            <div className="space-y-6 max-w-3xl">
              <h2 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
                Ready to Take Control of Your Legal Situation?
              </h2>
              <p className="text-primary-foreground/90 text-xl leading-relaxed">
                Don't let legal challenges overwhelm you. Start your journey to resolution today with professional,
                compassionate legal assistance.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button
                size="lg"
                variant="secondary"
                className="text-lg px-8 py-4 hover:scale-105 transition-all duration-300 shadow-lg"
                asChild
              >
                <Link href="/get-help">
                  Start Your Case Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="text-lg px-8 py-4 border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/10 bg-transparent"
                asChild
              >
                <Link href="/attorney">Join as Attorney</Link>
              </Button>
            </div>
            <div className="flex items-center space-x-6 pt-8 text-sm text-primary-foreground/80">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4" />
                <span>100% Free Consultation</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4" />
                <span>No Hidden Fees</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4" />
                <span>Confidential & Secure</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
