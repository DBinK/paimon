$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location -LiteralPath $ProjectRoot

# uv run 自动处理虚拟环境和参数
& uv run "src/paimon/main.py"

Read-Host "按任意键退出..."
