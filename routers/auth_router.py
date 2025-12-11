###
import bcrypt
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
# from starlette.responses import RedirectResponse
from fastapi.responses import RedirectResponse
from sqlalchemy.sql.functions import user

from db import au_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

templates = Jinja2Templates(directory="templates")


# 로그인 화면
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 로그인 처리
@router.post("/login")
def login(
        request: Request,
        accountId: str = Form(...),
        password: str = Form(...)
):
    user = au_db.get_user(accountId)
    print("로그인 데이터:", user)

    if user:
        stored_hash = user["password"]

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return RedirectResponse(url="/movielist?userId=" + accountId, status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "msg": "아이디 또는 비밀번호가 올바르지 않습니다."}
    )


# 회원가입 화면
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


# 회원가입 처리
@router.post("/register")
def register(
    request: Request,
    accountId: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    gender: str = Form(...),
    birth: str = Form(...),
    occupation: int = Form(...)
):
    # 1) 비밀번호를 bcrypt로 해싱
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # 아이디 중복 체크
    existing = au_db.get_user(accountId)
    if existing:
        return templates.TemplateResponse(
            "join.html",
            {"request": request, "msg": "이미 존재하는 아이디입니다."}
        )

    # DB insert
    au_db.insert_user(accountId, hashed_pw.decode(), name, gender, birth, occupation)
    return RedirectResponse("/auth/login", status_code=302)



# 로그아웃
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    return response


# ====================================
#           유저 정보 조회 화면
# ====================================

@router.get("/mypage")
def mypage(request: Request, userId: str):
    user = au_db.get_user(userId)
    print(user)
    return templates.TemplateResponse("mypage.html", {"request": request, "user": user})


@router.post("/user/update")
def update_user(
    accountId: str = Form(...), # 새 아이디
    password: str = Form(""),    # 새 비밀번호
    name: str = Form(...),
    gender: str = Form(...),
    birth: str = Form(...),
    occupation: str = Form(...)
):

    print("------------------")
    print(accountId)

    # 비밀번호 처리
    if password.strip() == "":
        hashed_pw = None
    else:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    au_db.update_user(accountId, hashed_pw, name, gender, birth, occupation)

    return RedirectResponse(url=f"/auth/mypage?userId={accountId}", status_code=302)