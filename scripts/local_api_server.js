#!/usr/bin/env node
/**
 * Local Vercel-style API server for /api/* (admin + info-banner + inquiry).
 * Loads .env.local / .env from project root.
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const ROOT = path.join(__dirname, '..');
const PORT = Number(process.env.LOCAL_API_PORT || 3001);

function loadEnvFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    const text = fs.readFileSync(filePath, 'utf8');
    text.split(/\r?\n/).forEach(function (line) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.charAt(0) === '#') return;
        const eq = trimmed.indexOf('=');
        if (eq === -1) return;
        const key = trimmed.slice(0, eq).trim();
        let val = trimmed.slice(eq + 1).trim();
        if (
            (val.startsWith('"') && val.endsWith('"')) ||
            (val.startsWith("'") && val.endsWith("'"))
        ) {
            val = val.slice(1, -1);
        }
        if (!(key in process.env)) {
            process.env[key] = val;
        }
    });
}

loadEnvFile(path.join(ROOT, '.env.local'));
loadEnvFile(path.join(ROOT, '.env'));

const ROUTES = {
    '/api/info-banner': path.join(ROOT, 'api', 'info-banner.js'),
    '/api/inquiry': path.join(ROOT, 'api', 'inquiry.js'),
    '/api/admin/login': path.join(ROOT, 'api', 'admin', 'login.js'),
    '/api/admin/logout': path.join(ROOT, 'api', 'admin', 'logout.js'),
    '/api/admin/me': path.join(ROOT, 'api', 'admin', 'me.js'),
    '/api/admin/banner': path.join(ROOT, 'api', 'admin', 'banner.js'),
    '/api/admin/translate': path.join(ROOT, 'api', 'admin', 'translate.js'),
};

function createRes(nodeRes) {
    const state = { statusCode: 200, headers: {} };
    return {
        statusCode: 200,
        setHeader: function (key, value) {
            state.headers[key] = value;
            nodeRes.setHeader(key, value);
        },
        status: function (code) {
            state.statusCode = code;
            this.statusCode = code;
            return this;
        },
        json: function (body) {
            if (!nodeRes.headersSent) {
                nodeRes.statusCode = state.statusCode;
                nodeRes.setHeader('Content-Type', 'application/json; charset=utf-8');
            }
            nodeRes.end(JSON.stringify(body));
        },
        end: function (body) {
            if (!nodeRes.headersSent) {
                nodeRes.statusCode = state.statusCode;
            }
            nodeRes.end(body == null ? '' : body);
        },
        send: function (body) {
            this.end(body);
        },
    };
}

function readBody(req) {
    return new Promise(function (resolve, reject) {
        const chunks = [];
        req.on('data', function (c) {
            chunks.push(c);
        });
        req.on('end', function () {
            const raw = Buffer.concat(chunks).toString('utf8');
            if (!raw) {
                resolve({});
                return;
            }
            const ctype = String(req.headers['content-type'] || '');
            if (ctype.indexOf('application/json') !== -1) {
                try {
                    resolve(JSON.parse(raw));
                } catch (e) {
                    reject(e);
                }
                return;
            }
            resolve(raw);
        });
        req.on('error', reject);
    });
}

function parseQuery(url) {
    const q = {};
    const idx = url.indexOf('?');
    if (idx === -1) return q;
    const search = new URLSearchParams(url.slice(idx + 1));
    search.forEach(function (value, key) {
        q[key] = value;
    });
    return q;
}

async function handle(req, res) {
    const urlPath = req.url.split('?', 1)[0];
    const routeFile = ROUTES[urlPath];
    if (!routeFile) {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify({ ok: false, error: 'Not found: ' + urlPath }));
        return;
    }

    let body = {};
    try {
        if (req.method !== 'GET' && req.method !== 'HEAD' && req.method !== 'OPTIONS') {
            body = await readBody(req);
        }
    } catch (e) {
        res.statusCode = 400;
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify({ ok: false, error: 'Neplatné JSON tělo.' }));
        return;
    }

    const handler = require(routeFile);
    const apiReq = {
        method: req.method,
        headers: req.headers,
        url: req.url,
        query: parseQuery(req.url),
        body: body,
    };
    const apiRes = createRes(res);

    try {
        await handler(apiReq, apiRes);
        if (!res.writableEnded) {
            // Handler returned without sending (e.g. requireAdmin already sent)
            if (!res.headersSent) {
                res.statusCode = apiRes.statusCode || 204;
                res.end('');
            }
        }
    } catch (e) {
        console.error('[local-api]', urlPath, e);
        if (!res.headersSent) {
            res.statusCode = 500;
            res.setHeader('Content-Type', 'application/json; charset=utf-8');
            res.end(JSON.stringify({ ok: false, error: String(e.message || e) }));
        }
    }
}

const server = http.createServer(function (req, res) {
    // CORS not needed for same-origin proxy; allow for direct hits
    if (req.method === 'OPTIONS') {
        res.statusCode = 204;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        res.end('');
        return;
    }
    handle(req, res);
});

server.listen(PORT, '127.0.0.1', function () {
    const configured = Boolean(
        process.env.ADMIN_USERNAME &&
            process.env.ADMIN_PASSWORD &&
            process.env.ADMIN_SESSION_SECRET &&
            String(process.env.ADMIN_SESSION_SECRET).length >= 16
    );
    console.log('Local API http://127.0.0.1:' + PORT + '/');
    console.log('Admin configured:', configured ? 'yes' : 'NO – fill .env.local');
});

// Keep require cache fresh-ish when restarting via nodemon isn't used
void pathToFileURL;
