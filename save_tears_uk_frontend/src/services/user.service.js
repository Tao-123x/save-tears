const API_URL = "http://127.0.0.1:8000";

export const registerUser = (username, password, household) => {
  return fetch(`${API_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
      room_number: household,
    }),
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else if (response.status === 400) {
        return response.json().then((err) => {
          throw err.detail;
        });
      } else {
        throw "Something went wrong";
      }
    })
    .catch((err) => {
      console.log("Err", err);
      return Promise.reject(err);
    });
};

export const loginUser = (username, password) => {
  return fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else if (response.status === 400) {
        return response.json().then((err) => {
          throw err.detail; // FastAPI uses "detail"
        });
      } else {
        throw "Something went wrong";
      }
    })
    .then((resJson) => {
      // store what YOUR backend returns
      localStorage.setItem("token", resJson.token);
      localStorage.setItem("username", resJson.username);
      localStorage.setItem("room_number", resJson.room_number);
      localStorage.setItem("role", resJson.role);

      return resJson;
    })
    .catch((err) => {
      console.log("Err", err);
      return Promise.reject(err);
    });
};