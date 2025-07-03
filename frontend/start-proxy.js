const ParcelProxyServer = require('parcel-proxy-server');

const server = new ParcelProxyServer({
  entryPoint: './public/index.html',
  parcelOptions: {},
  proxies: {
    '/api': {
      target: 'http://localhost:8000' // 后端服务地址
    }
  }
});

server.listen(1234, () => {
  console.log('Parcel proxy server running at http://localhost:1234');
}); 