function test() {

}

document.addEventListener("DOMContentLoaded", function () {
    const loginArea = document.getElementById("login-area");
    const logoutArea = document.getElementById("logout-area");

    //아직 백엔드 없으니까 임시로 상태 고정
    const isLoggedIn = true; // true로 바꾸면 환영문구. 로그아웃 보임

    if (loginArea && logoutArea) {
        if (isLoggedIn) {
            loginArea.style.display = "none";
            logoutArea.style.display = "block";
        } else {
            loginArea.style.display = "block";
            logoutArea.style.display = "none";
        }
    }
});