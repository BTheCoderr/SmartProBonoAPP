# SmartProBono — Legacy Legal Platform Prototype

> **Current production:** https://smartprobono.org  
> **Current canonical codebase:** `BTheCoderr/smartprobonoip`
>
> This repository is an earlier SmartProBono legal-tech prototype. It is kept as a reference for features, UX ideas, and migration candidates. It is **not** the source currently serving SmartProBono production.

<!-- repo-intro:start -->
**Project snapshot:** Earlier full-stack SmartProBono experiments covering AI-assisted intake, legal research, document workflows, role-based dashboard concepts, WebSocket experiments, and case-management prototypes.

**What it demonstrates:** Full-stack product design · AI-assisted workflows · role-based UX concepts · legal-tech prototyping · Flask + React architecture.

**Important:** A file, component, or API route being present in this repository does not mean that capability is enabled, production-ready, or live at smartprobono.org.
<!-- repo-intro:end -->

## Current Status

SmartProBono has moved forward into a unified **Legal + IP preparation platform** at **https://smartprobono.org**.

The current production product uses the newer `smartprobonoip` repository as its canonical codebase. That application now provides the SmartProBono umbrella experience, SmartProBono Legal, SmartProBonoIP, unified accounts/workspaces, and the current Supabase architecture.

This older repository should be treated as a **feature archive and prototype source**, not a production feature checklist.

## What This Repository Actually Contains

### Active frontend routes in this legacy build

The current `frontend/src/App.js` actively mounts:

- Home
- About
- Contact
- Legal AI Chat
- Document Scan
- Login
- Register
- Dashboard
- Privacy
- Terms

The app also contains many additional page components and experiments, but most are currently commented out or otherwise not enabled in the active router.

### Prototype / migration-candidate features present in code

Code exists for concepts including:

- AI Virtual Paralegal workflows
- CourtListener/case-law research
- Client portal
- Lawyer dashboard
- Bondsman dashboard
- Admin dashboard
- Document generation
- Legal forms
- Document collaboration
- WebSocket notifications
- Compliance/risk experiments
- CRM/case-management APIs
- Enhanced v2 APIs
- Voice/court-filing/model-management experiments

These should be described as **prototype capabilities or migration candidates**, not as live production features unless they are separately verified and enabled.

## Important Legacy Limitations

This repository includes development shortcuts and prototype implementations that should not be represented as production behavior:

- The frontend `ProtectedRoute` currently allows access without enforcing authentication.
- Many dashboard/tool routes are commented out in `frontend/src/App.js`.
- Document collaboration currently uses in-memory dictionaries for demo storage rather than durable collaborative persistence.
- The standalone WebSocket server defaults to `localhost:8765`.
- Several backend blueprints are conditionally registered and can be unavailable if dependencies or services are missing.
- Some older feature documentation describes intended behavior more broadly than the currently active runtime.
- This repository is not the code currently deployed at `smartprobono.org`.

## Production

Use the current product here:

**https://smartprobono.org**

The production SmartProBono architecture is organized around:

- **SmartProBono Legal** — legal preparation, document understanding, Ermi, draft preparation, and guided workflows.
- **SmartProBonoIP** — IP readiness, invention organization, research preparation, and professional handoff.
- **Unified Workspace** — authenticated Legal + IP persistence while preserving anonymous IP preparation.
- **Learn → Prepare → Connect** — the platform operating model.

SmartProBono is a preparation platform and is not a law firm. It does not replace lawyers, courts, legal-aid organizations, patent professionals, or other qualified professionals.

## Local Development for This Legacy Repository

`localhost` is used **only for local development of this historical codebase**. It is not the public SmartProBono address.

### Backend

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd backend
python combined_server.py
```

Typical legacy local backend:

```text
http://localhost:3001
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Typical legacy local frontend:

```text
http://localhost:3002
```

## Legacy Project Structure

```text
SmartProBonoAPP/
├── backend/
│   ├── combined_server.py
│   ├── production_app.py
│   ├── routes/
│   ├── services/
│   └── websocket_server.py
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── App.js
│   └── public/
└── requirements.txt
```

## Notable Legacy APIs

The repository contains backend implementations for several API groups, including:

- Document scanning and document generation
- Legal AI
- AI Virtual Paralegal experiments
- CourtListener research
- Enhanced v2 case/user/document APIs
- CRM and intake workflows
- Document collaboration
- Analytics
- Voice and court-filing experiments

Because this is a legacy prototype repository, do not assume every endpoint is enabled in the deployed runtime merely because its source file exists.

## Migration Rule

When a capability from this repository is useful, migrate it deliberately into the canonical SmartProBono platform rather than reactivating the entire old stack.

Migration candidates should receive:

1. Current security/auth architecture
2. Current Supabase ownership/RLS model
3. Current SmartProBono Legal safety language
4. Production tests
5. Explicit Legal/IP workspace integration
6. Current deployment verification at `smartprobono.org`

## License

MIT License — see `LICENSE`.
