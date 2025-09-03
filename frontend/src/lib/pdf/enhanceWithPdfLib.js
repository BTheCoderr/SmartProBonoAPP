import { PDFDocument, StandardFonts, rgb } from "pdf-lib";

// Merge multiple PDFs (Uint8Array each) into one
export async function mergePdfs(buffers) {
  const out = await PDFDocument.create();
  for (const buf of buffers) {
    const src = await PDFDocument.load(buf);
    const pages = await out.copyPages(src, src.getPageIndices());
    pages.forEach((p) => out.addPage(p));
  }
  return await out.save();
}

// Add simple header/footer text and page numbers
export async function addHeaderFooter(pdfBytes, opts = {}) {
  const doc = await PDFDocument.load(pdfBytes);
  const font = await doc.embedFont(StandardFonts.Helvetica);
  const size = 9;

  doc.getPages().forEach((page, idx) => {
    const { width, height } = page.getSize();
    if (opts.header) {
      page.drawText(opts.header, { x: 36, y: height - 24, size, font, color: rgb(0, 0, 0) });
    }
    if (opts.footer) {
      page.drawText(`${opts.footer}  ·  Page ${idx + 1} of ${doc.getPageCount()}`, {
        x: 36,
        y: 24,
        size,
        font,
        color: rgb(0, 0, 0),
      });
    }
  });

  return await doc.save();
}

// Super-lightweight fixed table (good enough for short lists)
// For real pagination and long tables, we can extend this later.
export async function drawSimpleTable(
  pdfBytes,
  rows,
  start = { x: 36, y: 600 },
  colWidths = [200, 150, 150],
  rowHeight = 22
) {
  const doc = await PDFDocument.load(pdfBytes);
  const font = await doc.embedFont(StandardFonts.Helvetica);
  const page = doc.getPages()[0];

  let y = start.y;
  for (const r of rows) {
    let x = start.x;
    r.cols.forEach((txt, i) => {
      page.drawText(txt ?? "", { x: x + 4, y: y + 6, size: 10, font, color: rgb(0, 0, 0) });
      page.drawRectangle({
        x,
        y,
        width: colWidths[i],
        height: rowHeight,
        borderColor: rgb(0, 0, 0),
        borderWidth: 0.5,
        opacity: 1,
      });
      x += colWidths[i];
    });
    y -= rowHeight;
  }
  return await doc.save();
}

// Place a PNG signature image at coordinates on a page
export async function placeSignatureImage(
  pdfBytes,
  pngBytes,
  opts = { pageIndex: 0, x: 380, y: 120, width: 160, height: 60 }
) {
  const doc = await PDFDocument.load(pdfBytes);
  const page = doc.getPages()[opts.pageIndex];
  const sig = await doc.embedPng(pngBytes);
  page.drawImage(sig, { x: opts.x, y: opts.y, width: opts.width, height: opts.height });
  return await doc.save();
}
