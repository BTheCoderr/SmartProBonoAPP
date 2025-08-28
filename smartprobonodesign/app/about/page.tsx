import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Users, Heart, Scale, Target } from "lucide-react"

const teamMembers = [
  {
    name: "Sarah Johnson",
    role: "Executive Director",
    description: "Former legal aid attorney with 15 years of experience serving underrepresented communities.",
  },
  {
    name: "Michael Chen",
    role: "Technology Director",
    description: "Software engineer passionate about using technology to increase access to justice.",
  },
  {
    name: "Maria Rodriguez",
    role: "Legal Director",
    description: "Immigration attorney and advocate with expertise in pro bono program development.",
  },
  {
    name: "David Kim",
    role: "Community Outreach Director",
    description: "Community organizer focused on connecting legal services with those who need them most.",
  },
]

const stats = [
  { number: "10,000+", label: "People Helped" },
  { number: "500+", label: "Volunteer Attorneys" },
  { number: "50+", label: "Partner Organizations" },
  { number: "95%", label: "Client Satisfaction" },
]

export default function AboutPage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-b from-background to-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-6 max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">About SmartProBono</h1>
            <p className="text-muted-foreground text-lg md:text-xl">
              We believe everyone deserves access to quality legal help, regardless of their ability to pay. Our mission
              is to bridge the justice gap through technology, compassion, and community.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Our Mission</h2>
              <p className="text-muted-foreground text-lg">
                SmartProBono was founded on the principle that legal help should be accessible to everyone. We use
                technology to connect people facing legal challenges with qualified attorneys who are committed to
                providing pro bono services.
              </p>
              <p className="text-muted-foreground text-lg">
                Our platform streamlines the process of finding legal help, making it easier for both clients to get the
                assistance they need and for attorneys to contribute their expertise to their communities.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-6">
              {stats.map((stat, index) => (
                <Card key={index} className="text-center">
                  <CardHeader>
                    <CardTitle className="text-3xl font-bold text-primary">{stat.number}</CardTitle>
                    <CardDescription className="font-medium">{stat.label}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Our Values</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              These core values guide everything we do and shape how we serve our community.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="text-center">
              <CardHeader>
                <Scale className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Justice for All</CardTitle>
                <CardDescription>
                  We believe legal help should be available to everyone, regardless of income or background.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Compassion</CardTitle>
                <CardDescription>
                  We approach every case with empathy and understanding, recognizing the human impact of legal issues.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Users className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Community</CardTitle>
                <CardDescription>
                  We build strong partnerships with attorneys, organizations, and communities to maximize our impact.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Target className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Excellence</CardTitle>
                <CardDescription>
                  We maintain high standards for legal services and continuously improve our platform and processes.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Our Team</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              Meet the dedicated professionals working to make legal help more accessible.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="w-20 h-20 bg-muted rounded-full mx-auto mb-4 flex items-center justify-center">
                    <Users className="h-10 w-10 text-muted-foreground" />
                  </div>
                  <CardTitle className="text-lg">{member.name}</CardTitle>
                  <CardDescription className="font-medium text-primary">{member.role}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{member.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-8">
            <div className="space-y-4 max-w-2xl mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Join Our Mission</h2>
              <p className="text-muted-foreground text-lg">
                Whether you need legal help or want to provide it, there's a place for you in our community.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="text-lg px-8">
                <Link href="/get-help">Get Legal Help</Link>
              </Button>
              <Button variant="outline" size="lg" asChild className="text-lg px-8 bg-transparent">
                <Link href="/attorney">Volunteer as Attorney</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
