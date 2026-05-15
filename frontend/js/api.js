const API_BASE = "";

async function request(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  const token = localStorage.getItem("token");
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    location.href = "/index.html";
    return;
  }

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) throw data.error || { code: "ERROR", message: "오류가 발생했습니다" };
  return data;
}

const api = {
  get: (path) => request("GET", path),
  post: (path, body) => request("POST", path, body),
  put: (path, body) => request("PUT", path, body),
  patch: (path, body) => request("PATCH", path, body),
  delete: (path) => request("DELETE", path),
};

function getUser() {
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
}

function requireAuth() {
  const token = localStorage.getItem("token");
  if (!token) { location.href = "/index.html"; return null; }
  return getUser();
}

function requireTeam() {
  const user = requireAuth();
  if (!user) return null;
  if (!user.team_id) { location.href = "/team.html"; return null; }
  return user;
}
