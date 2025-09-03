import { NextResponse } from "next/server";
import { generatePdfBuffer } from "@/lib/pdf/generateWithPdfme";
import {
  addHeaderFooter,
  drawSimpleTable,
  mergePdfs,
} from "@/lib/pdf/enhanceWithPdfLib";

export const dynamic = "force-dynamic";

function base64PdfToUint8Array(b64: string): Uint8Array {
  // Works reliably on Node runtimes
  return new Uint8Array(Buffer.from(b64, "base64"));
}

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // 1) Base PDF from template
    const basePdf = await generatePdfBuffer({
      clientName: body.clientName ?? "John Doe",
      caseNumber: body.caseNumber ?? "SPB-12345",
      dateIssued: body.dateIssued ?? new Date().toLocaleDateString(),
      bodyText: body.bodyText ?? "This is a SmartProBono document.",
    });

    // 2) Add header/footer
    let current = await addHeaderFooter(basePdf, {
      header: "SmartProBono • Access to Justice",
      footer: "Confidential — For client use only",
    });

    // 3) Add a simple table (example rows; replace with your real data)
    current = await drawSimpleTable(
      current,
      (body.tableRows ?? [
        { cols: ["Item", "Qty", "Amount"] },
        { cols: ["Filing Fee", "1", "$0.00"] },
        { cols: ["Service Fee", "1", "$0.00"] },
      ]) as Array<{ cols: string[] }>,
      { x: 36, y: 520 },
      [250, 100, 150],
      24
    );

    // 4) Optionally merge with attachments (base64-encoded PDFs)
    if (Array.isArray(body.attachments) && body.attachments.length) {
      const buffers = [current, ...body.attachments.map((b64: string) => base64PdfToUint8Array(b64))];
      current = await mergePdfs(buffers);
    }

    return new NextResponse(Buffer.from(current), {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'inline; filename="smartprobono.pdf"',
      },
    });
  } catch (e: any) {
    return NextResponse.json(
      { error: e?.message ?? "PDF generation failed" },
      { status: 500 }
    );
  }
}
