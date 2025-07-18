# 前端服务器配置说明

## 修改后端服务器地址

前端默认连接到 `https://192.168.1.100:5000`，您可以通过以下方式修改：

### 方法1: 直接修改配置文件

编辑 `src/config.js` 文件，修改默认值：

```javascript
const host = import.meta.env.VITE_SERVER_HOST || '您的IP地址';
const port = import.meta.env.VITE_SERVER_PORT || '端口号';
const useSSL = import.meta.env.VITE_USE_SSL === 'true' || true; // true为HTTPS，false为HTTP
```

### 方法2: 使用环境变量（推荐）

在 `frontend` 目录下创建 `.env` 文件：

```bash
# 后端服务器配置
VITE_SERVER_HOST=192.168.1.100
VITE_SERVER_PORT=5000
VITE_USE_SSL=true
```

### 常见配置示例

**局域网服务器（HTTPS）:**
```bash
VITE_SERVER_HOST=192.168.1.100
VITE_SERVER_PORT=5000
VITE_USE_SSL=true
```

**局域网服务器（HTTP）:**
```bash
VITE_SERVER_HOST=192.168.1.100
VITE_SERVER_PORT=5000
VITE_USE_SSL=false
```

**本地开发:**
```bash
VITE_SERVER_HOST=localhost
VITE_SERVER_PORT=5000
VITE_USE_SSL=true
```

## 注意事项

1. **HTTPS连接**: 如果使用自签名证书，浏览器可能会显示安全警告，需要手动确认继续访问
2. **防火墙**: 确保服务器的5000端口已开放
3. **网络连接**: 确保客户端设备能够访问服务器IP地址
4. **证书问题**: 如果HTTPS连接失败，可以尝试设置 `VITE_USE_SSL=false` 使用HTTP连接

## 测试连接

启动前端后，打开浏览器控制台，查看是否有 "连接到服务器: https://xxx.xxx.xxx.xxx:5000" 的日志输出。 