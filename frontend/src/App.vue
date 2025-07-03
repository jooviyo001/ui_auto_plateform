<template>
  <div>
    <div v-if="isLoggedIn">
      <nav class="nav-bar">
        <span v-for="item in navItems" :key="item.key" :class="['nav-item', {active: currentPage === item.key}]" @click="currentPage = item.key">{{ item.label }}</span>
        <span class="nav-logout" @click="logout">退出登录</span>
      </nav>
      <div class="page-content">
        <component :is="currentComponent" :token="token" />
      </div>
    </div>
    <div v-else class="login-bg">
      <div class="login-container">
        <div class="login-title">WEB自动化平台</div>
        <form class="login-form" @submit.prevent="onLogin">
          <div class="input-group">
            <input v-model="username" type="text" placeholder="用户名" required />
          </div>
          <div class="input-group">
            <input v-model="password" type="password" placeholder="密码" required />
          </div>
          <button class="login-btn" type="submit" :disabled="loading">{{ loading ? '登录中...' : '登 录' }}</button>
        </form>
        <div v-if="error" class="error-msg">{{ error }}</div>
      </div>
      <div class="neon-glow"></div>
      <div class="stars"></div>
    </div>
  </div>
</template>

<script>
import ProjectList from './ProjectList.vue'
import CaseList from './CaseList.vue'
import ExecutionList from './ExecutionList.vue'
import ReportList from './ReportList.vue'
import Settings from './Settings.vue'
import UserCenter from './UserCenter.vue'
export default {
  name: 'App',
  components: { ProjectList, CaseList, ExecutionList, ReportList, Settings, UserCenter },
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false,
      token: localStorage.getItem('token') || '',
      currentPage: 'project',
      navItems: [
        { key: 'project', label: '项目管理' },
        { key: 'case', label: '用例管理' },
        { key: 'execution', label: '执行管理' },
        { key: 'report', label: '报告查看' },
        { key: 'settings', label: '系统设置' },
        { key: 'user', label: '用户中心' }
      ]
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.token;
    },
    currentComponent() {
      switch (this.currentPage) {
        case 'project': return 'ProjectList';
        case 'case': return 'CaseList';
        case 'execution': return 'ExecutionList';
        case 'report': return 'ReportList';
        case 'settings': return 'Settings';
        case 'user': return 'UserCenter';
        default: return 'ProjectList';
      }
    }
  },
  methods: {
    async onLogin() {
      this.error = '';
      this.loading = true;
      try {
        console.log('[LOGIN] 请求参数:', this.username, this.password);
        const res = await fetch('/api/v1/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        const data = await res.json();
        console.log('[LOGIN] 响应状态:', res.status, '响应内容:', data);
        if (!res.ok) {
          this.error = data.detail || '登录失败';
        } else {
          localStorage.setItem('token', data.access_token);
          this.token = data.access_token;
        }
      } catch (e) {
        this.error = '网络错误或服务器无响应';
        console.error('[LOGIN] 网络或服务器错误:', e);
      } finally {
        this.loading = false;
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.token = '';
      this.currentPage = 'project';
    }
  }
}
</script>

<style scoped>
.nav-bar {
  display: flex;
  align-items: center;
  background: linear-gradient(90deg, #0f2027 0%, #2c5364 100%);
  padding: 0 32px;
  height: 56px;
  box-shadow: 0 2px 12px #00ffe7;
  position: sticky;
  top: 0;
  z-index: 10;
}
.nav-item {
  color: #fff;
  font-size: 1.1rem;
  margin-right: 32px;
  cursor: pointer;
  padding: 8px 0;
  transition: color 0.2s, border-bottom 0.2s;
  border-bottom: 2px solid transparent;
}
.nav-item.active {
  color: #00ffe7;
  border-bottom: 2px solid #00ffe7;
  font-weight: bold;
}
.nav-logout {
  margin-left: auto;
  color: #ff4b2b;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  padding: 8px 0;
  transition: color 0.2s;
}
.nav-logout:hover {
  color: #fff;
  text-shadow: 0 0 8px #ff4b2b;
}
.page-content {
  padding: 32px 0 0 0;
}
.login-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.login-container {
  background: rgba(20, 30, 48, 0.95);
  border-radius: 20px;
  box-shadow: 0 0 40px #00ffe7, 0 0 10px #1a2980;
  padding: 48px 36px 36px 36px;
  width: 350px;
  z-index: 2;
  position: relative;
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.login-title {
  font-size: 2rem;
  color: #00ffe7;
  text-align: center;
  margin-bottom: 32px;
  letter-spacing: 2px;
  text-shadow: 0 0 10px #00ffe7, 0 0 20px #1a2980;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-group input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: none;
  background: rgba(44, 83, 100, 0.7);
  color: #fff;
  font-size: 1rem;
  outline: none;
  box-shadow: 0 0 8px #00ffe7 inset;
  transition: box-shadow 0.3s;
}
.input-group input:focus {
  box-shadow: 0 0 16px #00ffe7 inset, 0 0 8px #1a2980;
}
.login-btn {
  background: linear-gradient(90deg, #00ffe7 0%, #1a2980 100%);
  color: #fff;
  font-size: 1.1rem;
  border: none;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  box-shadow: 0 0 20px #00ffe7, 0 0 10px #1a2980;
  transition: background 0.3s, box-shadow 0.3s;
  font-weight: bold;
  letter-spacing: 1px;
}
.login-btn:hover {
  background: linear-gradient(90deg, #1a2980 0%, #00ffe7 100%);
  box-shadow: 0 0 40px #00ffe7, 0 0 20px #1a2980;
}
.error-msg {
  color: #ff4b2b;
  text-align: center;
  margin-top: 16px;
  font-size: 1rem;
  text-shadow: 0 0 8px #ff4b2b;
}
.neon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #00ffe7 0%, transparent 70%);
  filter: blur(80px);
  transform: translate(-50%, -50%);
  z-index: 1;
  pointer-events: none;
  opacity: 0.5;
  animation: pulse 4s infinite alternate;
}
@keyframes pulse {
  0% { opacity: 0.3; }
  100% { opacity: 0.7; }
}
.stars {
  position: absolute;
  top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 0;
  pointer-events: none;
  background: transparent url('data:image/svg+xml;utf8,<svg width="100%25" height="100%25" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="1.5" fill="%23fff" opacity="0.8"/><circle cx="50" cy="80" r="1" fill="%23fff" opacity="0.5"/><circle cx="200" cy="150" r="2" fill="%23fff" opacity="0.7"/><circle cx="300" cy="300" r="1.2" fill="%23fff" opacity="0.6"/><circle cx="400" cy="100" r="1.8" fill="%23fff" opacity="0.8"/><circle cx="600" cy="400" r="1.1" fill="%23fff" opacity="0.5"/><circle cx="800" cy="200" r="1.6" fill="%23fff" opacity="0.7"/></svg>') repeat;
  animation: twinkle 10s linear infinite;
}
@keyframes twinkle {
  0% { background-position: 0 0; }
  100% { background-position: 100px 100px; }
}
</style> 