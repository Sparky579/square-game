// 前端配置文件
// 支持通过环境变量配置服务器地址

// 从环境变量获取配置，如果没有则使用默认值
const getEnvConfig = () => {
  // Vite 环境变量以 VITE_ 开头
  const host = import.meta.env.VITE_SERVER_HOST || 'sqapi.pekka.asia';
  const port = import.meta.env.VITE_SERVER_PORT || '443';
  // 使用HTTPS
  const useSSL = import.meta.env.VITE_USE_SSL === 'false' ? false : true;
  
  return {
    host,
    port: parseInt(port),
    useSSL
  };
};

export const config = {
  // 后端服务器配置
  server: getEnvConfig(),
  
  // 获取完整的服务器URL
  getServerUrl() {
    const protocol = this.server.useSSL ? 'https' : 'http';
    // 如果是标准端口（80或443），则不显示端口号
    const isStandardPort = (this.server.useSSL && this.server.port === 443) || 
                          (!this.server.useSSL && this.server.port === 80);
    const portPart = isStandardPort ? '' : `:${this.server.port}`;
    return `${protocol}://${this.server.host}${portPart}`;
  },
  
  // 获取WebSocket连接URL（Socket.IO）
  getSocketUrl() {
    return this.getServerUrl();
  },
  
  // 获取API URL
  getApiUrl() {
    return `${this.getServerUrl()}/api`;
  }
};

// 开发环境下的localhost配置（可选）
export const devConfig = {
  server: {
    host: 'localhost', // 本地开发
    port: 5000,
    useSSL: true
  },
  getServerUrl() {
    const protocol = this.server.useSSL ? 'https' : 'http';
    // 如果是标准端口（80或443），则不显示端口号
    const isStandardPort = (this.server.useSSL && this.server.port === 443) || 
                          (!this.server.useSSL && this.server.port === 80);
    const portPart = isStandardPort ? '' : `:${this.server.port}`;
    return `${protocol}://${this.server.host}${portPart}`;
  },
  getSocketUrl() {
    return this.getServerUrl();
  },
  getApiUrl() {
    return `${this.getServerUrl()}/api`;
  }
};

// 显示当前配置（用于调试）
console.log('当前服务器配置:', config.getServerUrl()); 