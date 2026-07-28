FROM python:3.11-slim
WORKDIR /app

# Install orita-mcp from PyPI
RUN pip install --no-cache-dir orita-mcp

# Environment variables (Glama / user will provide ORITA_API_KEY)
ENV ORITA_API_KEY=""
ENV ORITA_BASE_URL="https://orita.online"

# Run the MCP server (stdio transport)
CMD ["python", "-m", "orita_mcp"]
