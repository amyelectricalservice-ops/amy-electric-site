const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const rootDir = path.resolve(__dirname, '..');
const PORT = 8999;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml',
  '.txt': 'text/plain',
};

const server = http.createServer((req, res) => {
  let reqPath = decodeURIComponent(req.url.split('?')[0]);
  if (reqPath === '/') reqPath = '/index.html';
  
  let filePath = path.join(rootDir, reqPath);
  if (!fs.existsSync(filePath) && fs.existsSync(filePath + '.html')) {
    filePath += '.html';
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    const mime = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mime });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Local test server running on http://127.0.0.1:${PORT}`);
  
  const targetUrl = `http://127.0.0.1:${PORT}/index.html`;
  const outputPath = path.join(rootDir, 'reports', 'lighthouse-audit.json');
  
  const chromePath = process.env.CHROME_PATH || '/usr/bin/chromium';
  const chromeFlags = '--headless --no-sandbox --disable-gpu --disable-dev-shm-usage --disable-setuid-sandbox --ignore-certificate-errors --allow-insecure-localhost';
  
  const cmd = `CHROME_PATH="${chromePath}" npx lighthouse "${targetUrl}" --chrome-flags="${chromeFlags}" --output=json --output-path="${outputPath}" --quiet`;
  
  console.log(`Running Lighthouse audit against ${targetUrl}...`);
  try {
    execSync(cmd, { stdio: 'inherit' });
    console.log('Lighthouse audit finished successfully.');
  } catch (err) {
    console.error('Lighthouse execution warning/error:', err.message);
  } finally {
    server.close(() => {
      console.log('Server closed.');
      process.exit(0);
    });
  }
});
