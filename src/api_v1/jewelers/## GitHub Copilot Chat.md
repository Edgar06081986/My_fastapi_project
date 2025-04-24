## GitHub Copilot Chat

- Extension Version: 0.26.7 (prod)
- VS Code: vscode/1.99.3
- OS: Linux

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 140.82.121.5 (27 ms)
- DNS ipv6 Lookup: Error (26 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (1 ms)
- Electron fetch (configured): HTTP 200 (197 ms)
- Node.js https: HTTP 200 (220 ms)
- Node.js fetch: HTTP 200 (240 ms)
- Helix fetch: HTTP 200 (290 ms)

Connecting to https://api.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.112.21 (75 ms)
- DNS ipv6 Lookup: Error (2 ms): getaddrinfo ENOTFOUND api.githubcopilot.com
- Proxy URL: None (2 ms)
- Electron fetch (configured): HTTP 200 (438 ms)
- Node.js https: HTTP 200 (487 ms)
- Node.js fetch: HTTP 200 (454 ms)
- Helix fetch: HTTP 200 (475 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).