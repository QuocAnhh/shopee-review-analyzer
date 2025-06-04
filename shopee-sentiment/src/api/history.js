const API_URL = '/api/chats'; // Thay bằng domain thật nếu đã deploy

// Hàm tiện ích lấy token
export const getToken = () => {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    console.warn('No accessToken found in localStorage');
  }
  return token;
};

export const authHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${getToken() || ''}` 
});

// Lấy toàn bộ lịch sử chat
export const fetchHistory = async () => {
  const res = await fetch(API_URL, {
    method: 'GET',
    headers: authHeaders()
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Lỗi không xác định khi lấy lịch sử');
  return result.chats;
};

// Tạo chat mới (nếu cần)
export const createNewChat = async (initial_message = '') => {
  const res = await fetch(`${API_URL}/new`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ initial_message })
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Tạo cuộc trò chuyện thất bại');
  return result;
};

// Lấy chat theo ID
export const getChatById = async (chatId) => {
  const res = await fetch(`${API_URL}/${chatId}`, {
    method: 'GET',
    headers: authHeaders()
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Không tìm thấy cuộc trò chuyện');
  return result;
};

// Đổi tên chat
export const renameChat = async (chatId, newTitle) => {
  const res = await fetch(`${API_URL}/${chatId}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify({ new_title: newTitle })
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Đổi tên thất bại');
  return result;
};

// Đặt chat làm active
export const activateChat = async (chatId) => {
  const res = await fetch(`${API_URL}/${chatId}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify({ set_active: true })
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Không thể kích hoạt chat');
  return result;
};

// Xoá chat
export const deleteChat = async (chatId) => {
  const res = await fetch(`${API_URL}/${chatId}`, {
    method: 'DELETE',
    headers: authHeaders()
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Xoá chat thất bại');
  return result;
};

// Lấy chat đang active
export const fetchActiveChat = async () => {
  const res = await fetch(`${API_URL}/active`, {
    method: 'GET',
    headers: authHeaders()
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Không có chat đang hoạt động');
  return result;
};

// Cập nhật nội dung chat đang active
export const updateActiveChat = async (messages, title = '') => {
  const res = await fetch(`${API_URL}/active`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify({ messages, title })
  });

  const result = await res.json();
  if (!res.ok) throw new Error(result.error || 'Cập nhật thất bại');
  return result;
};