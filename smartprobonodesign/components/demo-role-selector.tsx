"use client"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { useAuth } from "@/lib/auth-context"
import type { DemoRole } from "@/lib/types"

const roleLabels: Record<DemoRole, string> = {
  client: "Client",
  attorney: "Attorney",
  admin: "Admin",
  paralegal: "Paralegal",
}

const roleColors: Record<DemoRole, "default" | "secondary" | "destructive" | "outline"> = {
  client: "default",
  attorney: "secondary",
  admin: "destructive",
  paralegal: "outline",
}

export function DemoRoleSelector() {
  const { demoRole, setDemoRole } = useAuth()

  return (
    <div className="flex items-center gap-2">
      <Badge variant={roleColors[demoRole]} className="text-xs">
        Demo: {roleLabels[demoRole]}
      </Badge>
      <Select value={demoRole} onValueChange={(value: DemoRole) => setDemoRole(value)}>
        <SelectTrigger className="w-32 h-8 text-xs">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {Object.entries(roleLabels).map(([role, label]) => (
            <SelectItem key={role} value={role} className="text-xs">
              {label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
