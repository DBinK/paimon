# Paimon
P A I M O N - Paimon Assists In Monitoring Overlay Network

一个简单的 **桌面网络探测面板**，实时显示 PING / TCP / HTTP / DNS 延迟  

特点：

* 桌面悬浮窗口 
* YAML 配置探测目标
* 多线程并发探测
* 支持 ICMP / TCP / HTTP / DNS
* 使用 **uv** 管理环境


<img width="1345" height="1113" alt="图片" src="https://github.com/user-attachments/assets/c197e005-9753-49e7-b0c1-3611059c6657" />


---

# 快速开始

安装 **uv** (若没安装)：

```bash
pip install uv
```

克隆项目：

```bash
git clone https://github.com/DBinK/paimon
cd paimon
```

运行：

```bash
uv run paimon
```

或：

```bash
uv run src/paimon/main.py
```

`uv` 会自动创建虚拟环境并安装依赖。

---

# 配置

配置文件：

```
config/test.yaml
```

示例：

```yaml
interval: 1.0  # 检测间隔

probes:

  - label: Local PING
    type: icmp
    host: 127.0.0.1

  - label: GitHub TCP
    type: tcp
    host: github.com
    port: 443

  - label: Google HTTP
    type: http
    url: https://www.google.com/generate_204

  - label: Google DNS
    type: dns
    domain: github.com
    dns: 8.8.8.8
```

支持的类型：

* `icmp`
* `tcp`
* `http`
* `dns`

---

# 使用

启动后会显示一个 **桌面悬浮面板**：

* 左键拖动窗口
* 右键 → 退出
* 颜色表示延迟状态

---

# 依赖

主要依赖：

* PySide6
* httpx
* ping3
* dnspython

由 **uv 自动安装**。
