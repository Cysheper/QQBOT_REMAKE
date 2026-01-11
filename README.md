
# QQBOT_REMAKE

一个最小的 FastAPI 服务示例。

## 运行

### 开发模式（自动重载）

> `reload` 模式下，Uvicorn **必须**使用 `模块:变量` 的 import string 形式来指定应用，否则会出现：
> `WARNING: You must pass the application as an import string to enable 'reload' or 'workers'.`

```fish
uv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 直接运行脚本

`main.py` 里已经写了 `uvicorn.run("main:app", reload=True)`，所以也可以：

```fish
uv run python main.py
```

## 接口

- `GET /`：返回 `Hello, World!`
- `POST /qq`：接收 JSON 并回显

