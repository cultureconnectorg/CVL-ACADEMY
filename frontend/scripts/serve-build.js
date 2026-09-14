const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..", "build");
const port = Number(process.env.PORT || 4180);

const TYPES = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

function safePath(urlPath) {
  const normalized = path.normalize(decodeURIComponent(urlPath.split("?")[0]));
  const relative = normalized.replace(/^([/\\])+/, "");
  const candidate = path.resolve(root, relative);
  return candidate.startsWith(root) ? candidate : null;
}

function sendFile(res, filePath) {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Not found");
      return;
    }
    const type = TYPES[path.extname(filePath).toLowerCase()] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store" });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.writeHead(405, { Allow: "GET, HEAD" });
    res.end();
    return;
  }

  const candidate = safePath(req.url || "/");
  if (candidate && fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
    sendFile(res, candidate);
    return;
  }

  // SPA navigation fallback. API requests intentionally have no fake
  // response: the production service worker must never cache API data.
  if ((req.url || "").startsWith("/api")) {
    res.writeHead(503, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ detail: "No backend in PWA smoke" }));
    return;
  }

  sendFile(res, path.join(root, "index.html"));
});

server.listen(port, "127.0.0.1", () => {
  console.log(`CVLN Academy production build on http://127.0.0.1:${port}`);
});
