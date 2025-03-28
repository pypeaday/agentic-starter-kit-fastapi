# MCP Server Notes

```json
{
  "mcpServers": {
    "ragdocs": {
      "command": "node",
      "args": [
        "/opt/homebrew/lib/node_modules/@qpd-v/mcp-server-ragdocs/build/index.js"
      ],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "EMBEDDING_PROVIDER": "ollama",
        "OLLAMA_URL": "http://localhost:11434"
      },
      "alwaysAllow": [
        "search_documentation",
        "list_sources",
        "test_ollama",
        "add_documentation"
      ],
      "disabled": false
    },
    "sequentialthinking": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp/sequentialthinking"]
    },
    "qdrant": {
      "command": "uvx",
      "args": [
        "mcp-server-qdrant",
        "--qdrant-url",
        "http://localhost:6333",
        "--qdrant-api-key",
        "your_api_key",
        "--collection-name",
        "roo"
      ]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"],
      "disabled": false,
      "alwaysAllow": ["git_status", "git_commit"]
    }
  }
}
```

## ragdocs

url: <https://github.com/qpd-v/mcp-ragdocs>
notes:
npm install -g @qpd-v/mcp-server-ragdocs
npm list -g for the path and fill that in as above

###
docker run -p 6333:6333 qdrant/qdrant
