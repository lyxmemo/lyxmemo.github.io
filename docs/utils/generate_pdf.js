#!/usr/bin/env node

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePDF() {
  const inputFile = process.argv[2] || '_site/book.html';
  const outputFile = process.argv[3] || 'assets/与廖耀湘有关的文字资料合集.pdf';

  if (!fs.existsSync(inputFile)) {
    console.error(`Error: Input file not found: ${inputFile}`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    const fileUrl = `file://${path.resolve(inputFile)}`;
    
    console.log(`Converting: ${inputFile} → ${outputFile}`);
    await page.goto(fileUrl, { waitUntil: 'networkidle2' });
    await page.pdf({
      path: outputFile,
      format: 'A4',
      margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' }
    });
    
    console.log(`✓ PDF generated: ${outputFile}`);
  } catch (error) {
    console.error('Error generating PDF:', error);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

generatePDF();
