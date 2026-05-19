const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const net = require('net');

let mainWindow;
const TARGET_PORT = 5173;
const TARGET_URL = `http://localhost:${TARGET_PORT}`;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1366,
    height: 768,
    minWidth: 1024,
    minHeight: 768,
    title: "Giày Đẹp Store - Hệ thống Quản lý Bán hàng",
    icon: path.join(__dirname, 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false // Cho phép gọi API và tải tài nguyên nội bộ dễ dàng
    }
  });

  // Ẩn menu mặc định để ứng dụng trông giống app native chuyên nghiệp
  Menu.setApplicationMenu(null);

  // Thử tải trang web
  loadWebApp();

  // Xử lý sự kiện khi không thể kết nối đến web app (ví dụ: server Vite chưa chạy)
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
    // Chỉ kích hoạt màn hình lỗi khi trang chính không tải được (bỏ qua các lỗi tài nguyên phụ/tracking)
    if (validatedURL === TARGET_URL || validatedURL.startsWith(TARGET_URL)) {
      console.log('Không thể kết nối đến Web App:', errorDescription);
      mainWindow.loadFile(path.join(__dirname, 'fallback.html'));
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function loadWebApp() {
  mainWindow.loadURL(TARGET_URL).catch(err => {
    console.log('Lần tải đầu tiên thất bại, chuyển sang màn hình chờ kết nối');
    mainWindow.loadFile(path.join(__dirname, 'fallback.html'));
  });
}

// Lắng nghe sự kiện thử lại kết nối từ màn hình fallback
ipcMain.on('retry-connection', () => {
  const socket = new net.Socket();
  socket.setTimeout(1500);

  // Kiểm tra xem port 5173 đã mở chưa
  socket.connect(TARGET_PORT, 'localhost', () => {
    socket.destroy();
    // Nếu kết nối thành công, tải lại trang web chính
    mainWindow.loadURL(TARGET_URL);
  });

  socket.on('error', () => {
    socket.destroy();
    mainWindow.webContents.send('connection-status', 'failed');
  });

  socket.on('timeout', () => {
    socket.destroy();
    mainWindow.webContents.send('connection-status', 'failed');
  });
});

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
