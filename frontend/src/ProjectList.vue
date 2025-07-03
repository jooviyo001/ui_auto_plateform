<template>
  <div class="project-list-bg">
    <div class="project-list-container">
      <h2>项目管理</h2>
      <button class="logout-btn" @click="logout">退出登录</button>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <ul v-if="projects.length">
        <li v-for="project in projects" :key="project.id" class="project-item">
          <div class="project-name">{{ project.name }}</div>
          <div class="project-desc">{{ project.description }}</div>
        </li>
      </ul>
      <div v-else-if="!loading">暂无项目</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectList',
  props: ['token'],
  data() {
    return {
      projects: [],
      loading: false,
      error: ''
    }
  },
  mounted() {
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch('/api/v1/project/', {
          headers: {
            'Authorization': 'Bearer ' + this.token
          }
        });
        const data = await res.json();
        if (!res.ok) {
          this.error = data.detail || '获取项目失败';
        } else {
          this.projects = data;
        }
      } catch (e) {
        this.error = '网络错误或服务器无响应';
      } finally {
        this.loading = false;
      }
    },
    logout() {
      localStorage.removeItem('token');
      location.reload();
    }
  }
}
</script>

<style scoped>
.project-list-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #232526 0%, #414345 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.project-list-container {
  background: rgba(30, 40, 60, 0.98);
  border-radius: 18px;
  box-shadow: 0 0 30px #00ffe7, 0 0 8px #1a2980;
  padding: 40px 32px 32px 32px;
  width: 420px;
  position: relative;
}
.project-list-container h2 {
  color: #00ffe7;
  text-align: center;
  margin-bottom: 28px;
  letter-spacing: 2px;
  text-shadow: 0 0 8px #00ffe7, 0 0 16px #1a2980;
}
.logout-btn {
  position: absolute;
  top: 18px;
  right: 24px;
  background: linear-gradient(90deg, #ff4b2b 0%, #1a2980 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 6px 16px;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 0 10px #ff4b2b, 0 0 4px #1a2980;
  transition: background 0.3s, box-shadow 0.3s;
}
.logout-btn:hover {
  background: linear-gradient(90deg, #1a2980 0%, #ff4b2b 100%);
  box-shadow: 0 0 20px #ff4b2b, 0 0 8px #1a2980;
}
.loading {
  color: #00ffe7;
  text-align: center;
  margin: 20px 0;
}
.error-msg {
  color: #ff4b2b;
  text-align: center;
  margin: 20px 0;
  font-size: 1rem;
  text-shadow: 0 0 8px #ff4b2b;
}
ul {
  list-style: none;
  padding: 0;
}
.project-item {
  background: rgba(44, 83, 100, 0.7);
  border-radius: 10px;
  margin-bottom: 18px;
  padding: 16px 18px;
  box-shadow: 0 0 8px #00ffe7 inset;
  color: #fff;
  transition: box-shadow 0.3s;
}
.project-item:hover {
  box-shadow: 0 0 16px #00ffe7 inset, 0 0 8px #1a2980;
}
.project-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #00ffe7;
  margin-bottom: 6px;
}
.project-desc {
  font-size: 1rem;
  color: #b2ebf2;
}
</style> 